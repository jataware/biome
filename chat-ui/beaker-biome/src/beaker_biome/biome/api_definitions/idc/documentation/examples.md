# Examples

## Example 1: Get columns available in IDC index

```
from idc_index import index
import pandas as pd

client = index.IDCClient()

# First, let's see what columns are available
query_columns = """
SELECT * FROM index LIMIT 1
"""

try:
    df = client.sql_query(query_columns)
    print("Available columns in the index:")
    print(df.columns.tolist())
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

## Example 2: Get slide microscopy data

```
from idc_index import index
import pandas as pd

client = index.IDCClient()

# Query for slide microscopy data
query = """
SELECT DISTINCT
    collection_id,
    PatientID,
    SeriesDescription,
    StudyDescription,
    BodyPartExamined,
    SeriesDate
FROM
    index
WHERE
    Modality = 'SM'
"""

try:
    df = client.sql_query(query)
    print("Slide Microscopy Data Available:")
    print("\nCollections with slide microscopy data:")
    print(df['collection_id'].unique())
    print("\nSample of the data:")
    print(df.head())
    print("\nTotal number of records:", len(df))
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

## Example 3: Get slide microscopy data for a specific collection

```
from idc_index import index
import pandas as pd

client = index.IDCClient()

# Query for AML-specific slide microscopy data
query = """
SELECT DISTINCT
    collection_id,
    PatientID,
    SeriesDescription,
    StudyDescription,
    BodyPartExamined,
    SeriesDate,
    Manufacturer,
    ManufacturerModelName,
    SeriesNumber,
    instanceCount
FROM
    index
WHERE
    Modality = 'SM'
    AND collection_id IN ('cptac_aml', 'cmb_aml')
ORDER BY
    PatientID, SeriesDate
"""

try:
    df = client.sql_query(query)
    print("AML Slide Microscopy Data:")
    print("\nTotal number of records:", len(df))
    
    print("\nUnique patients:", len(df['PatientID'].unique()))
    
    print("\nTypes of series descriptions (slide types):")
    print(df['SeriesDescription'].unique())
    
    print("\nSample of the data:")
    print(df.head(10))
    
    # Save to a CSV file for further analysis
    df.to_csv('aml_pathology_data.csv', index=False)
    print("\nData has been saved to 'aml_pathology_data.csv'")
    
except Exception as e:
    print(f"An error occurred: {str(e)}")   
```

## Example 4: Get additional information for microscopy data for a specific collection

```
from idc_index import index
import pandas as pd

client = index.IDCClient()

# Query for all available fields for AML slides
query = """
SELECT *
FROM
    index
WHERE
    Modality = 'SM'
    AND collection_id IN ('cptac_aml', 'cmb_aml')
    AND SeriesDescription LIKE '%bone marrow%'
ORDER BY
    PatientID, SeriesDate
"""

try:
    df = client.sql_query(query)
    print("AML Bone Marrow Slide Data:")
    print("\nTotal number of bone marrow slides:", len(df))
    
    print("\nAvailable columns (metadata fields):")
    print(df.columns.tolist())
    
    # Look for any columns that might contain annotations or clinical data
    clinical_cols = [col for col in df.columns if any(term in col.lower() 
                                                    for term in ['annotation', 'clinical', 'blast', 'cell', 
                                                               'pathology', 'diagnosis', 'grade', 'stage'])]
    print("\nPotentially relevant clinical/annotation columns:")
    print(clinical_cols)
    
    # Get the source DOIs which might lead to additional clinical data
    print("\nUnique source DOIs (for finding additional clinical data):")
    print(df['source_DOI'].unique())
    
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Let's also check if there are any study-level annotations
query_study = """
SELECT DISTINCT
    StudyDescription,
    collection_id,
    source_DOI,
    license_short_name
FROM
    index
WHERE
    collection_id IN ('cptac_aml', 'cmb_aml')
"""

try:
    df_study = client.sql_query(query_study)
    print("\nStudy-level information:")
    print(df_study)
except Exception as e:
    print(f"An error occurred querying study data: {str(e)}")
```

Example 5: Query to get download URLs for bone marrow slides

```
from idc_index import index
import pandas as pd

client = index.IDCClient()

# Query to get download URLs for bone marrow slides
query = """
SELECT
    PatientID,
    SeriesDescription,
    series_aws_url,
    series_size_MB
FROM
    index
WHERE
    Modality = 'SM'
    AND collection_id IN ('cptac_aml', 'cmb_aml')
    AND SeriesDescription LIKE '%bone marrow%'
LIMIT 1
"""

try:
    df = client.sql_query(query)
    print("Sample slide information:")
    print(df)
    
    if not df.empty:
        url = df['series_aws_url'].iloc[0]
        size_mb = df['series_size_MB'].iloc[0]
        print(f"\nFile size: {size_mb:.2f} MB")
        print(f"Download URL: {url}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

## Example 6: Get list of files in an S3 bucket for a specific collection on IDC

```
import boto3
from botocore import UNSIGNED
from botocore.config import Config
import os
import tempfile

# Function to list contents of an S3 path
def list_s3_contents(bucket, prefix):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    try:
        result = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' in result:
            return result['Contents']
        return []
    except Exception as e:
        print(f"Error listing S3 contents: {str(e)}")
        return []

