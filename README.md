# Biome 

Biome is an AI powered platform for performing the next generation of biomedical research. It is currently in the prototype stage of development and is under active development.

The goal of Biome is to seamlessly combine the ability to find research data with an ability to deeply analyze it--all from the same user interface. To accomplish this, Biome provides users both a chat and notebook style interface with specialized AI integrations under the hood that enable sophisticated interactions with a variety of biomedical data sources as well as domain specific software libraries and tools. 

Biome is being developed under ARPA-H's [Biomedical Data Fabric (BDF) Toolbox](https://arpa-h.gov/news-and-events/arpa-h-announces-effort-develop-single-data-system-biomedical-research) program.


## Requirements

- docker-compose

## Getting started 

Many environment variables will need to be defined. See `env.sample` for one to copy and paste, and/or consult the same thing inline below.

You will need to add the API keys.

Copy all of `env.sample` to `.env` in the root of the project directory, then add the keys.

Example:  
```
cp env.sample .env
```

The keys are defined at the top. All of the variables that are not necessary to manually change have been omitted below with the ellipses.

If running from Docker, leave the BIOME_DATA_DIR and BIOME_INTEGRATION_DIR values unset in .env, as the docker-compose defaults will be fine.

If not running from Docker, ensure you set them with .env.

```
# API Keys
OPENAI_API_KEY=<your API key>
GEMINI_API_KEY=<your API key>
ANTHROPIC_API_KEY=<your API key>
```

Note--by default, Biome will use Anthropic as the LLM provider. You can adjust this by changing the `LLM_PROVIDER_IMPORT_PATH` variable and the `LLM_SERVICE_MODEL` variables. You can leave the rest of the variables as is, unless you're doing a custom deployment. Currently at least Gemini and Anthropic keys are required.

If you wish to run Biome locally, outside of Docker you can install `beaker-kernel` then run `pip install -e .` from the root of the project directory. You'll then be able to run it via `beaker biome`.

### Initialization

First, fetch the large files from git lfs with:

```
git lfs pull
```

Starting the project with the following command: 
```
docker compose up -d
```

and can be brought down with
```
docker compose down
```

## Usage

Visit `http://localhost:8888` in the browser to use the Biome interface.


## Demo Videos (outdated...)

Workflow screen recording (at 2x speed) 

https://github.com/user-attachments/assets/4f08307b-dc60-4d90-a52e-6f6962dde76e


Notebook workflow and editing 

https://github.com/user-attachments/assets/6dea0820-2b3f-4f32-8a56-a2c8f5f70002

## Data Sources with API credentials

Some sources require API credentials to be set in the `.env` file, see `env.sample` for the applicable sources and variables that need to be set.
At this time, the following authenticated APIs are supported:
- AQS (Air Quality System)
  - Register for an API key at: https://aqs.epa.gov/data/api/signup?email=myemail@example.com 
- FAERS (subset of FDA Adverse Event Reporting System)
  - Register for an API key at: https://open.fda.gov/apis/authentication/
- USDA FoodData Central
  - Register for an API key at: https://fdc.nal.usda.gov/api-key-signup
- Census ACS (American Community Survey) and SF1
  - Register for an API key at: https://api.census.gov/data/key_signup.html
- Synapse (and nf.synapse.org Data Portal)
  - Register for an API key at: https://accounts.synapse.org/register1?appId=synapse.org
  - Go to User > Account Settings > Personal Access Token to create credentials
- Netrias
  - Request access from the Netrias team directly
- CDC Tracking Network
  - Email nephtrackingsupport@cdc.gov with name, email and organization for an API token.
    
## Data Files

Large data files are stored using Git LFS in the `data/` directory. To work with these files:

1. Install Git LFS: https://git-lfs.com/
2. After cloning the repository, run: `git lfs pull` to download the actual data files

## Funding

The development of Biome is based upon work supported by the Defense Advanced Research Projects Agency (DARPA) under Agreement No. HR00112490514.
