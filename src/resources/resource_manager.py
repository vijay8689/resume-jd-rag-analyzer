from __future__ import annotations

import html
from html.parser import HTMLParser
from pathlib import Path
from urllib import parse, request

import yaml


class _DuckDuckGoResultsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[dict[str, str]] = []
        self._current: dict[str, str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        if {"result__a", "result-link"}.intersection(classes):
            self._current = {"url": attributes.get("href") or "", "title": ""}

    def handle_data(self, data: str) -> None:
        if self._current is not None:
            self._current["title"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._current is not None:
            self._current["title"] = " ".join(self._current["title"].split())
            self.results.append(self._current)
            self._current = None


class ResourceManager:
    _tutorial_fallbacks = {
        "python": [
            {"title": "Python Official Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "tutorial"},
            {"title": "Real Python Tutorials", "url": "https://realpython.com/", "type": "tutorial"},
        ],
        "docker": [
            {"title": "Docker Get Started", "url": "https://docs.docker.com/get-started/", "type": "tutorial"},
            {"title": "Docker Tutorial", "url": "https://docker-curriculum.com/", "type": "tutorial"},
        ],
        "kubernetes": [
            {"title": "Kubernetes Basics", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "type": "tutorial"},
            {"title": "Kubernetes Tutorial", "url": "https://kubernetes.io/docs/home/", "type": "tutorial"},
        ],
        "playwright": [
            {"title": "Playwright Guide", "url": "https://playwright.dev/docs/intro", "type": "tutorial"},
            {"title": "Playwright Tutorial", "url": "https://playwright.dev/", "type": "tutorial"},
        ],
        "selenium": [
            {"title": "Selenium Getting Started", "url": "https://www.selenium.dev/documentation/webdriver/getting_started/", "type": "tutorial"},
            {"title": "Selenium Tutorial", "url": "https://www.selenium.dev/documentation/", "type": "tutorial"},
        ],
        "azure": [
            {"title": "Azure Getting Started", "url": "https://learn.microsoft.com/azure/", "type": "tutorial"},
            {"title": "Azure Free Training", "url": "https://learn.microsoft.com/training/", "type": "tutorial"},
        ],
    }

    def __init__(self, config_path: str | Path | None = None) -> None:
        self.config_path = Path(config_path or "config/learning_resources.yaml")

    def load(self) -> dict:
        """Load the curated learning resource YAML file."""
        if not self.config_path.exists():
            return {}
        with self.config_path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}

    def _fallback_tutorials(self, skill: str) -> list[dict]:
        """Provide known tutorial links for common skills when search results are unavailable."""
        key = (skill or "").strip().lower()
        return self._tutorial_fallbacks.get(key, [])

    def _search_duckduckgo_tutorials(self, skill: str) -> list[dict]:
        """Search DuckDuckGo for tutorial links related to a skill."""
        query = parse.quote(f"{skill} tutorial")
        seen: set[str] = set()
        results: list[dict] = []

        for endpoint in (
            f"https://html.duckduckgo.com/html/?q={query}",
            f"https://lite.duckduckgo.com/lite/?q={query}",
        ):
            try:
                req = request.Request(endpoint, headers={"User-Agent": "Mozilla/5.0"})
                with request.urlopen(req, timeout=5) as response:
                    body = response.read().decode("utf-8", "ignore")
            except Exception:
                continue

            parser = _DuckDuckGoResultsParser()
            parser.feed(body)
            for item in parser.results:
                destination = html.unescape(item["url"])
                parsed_url = parse.urlparse(parse.urljoin(endpoint, destination))
                if parsed_url.netloc.lower().endswith("duckduckgo.com"):
                    redirect_url = parse.parse_qs(parsed_url.query).get("uddg", [""])[0]
                    parsed_url = parse.urlparse(redirect_url)
                if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
                    continue
                url_value = parsed_url.geturl()
                if url_value in seen:
                    continue
                seen.add(url_value)
                results.append(
                    {
                        "title": item["title"] or f"{skill.title()} tutorial",
                        "url": url_value,
                        "type": "tutorial",
                    }
                )
                if len(results) == 5:
                    break
            if results:
                break

        return results[:5] if results else self._fallback_tutorials(skill)

    def get_resources_for_skill(self, skill: str) -> list[dict]:
        """Return learning resources for a specific skill."""
        data = self.load()
        key = (skill or "").strip().lower()
        resources = data.get(key, [])
        if resources:
            return resources
        return self._search_duckduckgo_tutorials(skill)

    def build_learning_roadmap(self, missing_skills: list[str]) -> dict:
        """Assemble learning resources keyed by missing skill."""
        resources = self.load()
        roadmap = {}
        for skill in missing_skills:
            if not skill:
                continue
            name = str(skill).strip()
            skill_key = name.lower()
            roadmap[name] = resources.get(skill_key, []) or self._search_duckduckgo_tutorials(name)
        return roadmap


def get_resource_manager() -> ResourceManager:
    """Return a resource manager instance."""
    return ResourceManager()
