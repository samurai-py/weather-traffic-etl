import os

import pandas as pd
import uuid

from src.etl.operators.transformers.weather import weather_transform
from src.etl.operators.transformers.directions import directions_transform


SRC_PATH = os.environ.get("SRC_PATH")

def generate_uuid():
    record_uuid = str(uuid.uuid4())
    
    return record_uuid

def write_records(path=f'{SRC_PATH}/data/records.csv'):
    
    r_uuid = generate_uuid()
    records_data = pd.DataFrame({'uuid': [r_uuid]})
    records_data.to_csv(path, mode='a', header=None, index=True)
    
def read_records(path=f'{SRC_PATH}/data/records.csv'):
    write_records()
    
    records = pd.read_csv(path)
    records_len = len(records['uuid'])
    return records_len    

def run_transform(weather_output_path=f'{SRC_PATH}/data/weather_cleaned_data.csv', directions_output_path=f'{SRC_PATH}/data/directions_cleaned_data.csv'):
        
    records_id = int(read_records())
    
    weather_result = weather_transform()
    weather_result['record_id'] = records_id
    directions_result = directions_transform()
    directions_result['record_id'] = records_id
    
    # Salve o DataFrame em um arquivo CSV
    weather_result.to_csv(weather_output_path, index=False)      
    directions_result.to_csv(directions_output_path, index=False)    
    
    return weather_output_path, directions_output_path

if __name__ == "__main__":
    run_transform()