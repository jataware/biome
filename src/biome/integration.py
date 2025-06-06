import yaml
from pathlib import Path
import os
import logging

logger = logging.getLogger(__name__)

def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)
yaml.add_representer(str, str_presenter)
yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

# add dumpers but not loaders, since we need to get raw specifications elsewhere to give to beaker

class LoadYamlTag(yaml.YAMLObject):
    yaml_tag = "!load_yaml"
    def __init__(self, payload):
        self.payload = payload
    def __repr__(self):
        return f"LoadYamlTag({self.payload})"
    @classmethod
    def from_yaml(cls, loader, node):
        return LoadYamlTag(node.value)
    @classmethod
    def to_yaml(cls, dumper, data):
        logger.warning(msg="load_yaml dump")
        return dumper.represent_scalar(cls.yaml_tag, data.payload)

# yaml.SafeLoader.add_constructor("!load_yaml", LoadYamlTag.from_yaml)
yaml.SafeDumper.add_multi_representer(LoadYamlTag, LoadYamlTag.to_yaml)


class LoadTextTag(yaml.YAMLObject):
    yaml_tag = "!load_txt"
    def __init__(self, payload):
        self.payload = payload
    def __repr__(self):
        return f"LoadTextTag({self.payload})"
    @classmethod
    def from_yaml(cls, loader, node):
        return LoadTextTag(node.value)
    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, data.payload)

# yaml.SafeLoader.add_constructor("!load_txt", LoadTextTag.from_yaml)
yaml.SafeDumper.add_multi_representer(LoadTextTag, LoadTextTag.to_yaml)


class FillTag(yaml.YAMLObject):
    yaml_tag = "!fill"
    def __init__(self, payload):
        self.payload = payload
    def __repr__(self):
        return f"FillTag({self.payload})"
    @classmethod
    def from_yaml(cls, loader, node):
        return FillTag(node.value)
    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, data.payload, style="|")

# yaml.SafeLoader.add_constructor("!fill", FillTag.from_yaml)
yaml.SafeDumper.add_multi_representer(FillTag, FillTag.to_yaml)


def create_file_model(content: str):
    return {
        "type": "file",
        "format": "text",
        "content": content
    }


def create_directory_model():
    return {
        "type": "directory",
        "format": "json",
        "mimetype": None
    }


def get_integration_slug(integration):
    return integration.get("slug", integration.get("name", "").lower().replace(" ", "_"))


def get_integration_folder(integration):
    url: str = integration.get("url", "")
    if url == "":
        return get_integration_slug(integration)
    elif url.endswith("api.yaml"):
        return url[:-(len("api.yaml"))]
    else:
        return url


def get_integration_base_path(integration):
    return (Path(os.environ.get("BIOME_INTEGRATIONS_DIR", "./"))
                / get_integration_folder(integration)).resolve()


def create_folder_structure_for_integration(manager, integration):
    base_path = get_integration_base_path(integration)
    if not manager.dir_exists(str(base_path)):
        manager.save(create_directory_model(), str(base_path))
    documentation_path = base_path / "documentation"
    if not manager.dir_exists(str(documentation_path)):
        manager.save(create_directory_model(), str(documentation_path))


def format_integration(integration):
    saved_fields = {
        "name": integration.get("name"),
        "slug": get_integration_slug(integration),
        "cache_key": f"integration_{get_integration_slug(integration)}",
        "examples": LoadYamlTag("documentation/examples.yaml"),
        "description": integration.get("description"),
        "documentation": FillTag(integration.get("source"))
    }
    for file in integration.get("attached_files", []):
        print('a')
        saved_fields[file.get("name")] = LoadTextTag(
            f"documentation/{file.get('filepath')}"
        )
    return yaml.safe_dump(saved_fields)


def write_integration(manager, integration):
    base_path = get_integration_base_path(integration)
    create_folder_structure_for_integration(manager, integration)

    example_path = base_path / "documentation" / "examples.yaml"
    manager.save(
        create_file_model(yaml.safe_dump(integration.get("examples", ""))),
        str(example_path)
    )

    integration_yaml_path = base_path / "api.yaml"
    manager.save(
        create_file_model(format_integration(integration)),
        str(integration_yaml_path)
    )
