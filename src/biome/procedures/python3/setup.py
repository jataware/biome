import IPython
import warnings

formatter = IPython.get_ipython().display_formatter.formatters['text/plain']
formatter.max_seq_length = 0
warnings.filterwarnings('ignore', category=FutureWarning)
print("Setup complete")