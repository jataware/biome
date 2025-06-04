::: {#33d59592-e660-499a-89f4-c4ee4293f8d8 .cell .markdown}
# Example: Open mHealth Blood Pressure Visualization
:::

::: {#fc2e0d76-407c-433d-9254-eb70a2e118a1 .cell .markdown}
We generate random Open mHealth blood pressure readings, and visualize
them with matplotlib.
:::

:::: {#161d9075-5670-474d-926a-c62d71d77953 .cell .code execution_count="1"}
``` python
%pip install -q pandas matplotlib requests
```

::: {.output .stream .stdout}
    Note: you may need to restart the kernel to use updated packages.
:::
::::

::: {#4714741c-dfb0-4f84-a9a0-9cf7e4ea39a2 .cell .code execution_count="2"}
``` python
import random
from datetime import datetime, timedelta

import pandas as pd
import matplotlib.pyplot as plt
```
:::

::: {#342837d3-aba9-4c76-bb79-bbd5f776e7f9 .cell .code execution_count="3"}
``` python
def generate_blood_pressure_readings(num_readings):
    '''
    Generate random Open mHealth blood pressure readings.
    https://www.openmhealth.org/documentation/#/schema-docs/schema-library/schemas/omh_blood-pressure
    '''
    readings = []
    start_time = datetime(2020, 1, 1, 0, 0, 0)
    
    for _ in range(num_readings):
        # Generate random systolic and diastolic blood pressure values
        systolic = random.randint(100, 160)  # Assuming normal range for systolic pressure
        diastolic = random.randint(60, 100)  # Assuming normal range for diastolic pressure
        
        # Generate random measurement location, body posture, and temporal relationship to physical activity
        body_posture = random.choice(["sitting", "standing"])
        measurement_location = random.choice(["left wrist", "right wrist"])
        temporal_relationship_to_physical_activity = random.choice(["at rest", "during exercise"])

        # Generate a random effective time frame
        time_frame = start_time + timedelta(minutes=random.randint(1, 60*24*365))

        # Append the reading to the list
        readings.append({
            "systolic_blood_pressure": {"value": systolic, "unit": "mmHg"},
            "diastolic_blood_pressure": {"value": diastolic, "unit": "mmHg"},
            "body_posture": body_posture,
            "measurement_location": measurement_location,
            "temporal_relationship_to_physical_activity": temporal_relationship_to_physical_activity,
            "effective_time_frame": { "date_time": time_frame.strftime("%Y-%m-%dT%H:%M:%SZ") }
        })
        
    return readings
```
:::

::: {#7e8b501c-576c-4325-9476-047850d0dae2 .cell .code execution_count="4"}
``` python
def plot_readings_over_time(readings):
    '''
    Plot Open mHealth blood pressure readings.
    '''
    # Create a DataFrame from the readings
    df = pd.DataFrame(readings)

    # Convert effective_time_frame to datetime format
    df['effective_time_frame'] = pd.to_datetime(df['effective_time_frame'].apply(lambda x: x['date_time']))

    # Sort DataFrame by effective_time_frame
    df = df.sort_values(by='effective_time_frame')

    # Plot systolic and diastolic blood pressure over time
    plt.figure(figsize=(10, 6))
    plt.plot(df['effective_time_frame'], df['systolic_blood_pressure'].apply(lambda x: x['value']), 
             label='Systolic BP', color='purple', marker='o', markersize=4, linewidth=0.2)
    plt.plot(df['effective_time_frame'], df['diastolic_blood_pressure'].apply(lambda x: x['value']), 
             label='Diastolic BP', color='green', marker='o', markersize=4, linewidth=0.2)

    plt.xlabel('Time')
    plt.ylabel('Blood Pressure (mmHg)')
    plt.title('Systolic and Diastolic Blood Pressure Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
```
:::

::: {#726cd9a5-163a-4d79-9e0a-53e7678cf542 .cell .code execution_count="5"}
``` python
# Generate synthetic blood pressure readings
num_readings = 500
readings = generate_blood_pressure_readings(num_readings)
```
:::

:::: {#90964567-09f2-497a-81fd-061fd8bebdfa .cell .code execution_count="6"}
``` python
plot_readings_over_time(readings)
```

::: {.output .display_data}
![](63c5f9516b184ec6c241c7113fe81014720a7f27.png)
:::
::::

::: {#8ab9d2a4-2bb8-45b3-9d68-198bfe257b34 .cell .markdown}
## Data from Open mHealth web-visualizations

A javascript visualization at
<https://jsfiddle.net/jasperspeicher/dremvboo/> (via
<https://github.com/openmhealth/web-visualizations>) contains some
example data. Let\'s render that data too.
:::

::: {#9f0149cd-c263-4c30-baea-9be1d60cfd24 .cell .code execution_count="7"}
``` python
jasper_speicher_data_url = 'https://gist.githubusercontent.com/jasperSpeicher/3a6af8226182880d75d2/raw/1yr.json'
```
:::

::: {#60dcca27-be6d-469c-9dad-2ee2280ef431 .cell .code execution_count="8"}
``` python
import requests
```
:::

::: {#e9d23a20-cd76-4646-b3ef-8fcaed588459 .cell .code execution_count="9"}
``` python
r = requests.get(jasper_speicher_data_url)
jasper_speicher_data = r.json()
```
:::

::: {#9c2f6f6a-65c6-4f74-aad8-f0a7a87ef74e .cell .code execution_count="10"}
``` python
filtered_data = [item['body'] for item in jasper_speicher_data 
                 if 'body' in item 
                 and 'effective_time_frame' in item['body'] 
                 and 'systolic_blood_pressure' in item['body'] 
                 and 'diastolic_blood_pressure' in item['body']]
```
:::

:::: {#a1278787-79cd-48b3-a0ce-eb9da0a40167 .cell .code execution_count="11"}
``` python
plot_readings_over_time(filtered_data)
```

::: {.output .display_data}
![](86fed95ba34f06daa1d33acdce596490883afc0c.png)
:::
::::
