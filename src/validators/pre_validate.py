import great_expectations as ge
import pandas as pd

from validation_assets.read_json import read_json_file

def run_pre_validate(file_path, validation_cols_json):
    # Carregue seu DataFrame
    df = pd.read_csv(file_path)

    df_ge = ge.from_pandas(df)

    cols_data = read_json_file(validation_cols_json)

    cols = cols_data['cols']

    for col in cols:
        try:
            df_ge.expect_column_values_to_not_be_null(col)
        except ge.exceptions.DataContextError as e:
            print(f"As expectativas para a coluna <{col}> não foram atendidas. Detalhes:")
            print(e)

    # Obtenha os resultados da validação
    results = df_ge.validate()

    if not results["success"]:
        print("As expectativas não foram atendidas. Detalhes:")
        print(results["results"])
        raise ValueError("As expectativas não foram atendidas.")

    print("As expectativas foram atendidas com sucesso!")

    return print(results['success'])

if __name__ == "__main__":
    # Modifique os caminhos dos arquivos e do JSON conforme necessário
    run_pre_validate(file_path='../../data/weather_raw_data.csv', validation_cols_json='validation_assets/cols/weather_cols.json')
    run_pre_validate(file_path='../../data/routes_raw_data.csv', validation_cols_json='validation_assets/cols/routes_cols.json')
