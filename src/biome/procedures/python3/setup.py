import IPython
import warnings
import os

# Set environment variables from the biome context template vars
os.environ.setdefault("API_EPA_AQS_EMAIL", "{{aqs_email}}")
os.environ.setdefault("API_EPA_AQS", "{{aqs_api_key}}")
os.environ.setdefault("API_OPENFDA", "{{openfda_faers_api_key}}")
os.environ.setdefault("API_USDA_FDC", "{{usda_fdc_api_key}}")
os.environ.setdefault("API_CENSUS", "{{census_api_key}}")
os.environ.setdefault("API_CDC_TRACKING_NETWORK", "{{cdc_tracking_network_api_key}}")
os.environ.setdefault("API_SYNAPSE", "{{synapse_api_key}}")
os.environ.setdefault("NETRIAS_KEY", "{{netrias_api_key}}")
os.environ.setdefault("ALPHAGENOME_KEY", "{{alphagenome_key}}")
os.environ.setdefault("IMMPORT_USERNAME", "{{immport_username}}")
os.environ.setdefault("IMMPORT_PASSWORD", "{{immport_password}}")
os.environ.setdefault("API_EPA_AQS_EMAIL", "{{aqs_email}}")
os.environ.setdefault("API_EPA_AQS", "{{aqs_key}}")
formatter = IPython.get_ipython().display_formatter.formatters['text/plain']
formatter.max_seq_length = 0
warnings.filterwarnings('ignore', category=FutureWarning)
print("Setup complete")
