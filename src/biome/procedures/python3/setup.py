import IPython
import warnings
import os

# Set API keys if provided
_api_keys = {
    "API_EPA_AQS_EMAIL": "{{aqs_email}}",
    "API_EPA_AQS": "{{aqs_api_key}}",
    "API_OPENFDA": "{{openfda_faers_api_key}}",
    "API_USDA_FDC": "{{usda_fdc_api_key}}",
    "API_CENSUS": "{{census_api_key}}",
    "API_CDC_TRACKING_NETWORK": "{{cdc_tracking_network_api_key}}",
    "API_SYNAPSE": "{{synapse_api_key}}",
    "NETRIAS_KEY": "{{netrias_api_key}}",
    "ALPHAGENOME_KEY": "{{alphagenome_key}}",
    "IMMPORT_USERNAME": "{{immport_username}}",
    "IMMPORT_PASSWORD": "{{immport_password}}"
}
for key, value in _api_keys.items():
    if value and value != "None":
        os.environ.setdefault(key, value)

formatter = IPython.get_ipython().display_formatter.formatters['text/plain']
formatter.max_seq_length = 0
warnings.filterwarnings('ignore', category=FutureWarning)
print("Setup complete")
