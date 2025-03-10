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


```
# API Keys
OPENAI_API_KEY=<your API key>
GEMINI_API_KEY=<your API key>
ANTHROPIC_API_KEY=<your API key>
```

You can leave the rest of the variables as is, unless you're doing a custom deployment.

You'll also need to create a `.beaker.conf` file in the root of the project directory. See `.beaker.conf.template` for an example. 
When running on Docker, the file is already mounted by default (see `docker-compose.yaml`). This file selects the provider, or base agent, to be used. The environment variables are used to support the multi-agent API integration; currently at least Gemini and Anthropic keys are required. In the future this will become configurable.
Update the .beaker.conf values with...

### Initialization

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


## Funding

The development of Biome is based upon work supported by the Defense Advanced Research Projects Agency (DARPA) under Agreement No. HR00112490514.
