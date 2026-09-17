from __future__ import annotations

from pathlib import Path

import yaml


class ResourceManager:
    def __init__(self, config_path: str | Path | None = None) -> None:
        self.config_path = Path(config_path or "config/learning_resources.yaml")

    def load(self) -> dict:
        """Load the curated learning resource YAML file."""
        if not self.config_path.exists():
            return {}
        with self.config_path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}

    def get_resources_for_skill(self, skill: str) -> list[dict]:
        """Return learning resources for a specific skill."""
        data = self.load()
        return data.get(skill.lower(), [])

    def build_learning_roadmap(self, missing_skills: list[str]) -> dict:
        """Assemble learning resources keyed by missing skill."""
        resources = self.load()
        roadmap = {}
        for skill in missing_skills:
            roadmap[skill] = resources.get(skill.lower(), [])
        return roadmap


def get_resource_manager() -> ResourceManager:
    """Return a resource manager instance."""
    return ResourceManager()
