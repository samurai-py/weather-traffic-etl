import pandas as pd
from unidecode import unidecode

def directions_transform():
    try:
        df = pd.read_csv('../../data/directions_raw_data.csv')
        df['current_time'] = pd.to_datetime(df['current_time'])
        
        result = df.copy()
        
        result['origin_name_normalized'] = result['origin'].apply(unidecode)
        result['destination_name_normalized'] = result['destination'].apply(unidecode)

        # Removendo duplicatas no DataFrame final
        result.drop_duplicates(inplace=True)
        result.reset_index(drop=True, inplace=True)
        
        return result
        
    except Exception as e:
        return f"Erro durante a transformação: {str(e)}"