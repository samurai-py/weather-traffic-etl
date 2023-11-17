import great_expectations as ge
import pandas as pd

from src.validators.validation_assets.read_json import read_json_file

def run_pos_validate(file_path, cols_json, cities_json, name_normalized_cols=None):

    # Carregue seu DataFrame
    df = pd.read_csv(file_path)

    df_ge = ge.from_pandas(df)

    # Ler os arquivos JSON
    cols_data = read_json_file(cols_json)
    cities_data = read_json_file(cities_json)

    cols = cols_data['cols']
    cities_names = cities_data['cities_names']

    for col in cols:
        try:
            df_ge.expect_column_values_to_not_be_null(col)
        except ge.exceptions.DataContextError as e:
            print(f"As expectativas para a coluna <{col}> não foram atendidas. Detalhes:")
            print(e)

    if name_normalized_cols:
        for name_normalized_col in name_normalized_cols:
            try:
                df_ge.expect_column_values_to_not_be_null(name_normalized_col)
            except ge.exceptions.DataContextError as e:
                print(f"As expectativas para a coluna <{name_normalized_col}> não foram atendidas. Detalhes:")
                print(e)

            try:
                # Verificar se os valores normalizados na coluna 'name' estão na lista normalizada 'normalized_cities_names'
                df_ge.expect_column_values_to_be_in_set(name_normalized_col, value_set=cities_names)
            except ge.exceptions.DataContextError as e:
                print(f"As expectativas para a coluna '{name_normalized_col}' não foram atendidas. Detalhes:")
                print(e)

    # Remover a coluna 'name_normalized' se existir
    if 'name_normalized' in df.columns:
        df = df.drop(columns=['name_normalized'])

    # Obtenha os resultados da validação
    results = df_ge.validate()

    if not results["success"]:
        print("As expectativas não foram atendidas. Detalhes:")
        print(results["results"])
        raise ValueError("As expectativas não foram atendidas.")

    print(f"As expectativas para {file_path} foram atendidas com sucesso!")

if __name__ == "__main__":
    # Modifique os caminhos dos arquivos e do JSON conforme necessário
    run_pos_validate(file_path='/usr/local/airflow/dags/src/data/weather_cleaned_data.csv', cols_json='validation_assets/cols/weather_cols.json', cities_json='validation_assets/cities.json')
    run_pos_validate(file_path='/usr/local/airflow/dags/src/data/directions_cleaned_data.csv', cols_json='validation_assets/cols/directions_cols.json', cities_json='validation_assets/cities.json', name_normalized_cols=['origin_name_normalized', 'destination_name_normalized'])
