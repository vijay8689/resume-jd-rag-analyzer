from src.resources.resource_manager import ResourceManager


def test_resources_load_successfully():
    manager = ResourceManager("config/learning_resources.yaml")
    data = manager.load()
    assert "playwright" in data


def test_build_learning_roadmap_uses_duckduckgo_fallback(monkeypatch):
    manager = ResourceManager("config/learning_resources.yaml")

    monkeypatch.setattr(
        manager,
        "_search_duckduckgo_tutorials",
        lambda skill: [{"title": f"{skill} tutorial", "url": "https://example.com/tutorial"}],
    )

    roadmap = manager.build_learning_roadmap(["tensorflow"])
    assert roadmap["tensorflow"][0]["url"] == "https://example.com/tutorial"
