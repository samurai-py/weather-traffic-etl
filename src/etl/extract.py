import os
import requests
import pandas as pd
from datetime import datetime

from operators.extractors.weather import get_weather
from operators.extractors.directions import get_directions

def run_extract(weather_output_path='../../data/weather_raw_data.csv', directions_output_path='../../data/directions_raw_data.csv'):
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '../../data/municipios.csv')
    
    cities_df = pd.read_csv(csv_path)

    # Criar as strings 'lat,lon' e armazená-las na lista cities_data
    cities_df['lat_lon'] = cities_df.apply(lambda row: f"{row['latitude']},{row['longitude']}" if not pd.isnull(row['latitude']) else None, axis=1)
    cities_data = cities_df['lat_lon'].tolist()

    # Criar DataFrame com todas as rotas possíveis
    weather_result = get_weather(dataframe=cities_df, list_names=cities_data)
    directions_result = get_directions(dataframe=cities_df, num_cities=3)
    
    weather_result.to_csv(weather_output_path, index=False)   
    
    # Salvar o DataFrame das rotas em um arquivo CSV
    directions_result.to_csv(directions_output_path, index=False)     
    
    return weather_output_path, directions_output_path

if __name__ == "__main__":
    run_extract()
