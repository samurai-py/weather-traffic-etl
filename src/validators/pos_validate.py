import great_expectations as ge
import pandas as pd

def run_pos_validate():
    # Carregue seu DataFrame
    df = pd.read_csv('../../data/transformed_data.csv')

    df_ge = ge.from_pandas(df)

    cols = ['name', 'region', 'country', 'lat', 'lon', 'tz_id', 'localtime', 'last_updated']

    for col in cols:
        try:
            df_ge.expect_column_values_to_not_be_null(col)
        except ge.exceptions.ExpectationSuiteValidationFailedError as e:
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
    run_pos_validate()
