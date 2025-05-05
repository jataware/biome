import logging
import os
from pathlib import Path

from adhoc_api.loader import load_yaml_api
from adhoc_api.tool import AdhocApi, ensure_name_slug_compatibility
from adhoc_api.uaii import gpt_41, o3_mini

logger = logging.getLogger(__name__)
DATASOURCES_FOLDER = os.environ.get("BIOME_INTEGRATIONS_DIR", "../src/biome/datasources/")


def fetch_specs():
    if DATASOURCES_FOLDER == "":
        raise ValueError(
            "No BIOME_INTEGRATION_DIR set. "
            "Please set the environment variable of where the integrations reside."
        )

    datasource_root = (Path(__file__).resolve().parent.parent / DATASOURCES_FOLDER).resolve()

    data_dir_raw = os.environ.get("BIOME_DATA_DIR", "../data")
    try:
        data_dir = Path(data_dir_raw).resolve(strict=True)
        logger.info("Using data_dir", extra={"data_dir": data_dir})
    except OSError as e:
        data_dir = ""
        logger.error(
            "Failed to set biome data dir",
            extra={"data_dir_raw": data_dir_raw, "exception": e}
        )

    api_specs = []

    for datasource_dir in os.listdir(datasource_root):
        datasource_full_path = datasource_root / datasource_dir
        if datasource_dir == ".ipynb_checkpoints":
            Path.rmdir(datasource_full_path)

        if Path.is_dir(datasource_full_path):
            api_yaml = datasource_full_path / "api.yaml"
            if not api_yaml.is_file():
                logger.warning("Ignoring malformed API:", extra={"API": api_yaml})
                continue
            api_spec = load_yaml_api(api_yaml)
            ensure_name_slug_compatibility(api_spec)
            api_spec["documentation"] = api_spec["documentation"].replace(
                "{DATASET_FILES_BASE_PATH}",
                str(data_dir)
            )
            api_spec["documentation"] = api_spec["documentation"].replace(
                "{{DATASET_FILES_BASE_PATH}}",
                str(data_dir)
            )
            if "examples" in api_spec and isinstance(api_spec["examples"], list):
                for example in api_spec["examples"]:
                    if "code" in example and isinstance(example["code"], str):
                        example["code"] = example["code"].replace(
                            "{{DATASET_FILES_BASE_PATH}}",
                            str(data_dir)
                        )
                        example["code"] = example["code"].replace(
                            "{DATASET_FILES_BASE_PATH}",
                            str(data_dir)
                        )
            api_specs.append(api_spec)
    return api_specs

def initialize_adhoc():
    specs = fetch_specs()

    curator_config = {**o3_mini, 'api_key': os.environ.get("OPENAI_API_KEY")}
    gpt_41_config = {**gpt_41, 'api_key': os.environ.get("OPENAI_API_KEY")}


    return AdhocApi(
        apis=specs,
        drafter_config=[gpt_41_config],
        curator_config=curator_config,
        contextualizer_config=gpt_41_config
    )
