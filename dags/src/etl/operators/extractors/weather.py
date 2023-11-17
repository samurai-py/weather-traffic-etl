import requests
import pandas as pd

WEATHER_API_KEY = "eacb618dcb074af4b3c203226230701"

def weather_request(url):
    request = requests.get(url)
    return pd.read_json(request.text)

def pipeline_weather(weather_data):
    temp_location = pd.DataFrame(weather_data['location'][~weather_data['location'].isnull()]).transpose()
    temp_weather = pd.DataFrame(weather_data['current'][~weather_data['current'].isnull()]).transpose()

    result = pd.concat([temp_location, temp_weather], axis=1)
    result.ffill(inplace=True)
    result.bfill(inplace=True)

    return result

def get_weather(dataframe=None, list_names=None):
    
    if (dataframe is not None) and (list_names is not None):
        
        final_result = pd.DataFrame()
        
        for lat_lon in list_names:
            try:
                weather_url = f'https://api.weatherapi.com/v1/current.json?q={lat_lon}&key={WEATHER_API_KEY}&lang=pt_br'
                weather_data = weather_request(weather_url)
                city_result = pipeline_weather(weather_data)
                
                # Adicione o nome real da cidade ao DataFrame city_result
                city_result['real_city_name'] = dataframe.loc[dataframe['lat_lon'] == lat_lon, 'nome'].values[0]
                
                final_result = pd.concat([final_result, city_result])
            except Exception as err:
                print(f'Erro ao obter dados meteorológicos para {lat_lon}: {err}')
                
        df = final_result.copy()
        print(df)
        normalized_df = pd.json_normalize(df['condition'])
        # Combinando o DataFrame resultante com o DataFrame original
        weather_result = pd.concat([df.reset_index(drop=True), normalized_df.ffill().bfill().reset_index(drop=True)], axis=1)
        
        return weather_result
    
    else:
        # Faça algo quando dataframe ou list_names for None
        return pd.DataFrame()  # Ou retorne o que for apropriado no seu caso
    