"""Public job discovery with source links and explicit provider limitations."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode, urlsplit, urlunsplit, quote
import os
import re

from dotenv import dotenv_values
import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


class JobCardParser(HTMLParser):
    fields = {'base-search-card__title': 'title', 'base-search-card__subtitle': 'company', 'job-search-card__location': 'location'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.job = {}
        self.capture = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set(attrs.get('class', '').split())
        for css, field in self.fields.items():
            if css in classes:
                self.capture = (tag, field)
        if tag == 'a' and 'base-card__full-link' in classes:
            self.job['url'] = attrs.get('href', '')
        if tag == 'time':
            self.job['posted'] = attrs.get('datetime', '')

    def handle_data(self, data):
        if self.capture:
            field = self.capture[1]
            self.job[field] = self.job.get(field, '') + data

    def handle_endtag(self, tag):
        if self.capture and tag == self.capture[0]:
            self.capture = None


def listing_url(value, source):
    """Only return actual listing links on the selected site's domain."""
    parsed = urlsplit(value)
    domain, prefix = ('linkedin.com', '/jobs/view/') if source == 'LinkedIn' else ('naukri.com', '/job-listings-')
    host = (parsed.hostname or '').lower()
    if parsed.scheme != 'https' or not (host == domain or host.endswith('.' + domain)) or not parsed.path.startswith(prefix):
        return ''
    return urlunsplit(('https', parsed.netloc, parsed.path, '', ''))


def search_links(role, location):
    slug = lambda value: quote(re.sub(r'\s+', '-', value.strip().lower()), safe='-')
    naukri_path = slug(role) + '-jobs' + ('-in-' + slug(location) if location else '')
    return {
        'LinkedIn': 'https://www.linkedin.com/jobs/search/?' + urlencode({'keywords': role, 'location': location}),
        'Naukri': 'https://www.naukri.com/' + naukri_path + '?' + urlencode({'k': role, 'l': location}),
    }


def matches_role(role, title):
    tokens = re.findall(r'[\w+#.]+', role.casefold())
    title_tokens = set(re.findall(r'[\w+#.]+', title.casefold()))
    return bool(tokens) and all(token in title_tokens for token in tokens)


def parse_linkedin(html, role):
    jobs, seen = [], set()
    for card in re.findall(r'<li\b[^>]*>(.*?)</li>', html, re.S | re.I):
        parser = JobCardParser()
        parser.feed(card)
        job = {key: ' '.join(value.split()) for key, value in parser.job.items()}
        url = listing_url(job.get('url', ''), 'LinkedIn')
        if url and url not in seen and matches_role(role, job.get('title', '')):
            job['url'] = url
            jobs.append(job)
            seen.add(url)
    return jobs[:10]


def search_api_key():
    key = os.getenv('SERPAPI_API_KEY') or dotenv_values(Path(__file__).resolve().parents[2] / '.env').get('SERPAPI_API_KEY')
    if not key:
        try:
            key = st.secrets.get('SERPAPI_API_KEY', '')
        except StreamlitSecretNotFoundError:
            key = ''
    return (key or '').strip()


def _search_source(role, location, source, api_key):
    result = {'role': role, 'source': source, 'search_url': search_links(role, location)[source], 'jobs': [], 'notice': ''}
    try:
        if source == 'LinkedIn':
            try:
                response = requests.get(result['search_url'], timeout=(5, 15))
                response.raise_for_status()
                result['jobs'] = parse_linkedin(response.text, role)
            except requests.RequestException:
                pass
            if result['jobs']:
                return result
        if api_key:
            site = 'linkedin.com/jobs/view/' if source == 'LinkedIn' else 'naukri.com/job-listings-'
            response = requests.get('https://serpapi.com/search.json', params={'engine': 'google', 'q': f'site:{site} {role} {location}', 'api_key': api_key}, timeout=(5, 15))
            response.raise_for_status()
            data = response.json()
            if data.get('error'):
                result['notice'] = 'The search provider could not complete this request. Check its key or quota.'
                return result
            seen = set()
            for item in data.get('organic_results', []):
                url = listing_url(item.get('link', ''), source)
                title = item.get('title', '')
                if url and url not in seen and matches_role(role, title):
                    result['jobs'].append({'title': title, 'url': url, 'snippet': item.get('snippet', ''), 'indexed': True})
                    seen.add(url)
            result['jobs'] = result['jobs'][:10]
        elif source == 'Naukri':
            result['notice'] = 'Open Naukri to view matching jobs. In-app listings require a configured search provider.'
            return result
        if not result['jobs']:
            result['notice'] = 'No matching listings could be retrieved. Open the site search for more results.'
    except (requests.RequestException, ValueError):
        # Do not expose request URLs: the search provider URL can contain a key.
        result['notice'] = 'Listings are temporarily unavailable. Use the site search link to continue.'
    return result


def find_jobs(roles, location, api_key=''):
    cleaned = list(dict.fromkeys(role.strip() for role in roles if role.strip()))
    if not cleaned or len(cleaned) > 5 or any(len(role) > 100 for role in cleaned) or len(location) > 100:
        raise ValueError('Enter one to five job roles (up to 100 characters each) and a location up to 100 characters.')
    tasks = [(role, location.strip(), source, api_key) for role in cleaned for source in ('LinkedIn', 'Naukri')]
    with ThreadPoolExecutor(max_workers=4) as executor:
        groups = list(executor.map(lambda args: _search_source(*args), tasks))
    return {'groups': groups, 'location': location.strip(), 'searched_at': datetime.now(timezone.utc).strftime('%d %b %Y, %H:%M UTC')}
