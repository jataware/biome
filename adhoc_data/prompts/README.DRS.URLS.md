You have access to a tool for accessing DRS urls in the form of `drs://`, but you may also do it inline
with the following snippet. Provide the URIs in `uris`

```py
uri = ""
if not uri.startswith("drs://"):
    raise ValueError("Invalid DRS URI: Must start with 'drs://'")
try:
    object_id = uri.split(":")[-1]
except IndexError:
    raise ValueError("Invalid DRS URI: Missing object ID")
url = f"https://nci-crdc.datacommons.io/ga4gh/drs/v1/objects/{object_id}"
response = requests.get(url)
response.raise_for_status()
file_info = response.json()
```

If you want to download a file that you have a DRS URI to,

```py
https_url = None
for access_method in file_info.get('access_methods', []):
    if access_method.get('type') == 'https':
        https_url = access_method['access_url']['url']
        break

if https_url:
    file_size = file_info.get('size', 'unknown size')
    print(f"Downloading: {filename} ({file_size} bytes)")
    file_response = requests.get(https_url, stream=True)
    file_response.raise_for_status()
    file_path = os.path.join(download_path, filename)
    with open(file_path, 'wb') as f:
        for chunk in file_response.iter_content(chunk_size=8192):
            f.write(chunk)
else:
    print(f"Failed to find HTTPS download link: {file_info}")
```
