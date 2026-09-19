from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib import parse, request

import yaml


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
        q_variants = [f"{skill} tutorial", f"{skill} course", f"{skill} for beginners"]
        seen: set[str] = set()
        results: list[dict] = []

        for query in q_variants:
            encoded = parse.quote(query)
            for endpoint in (
                f"https://duckduckgo.com/html/?q={encoded}",
                f"https://lite.duckduckgo.com/lite/?q={encoded}",
                f"https://api.duckduckgo.com/?q={encoded}&format=json&no_redirect=1&skip_disambig=1",
            ):
                try:
                    req = request.Request(endpoint, headers={"User-Agent": "Mozilla/5.0"})
                    with request.urlopen(req, timeout=12) as response:
                        body = response.read().decode("utf-8", "ignore")
                except Exception:
                    continue

                if endpoint.startswith("https://api.duckduckgo.com"):
                    try:
                        payload = json.loads(body)
                    except json.JSONDecodeError:
                        continue
                    for item in payload.get("RelatedTopics", []) or []:
                        if isinstance(item, dict):
                            nested_items = item.get("Topics", [item]) if isinstance(item.get("Topics"), list) else [item]
                            for nested in nested_items:
                                if not isinstance(nested, dict):
                                    continue
                                url_value = nested.get("FirstURL") or nested.get("URL")
                                if not url_value or not url_value.startswith("http") or url_value in seen:
                                    continue
                                title = nested.get("Text") or nested.get("Title") or skill
                                seen.add(url_value)
                                results.append({"title": title, "url": url_value, "type": "tutorial"})
                    if payload.get("AbstractURL") and payload.get("AbstractURL") not in seen:
                        seen.add(payload["AbstractURL"])
                        results.append({"title": payload.get("Heading") or f"{skill} tutorial", "url": payload["AbstractURL"], "type": "tutorial"})
                    if results:
                        break
                    continue

                pattern = re.compile(r'href=\"(https?://[^\"]+)\"', re.IGNORECASE)
                matches = pattern.findall(body)
                for url_value in matches:
                    cleaned = html.unescape(url_value)
                    if "duckduckgo.com" in cleaned or cleaned in seen or not cleaned.startswith("http"):
                        continue
                    title = skill.title()
                    if title not in [r.get("title") for r in results]:
                        seen.add(cleaned)
                        results.append({"title": f"{title} tutorial", "url": cleaned, "type": "tutorial"})
                if results:
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
