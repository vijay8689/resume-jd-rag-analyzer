from src.resources.resource_manager import ResourceManager


def test_resources_load_successfully():
    manager = ResourceManager("config/learning_resources.yaml")
    data = manager.load()
    assert "playwright" in data
