import os

import psycopg2

from src.etl.operators.loaders.loader import run_load

def connect_and_insert(table_name):
    # Substitua essas informações de conexão pelo que for relevante para o seu banco de dados Redshift
    connection_params = {
        'host': os.environ.get('REDSHIFT_HOST'),
        'dbname': os.environ.get('REDSHIFT_DBNAME'),
        'user': os.environ.get('REDSHIFT_USER'),
        'password': os.environ.get('REDSHIFT_PASSWORD'),
        'port': int(os.environ.get('REDSHIFT_PORT'))  # Converta a porta para inteiro
    }

    try:
        # Conectar ao banco de dados Redshift
        connection = psycopg2.connect(**connection_params)

        # Criar um cursor
        cursor = connection.cursor()

        # Executar a função run_load para 'records', 'locations', 'weather' e 'directions'
        sql_statements = run_load(table_name)

        # Executar as instruções SQL e fazer commit
        cursor.execute(sql_statements)
        connection.commit()

    except Exception as e:
        print(f"Erro ao conectar ou inserir no banco de dados Redshift: {str(e)}")

    finally:
        # Fechar o cursor e a conexão com o banco de dados, mesmo em caso de exceção
        cursor.close()
        connection.close()

if __name__ == "__main__":
    connect_and_insert(table_name)