# Parse S3 URL and list contents
s3_url = "s3://idc-open-data/d53e7fc3-8ef9-4de5-8059-47b21a67eb4f"
bucket = s3_url.split('/')[2]
prefix = '/'.join(s3_url.split('/')[3:])

print(f"Checking contents of bucket: {bucket}")
print(f"With prefix: {prefix}")

contents = list_s3_contents(bucket, prefix)
print("\nFound files:")
for item in contents:
    print(f"- {item['Key']} ({item['Size']/1024/1024:.2f} MB)")

# Let's also check if we can get any pre-signed URLs or public access URLs
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
try:
    # Try to get the bucket location
    location = s3.get_bucket_location(Bucket=bucket)
    print(f"\nBucket location: {location}")
    
    # Try to get bucket policy
    try:
        policy = s3.get_bucket_policy(Bucket=bucket)
        print("\nBucket policy:", policy)
    except Exception as e:
        print("\nCouldn't get bucket policy:", str(e))
        
except Exception as e:
    print(f"\nError getting bucket information: {str(e)}")
```

## Example 7: Download and visualize a slide microscopy image with pydicom and matplotlib

```
import sys
import subprocess

# Install required package
subprocess.check_call([sys.executable, "-m", "pip", "install", "pydicom"])

import boto3
from botocore import UNSIGNED
from botocore.config import Config
import os
import tempfile
import pydicom
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Create S3 client
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

# Create temporary directory
temp_dir = tempfile.mkdtemp()

# Let's try the smallest DICOM file first
file_key = "d53e7fc3-8ef9-4de5-8059-47b21a67eb4f/40006642-6ee5-44ca-bc5f-e1cc2bd7ee70.dcm"
local_file = os.path.join(temp_dir, "slide.dcm")

try:
    print(f"Downloading file: {file_key}")
    s3.download_file('idc-open-data', file_key, local_file)
    print("Download successful!")
    
    # Try to read the DICOM file
    print("\nReading DICOM file...")
    ds = pydicom.dcmread(local_file)
    
    print("\nDICOM metadata:")
    print(f"Patient ID: {ds.PatientID}")
    print(f"Modality: {ds.Modality}")
    print(f"Image Type: {ds.ImageType}")
    
    # Convert to image and display
    if hasattr(ds, 'pixel_array'):
        print("\nConverting to image...")
        pixel_array = ds.pixel_array
        
        # Normalize the pixel values
        if pixel_array.dtype != np.uint8:
            pixel_array = ((pixel_array - pixel_array.min()) * 255.0 / 
                         (pixel_array.max() - pixel_array.min())).astype(np.uint8)
        
        # Create image
        img = Image.fromarray(pixel_array)
        
        # Display
        plt.figure(figsize=(15, 10))
        plt.imshow(img, cmap='gray')
        plt.axis('off')
        plt.title(f"DICOM Image - Patient: {ds.PatientID}")
        plt.show()
    else:
        print("No pixel data found in the DICOM file")
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Clean up
    if os.path.exists(local_file):
        os.remove(local_file)
    os.rmdir(temp_dir)
```

## Example 8: Download and visualize a slide microscopy image with pydicom and matplotlib

```
import sys
import boto3
from botocore import UNSIGNED
from botocore.config import Config
import os
import tempfile
import pydicom
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Create S3 client
s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

# Create temporary directory
temp_dir = tempfile.mkdtemp()

# Let's try one of the larger image tiles
file_key = "d53e7fc3-8ef9-4de5-8059-47b21a67eb4f/6f8f2731-cf43-4ae0-a328-186101d6fcd8.dcm"
local_file = os.path.join(temp_dir, "slide_tile.dcm")

try:
    print(f"Downloading file: {file_key}")
    print("(This might take a while as it's a large file...)")
    s3.download_file('idc-open-data', file_key, local_file)
    print("Download successful!")
    
    # Try to read the DICOM file
    print("\nReading DICOM file...")
    ds = pydicom.dcmread(local_file)
    
    print("\nDICOM metadata:")
    print(f"Patient ID: {ds.PatientID}")
    print(f"Modality: {ds.Modality}")
    print(f"Image Type: {ds.ImageType}")
    print(f"Rows x Columns: {ds.Rows} x {ds.Columns}")
    if hasattr(ds, 'PhotometricInterpretation'):
        print(f"Photometric Interpretation: {ds.PhotometricInterpretation}")
    if hasattr(ds, 'SamplesPerPixel'):
        print(f"Samples Per Pixel: {ds.SamplesPerPixel}")
    
    # Convert to image and display
    if hasattr(ds, 'pixel_array'):
        print("\nConverting to image...")
        pixel_array = ds.pixel_array
        
        print(f"Pixel array shape: {pixel_array.shape}")
        print(f"Pixel array dtype: {pixel_array.dtype}")
        
        # Normalize the pixel values
        if pixel_array.dtype != np.uint8:
            pixel_array = ((pixel_array - pixel_array.min()) * 255.0 / 
                         (pixel_array.max() - pixel_array.min())).astype(np.uint8)
        
        # Create image
        img = Image.fromarray(pixel_array)
        
        # Display
        plt.figure(figsize=(15, 10))
        plt.imshow(img, cmap='gray')
        plt.axis('off')
        plt.title(f"DICOM Image Tile - Patient: {ds.PatientID}")
        plt.show()
    else:
        print("No pixel data found in the DICOM file")
    
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Clean up
    if os.path.exists(local_file):
        os.remove(local_file)
    os.rmdir(temp_dir)
```