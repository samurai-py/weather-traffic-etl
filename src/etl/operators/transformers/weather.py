import pandas as pd
from unidecode import unidecode

def weather_transform():
    try:
        df = pd.read_csv('../../data/weather_raw_data.csv')
        df['localtime'] = pd.to_datetime(df['localtime'])
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        df = df.drop(columns=['condition', 'name'], axis=1)

        df.rename(columns={'text': 'condition',
                           'real_city_name': 'name'}, inplace=True)
        result = df[['name', 'region', 'country','lat', 'lon', 'tz_id','condition','temp_c', 'temp_f',
            'is_day', 'wind_mph', 'pressure_mb', 'precip_mm', 'humidity', 'cloud', 'feelslike_c', 'feelslike_f',
            'localtime', 'last_updated']]
        
        result['name_normalized'] = result['name'].apply(unidecode)

        # Removendo duplicatas no DataFrame final
        result.drop_duplicates(inplace=True)
        result.reset_index(drop=True, inplace=True)
        
        return result
        
    except Exception as e:
        return f"Erro durante a transformação: {str(e)}"