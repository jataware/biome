import os

os.environ["{{ key_name }}"] = "{{ key_value }}"
f"Environment variable {{ key_name }} has been set"
