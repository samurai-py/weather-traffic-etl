import itertools
import requests
import pandas as pd
from datetime import datetime

GOOGLE_API_KEY = "AIzaSyDV-Nxv9OjWLs0eDrtEfEp_vQCm72XjJ84"

def get_routes(dataframe=None, num_cities=None):
    cities_data_filtered = dataframe[:num_cities]

    all_routes = list(itertools.combinations(cities_data_filtered['nome'], 2))
    routes_df = pd.DataFrame(all_routes, columns=['origin', 'destination'])
    
    # Adiciona as combinações inversas
    inverse_routes = pd.DataFrame(routes_df[['destination', 'origin']].values, columns=['origin', 'destination'])
    all_routes_df = pd.concat([routes_df, inverse_routes], ignore_index=True)

    durations = []
    distances = []
    current_times = []
    origins = []
    destinations = []

    for index, row in all_routes_df.iterrows():
        origin_name = row['origin']
        destination_name = row['destination']

        origin_lat_lon = dataframe.loc[dataframe['nome'] == origin_name, 'lat_lon'].values[0]
        destination_lat_lon = dataframe.loc[dataframe['nome'] == destination_name, 'lat_lon'].values[0]

        base_url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin_lat_lon,
            "destination": destination_lat_lon,
            "key": GOOGLE_API_KEY,
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

    all_routes_df['duration'] = durations
    all_routes_df['distance'] = distances
    all_routes_df['current_time'] = current_times
    all_routes_df['origin'] = origins
    all_routes_df['destination'] = destinations

    return all_routes_df
