from urllib.parse import parse_qs, urlsplit
from unittest.mock import Mock
import pytest
import requests
from src.services import job_search_service as jobs


def test_search_links_preserve_role_and_location():
    links = jobs.search_links('C++ Developer', 'New Delhi')
    assert parse_qs(urlsplit(links['LinkedIn']).query)['keywords'] == ['C++ Developer']
    assert parse_qs(urlsplit(links['Naukri']).query) == {'k':['C++ Developer'], 'l':['New Delhi']}


def test_linkedin_parser_filters_and_deduplicates():
    card = '<li><a class="base-card__full-link" href="https://in.linkedin.com/jobs/view/python-123?trackingId=1"></a><h3 class="base-search-card__title">Python Developer</h3><h4 class="base-search-card__subtitle"><a>Example Company</a></h4><span class="job-search-card__location">India</span></li>'
    results = jobs.parse_linkedin(card + card + card.replace('Python Developer', 'Java Developer'), 'Python Developer')
    assert len(results) == 1
    assert results[0]['company'] == 'Example Company'
    assert '?' not in results[0]['url']


@pytest.mark.parametrize('url', ['https://naukri.com.evil.test/job-listings-123', 'javascript:alert(1)', 'https://www.naukri.com/python-jobs'])
def test_listing_links_reject_untrusted_or_search_urls(url):
    assert not jobs.listing_url(url, 'Naukri')


def test_naukri_indexed_results(monkeypatch):
    response = Mock()
    response.json.return_value = {'organic_results': [{'title':'Python Developer - Example', 'link':'https://www.naukri.com/job-listings-python-123', 'snippet':'Python role in Delhi'}, {'title':'Unrelated role', 'link':'https://www.naukri.com/job-listings-other-456'}]}
    monkeypatch.setattr(jobs.requests, 'get', lambda *args, **kwargs: response)
    result = jobs._search_source('Python Developer', 'Delhi', 'Naukri', 'test-key')
    assert len(result['jobs']) == 1
    assert result['jobs'][0]['indexed']


def test_provider_failure_retains_link_without_exposing_key(monkeypatch):
    def fail(*args, **kwargs):
        raise requests.ConnectionError('URL contained test-secret')
    monkeypatch.setattr(jobs.requests, 'get', fail)
    result = jobs._search_source('Developer', 'India', 'Naukri', 'test-secret')
    assert result['search_url']
    assert result['notice']
    assert 'test-secret' not in str(result)


def test_validation_and_no_key_fallback():
    with pytest.raises(ValueError):
        jobs.find_jobs([' '], 'India')
    result = jobs._search_source('Developer', 'India', 'Naukri', '')
    assert not result['jobs']
    assert 'configured search provider' in result['notice']
