import pandas as pd

def run_transform(output_path='../../data/transformed_data.csv'):
    try:
        df = pd.read_csv('../../data/transformed_data.csv')
        df['localtime'] = pd.to_datetime(df['localtime'])
        df['last_updated'] = pd.to_datetime(df['last_updated'])
        
        # Salve o DataFrame em um arquivo CSV
        df.to_csv(output_path, index=False)        
        return output_path
        
    except Exception as e:
        return f"Erro durante a transformação: {str(e)}"

if __name__ == "__main__":
    run_transform()
