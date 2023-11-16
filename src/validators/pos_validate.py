import great_expectations as ge
import pandas as pd

from validation_assets.read_json import read_json_file

def run_pos_validate():
    # Carregue seu DataFrame
    df = pd.read_csv('../../data/transformed_data.csv')

    df_ge = ge.from_pandas(df)

    # Ler os arquivos JSON
    cities_data = read_json_file('validation_assets/cities.json')
    cols_data = read_json_file('validation_assets/cols.json')

    cols = cols_data['cols']
    cities_names = cities_data['cities_names']

    for col in cols:
        try:
            df_ge.expect_column_values_to_not_be_null(col)
        except ge.exceptions.DataContextError as e:
            print(f"As expectativas para a coluna <{col}> não foram atendidas. Detalhes:")
            print(e)

    try:
        # Verificar se os valores normalizados na coluna 'name' estão na lista normalizada 'normalized_cities_names'
        df_ge.expect_column_values_to_be_in_set('name_normalized', value_set=cities_names)
    except ge.exceptions.DataContextError as e:
        print(f"As expectativas para a coluna 'name' não foram atendidas. Detalhes:")
        print(e)

    # Remover a coluna 'name_normalized'
    df = df.drop(columns=['name_normalized'])

    # Obtenha os resultados da validação
    results = df_ge.validate()

    if not results["success"]:
        print("As expectativas não foram atendidas. Detalhes:")
        print(results["results"])
        raise ValueError("As expectativas não foram atendidas.")

    print("As expectativas foram atendidas com sucesso!")

    return print(results['success'])

if __name__ == "__main__":
    run_pos_validate()
