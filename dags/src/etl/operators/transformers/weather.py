import os

import pandas as pd


SRC_PATH = os.environ.get("SRC_PATH")

def weather_transform():
    try:
        # Carregue o DataFrame dos municípios
        municipios_df = pd.read_csv(f'{SRC_PATH}/data/municipios.csv', encoding='utf-8')
        df = pd.read_csv(f'{SRC_PATH}/data/weather_raw_data.csv')
        df['localtime'] = pd.to_datetime(df['localtime'])
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        df = df.drop(columns=['condition', 'name'], axis=1)

        df.rename(columns={'text': 'condition',
                           'real_city_name': 'name'}, inplace=True)
        result = df[['name', 'region', 'country','lat', 'lon', 'tz_id','condition','temp_c', 'temp_f',
            'is_day', 'wind_mph', 'pressure_mb', 'precip_mm', 'humidity', 'cloud', 'feelslike_c', 'feelslike_f',
            'localtime', 'last_updated']]
        result['name_normalized'] = result['name'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        
        # Faça uma fusão (merge) entre os DataFrames usando a coluna 'name_normalized' e 'nome'
        result = pd.merge(result, municipios_df[['nome', 'codigo_ibge']], left_on='name', right_on='nome', how='left')
        
        # Renomeie a coluna 'cod_ibge' para 'system_id'
        result.rename(columns={'codigo_ibge': 'system_id'}, inplace=True)
        
        # Remova colunas desnecessárias após a fusão
        result.drop(['nome'], axis=1, inplace=True)

        # Removendo duplicatas no DataFrame final
        result.drop_duplicates(inplace=True)
        result.reset_index(drop=True, inplace=True)

        return result
        
    except Exception as e:
        return f"Erro durante a transformação: {str(e)}"