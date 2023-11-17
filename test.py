import csv
from datetime import datetime
from src.etl.operators.loaders.mapper.mapper import Records

def read_records_data_from_csv():
    try:
        records_data = []

        with open('data/records.csv', 'r') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                records_data.append(Records.from_csv(row))

        return records_data

    except Exception as e:
        return f"Erro durante a leitura de dados de records: {str(e)}"


def insert_data_into_records_table(data):
    try:
        # Inicializa uma lista para armazenar as instruções SQL
        sql_statements = []

        # Itera sobre as instâncias de Records e gera instruções SQL
        for record in data:
            sql = f"INSERT INTO records (uuid, created_at, updated_at) " \
                  f"VALUES ({record.uuid}, '{record.created_at.strftime('%Y-%m-%d %H:%M:%S')}', " \
                  f"'{record.updated_at.strftime('%Y-%m-%d %H:%M:%S')}');"

            # Adiciona a instrução SQL à lista
            sql_statements.append(sql)

        # Retorna a lista de instruções SQL como uma única string
        return '\n'.join(sql_statements)

    except Exception as e:
        return f"Erro durante a inserção de dados em records: {str(e)}"

# Testar a função
records = read_records_data_from_csv()

# Exemplo de como acessar os atributos de uma instância
for record in records:
    print(f"UUID: {record.uuid}, Created At: {record.created_at}, Updated At: {record.updated_at}")

# Teste a função
sql_string_records = insert_data_into_records_table(records)

# Imprime a string resultante
print(sql_string_records)

