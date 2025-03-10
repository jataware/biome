import IPython
import warnings
import os

os.environ.setdefault("API_EPA_AQS_EMAIL", "{{aqs_email}}")
os.environ.setdefault("API_EPA_AQS", "{{aqs_api_key}}")

formatter = IPython.get_ipython().display_formatter.formatters['text/plain']
formatter.max_seq_length = 0
warnings.filterwarnings('ignore', category=FutureWarning)
print("Setup complete")