import os

import pandas as pd


SRC_PATH = os.environ.get("SRC_PATH")

def directions_transform():
    try:
        
        # Leitura do CSV dos municípios
        df_municipios = pd.read_csv(f'{SRC_PATH}/municipios.csv')
        
        # Leitura do CSV das direções
        df_directions = pd.read_csv(f'{SRC_PATH}/directions_raw_data.csv')
        
        df_directions['current_time'] = pd.to_datetime(df_directions['current_time'])
        
        # Criação de uma cópia do DataFrame
        result = df_directions.copy()

        # Normalização de nomes
        result['origin_name_normalized'] = result['origin'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        result['destination_name_normalized'] = result['destination'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        
        # Substituição de vírgulas por pontos na coluna 'distance'
        result['distance'] = result['distance'].str.replace(',', '.')

        # Remoção de duplicatas
        result.drop_duplicates(inplace=True)
        result.reset_index(drop=True, inplace=True)

        # Mapeamento do nome da origem para o código IBGE
        result = result.merge(df_municipios[['nome', 'codigo_ibge']],
                              left_on='origin', right_on='nome', how='left')
        result = result.rename(columns={'codigo_ibge': 'origin_id'})

        # Mapeamento do nome do destino para o código IBGE
        result = result.merge(df_municipios[['nome', 'codigo_ibge']],
                              left_on='destination', right_on='nome', how='left')
        result = result.rename(columns={'codigo_ibge': 'destination_id'})

        # Remoção de colunas desnecessárias
        result = result.drop(['nome_x', 'nome_y'], axis=1)

        return result

    except Exception as e:
        return f"Erro durante a transformação: {str(e)}"
