from io import BytesIO

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


def test_duckduckgo_search_extracts_redirected_tutorial_links(monkeypatch):
    manager = ResourceManager("config/learning_resources.yaml")
    response = BytesIO(
        b'<a class="result__a" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Flearn.example%2Fpython">'
        b"Python Tutorial</a>"
    )
    monkeypatch.setattr("src.resources.resource_manager.request.urlopen", lambda *args, **kwargs: response)

    results = manager._search_duckduckgo_tutorials("python")

    assert results == [
        {
            "title": "Python Tutorial",
            "url": "https://learn.example/python",
            "type": "tutorial",
        }
    ]
