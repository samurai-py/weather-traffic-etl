import itertools
import requests
import pandas as pd
from datetime import datetime
import os

DIRECTIONS_API_KEY = os.environ.get('DIRECTIONS_API_KEY')

def get_directions(dataframe=None, num_cities=None):
    cities_data_filtered = dataframe[:num_cities]

    all_directions = list(itertools.combinations(cities_data_filtered['nome'], 2))
    directions_df = pd.DataFrame(all_directions, columns=['origin', 'destination'])
    
    # Adiciona as combinações inversas
    inverse_directions = pd.DataFrame(directions_df[['destination', 'origin']].values, columns=['origin', 'destination'])
    all_directions_df = pd.concat([directions_df, inverse_directions], ignore_index=True)

    durations = []
    distances = []
    current_times = []
    origins = []
    destinations = []

    for index, row in all_directions_df.iterrows():
        origin_name = row['origin']
        destination_name = row['destination']

        origin_lat_lon = dataframe.loc[dataframe['nome'] == origin_name, 'lat_lon'].values[0]
        destination_lat_lon = dataframe.loc[dataframe['nome'] == destination_name, 'lat_lon'].values[0]

        base_url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin_lat_lon,
            "destination": destination_lat_lon,
            "key": DIRECTIONS_API_KEY,
            "language": 'pt-BR'
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if data['status'] == 'OK':
            duration = data['routes'][0]['legs'][0]['duration']['text']
            distance = data['routes'][0]['legs'][0]['distance']['text']
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            durations.append(duration)
            distances.append(distance)
            current_times.append(current_time)
            origins.append(origin_name)
            destinations.append(destination_name)
        else:
            print(f"Erro na solicitação para rota {origin_name} -> {destination_name}: {data['status']}")
            durations.append(None)
            distances.append(None)
            current_times.append(None)
            origins.append(None)
            destinations.append(None)

    all_directions_df['duration'] = durations
    all_directions_df['distance'] = distances
    all_directions_df['current_time'] = current_times
    all_directions_df['origin'] = origins
    all_directions_df['destination'] = destinations

    return all_directions_df
