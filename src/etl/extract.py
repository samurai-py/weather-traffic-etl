import os
import requests
import pandas as pd
from datetime import datetime

WEATHER_API_KEY = "eacb618dcb074af4b3c203226230701"
GOOGLE_API_KEY = "AIzaSyDV-Nxv9OjWLs0eDrtEfEp_vQCm72XjJ84"

def get_weather(url):
    request = requests.get(url)
    return pd.read_json(request.text)

def pipeline_weather(weather_data):
    temp_location = pd.DataFrame(weather_data['location'][~weather_data['location'].isnull()]).transpose()
    temp_weather = pd.DataFrame(weather_data['current'][~weather_data['current'].isnull()]).transpose()

    result = pd.concat([temp_location, temp_weather], axis=1)
    result.ffill(inplace=True)
    result.bfill(inplace=True)

    return result

def get_routes(origin, destination):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_API_KEY,
        "language": 'pt-BR'
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        duration = data['routes'][0]['legs'][0]['duration']['text']
        distance = data['routes'][0]['legs'][0]['distance']['text']
        current_time = datetime.now()
        print(f"Tempo estimado de viagem: {duration}")
        print(f"Distância: {distance}")
        print(f"Hora Local: {current_time}")
    else:
        print(f"Erro na solicitação: {data['status']}")

def run_extract(output_path='../../data/raw_data.csv'):
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, '../../data/municipios.csv')
    
    municipios_df = pd.read_csv(csv_path)

    # Criar as strings 'lat,lon' e armazená-las na lista cities_data
    cities_data = municipios_df.apply(lambda row: f"{row['latitude']},{row['longitude']}" if not pd.isnull(row['latitude']) else None, axis=1).tolist()

    final_result = pd.DataFrame()

    for lat_lon in cities_data:
        try:
            weather_url = f'https://api.weatherapi.com/v1/current.json?q={lat_lon}&key={WEATHER_API_KEY}&lang=pt_br'
            weather_data = get_weather(weather_url)
            city_result = pipeline_weather(weather_data)
            final_result = pd.concat([final_result, city_result])
        except Exception as err:
            print(f'Erro ao obter dados meteorológicos para {lat_lon}: {err}')

    df = final_result.copy()
    normalized_df = pd.json_normalize(df['condition'])
    # Combinando o DataFrame resultante com o DataFrame original
    result_df = pd.concat([df.reset_index(drop=True), normalized_df.ffill().bfill().reset_index(drop=True)], axis=1)


    # Removendo a coluna original 'condition'
    result_df = result_df.drop('condition', axis=1)

    result_df.rename(columns={'text': 'condition'}, inplace=True)
    final_df = result_df[['name', 'region', 'country','lat', 'lon', 'tz_id','condition','temp_c', 'temp_f',
           'is_day', 'wind_mph', 'pressure_mb', 'precip_mm', 'humidity', 'cloud', 'feelslike_c', 'feelslike_f',
           'localtime', 'last_updated']]

    # Removendo duplicatas no DataFrame final
    final_df.drop_duplicates(inplace=True)
    final_df.reset_index(drop=True, inplace=True)
    print(final_df)
    
    print(final_df.columns)

    print(final_df.info())
    
    # Exemplo de uso para as coordenadas de São Paulo e Rio de Janeiro
    origin = f"{final_df['lat'].iloc[0]},{final_df['lon'].iloc[0]}"
    destination = f"{final_df['lat'].iloc[1]},{final_df['lon'].iloc[1]}"
    
    get_routes(origin, destination)
    
    final_df.to_csv(output_path, index=False)        
    return output_path

if __name__ == "__main__":
    run_extract()
