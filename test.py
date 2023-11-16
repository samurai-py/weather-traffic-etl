from datetime import datetime
from src.etl.operators.loaders.mapper.mapper import Directions

def read_directions_data_from_csv():
    # Nome do arquivo CSV
    csv_filename = 'data/directions_cleaned_data.csv'

    # Lista para armazenar instâncias da classe Directions
    directions_data = []

    # Lógica para ler dados do CSV para a tabela 'directions'
    with open(csv_filename, 'r', encoding='utf-8') as file:
        # Ignorar cabeçalho
        next(file)

        for line in file:
            # Dividir os dados da linha
            data = line.strip().split(',')

            try:
                # Tentar converter os dados para os tipos corretos
                record_id = int(data[7])
                origin_id = int(data[0])
                destination_id = int(data[1])
                distance = float(data[3])
                trip_long = data[4]
                created_at = datetime.strptime(data[5], "%Y-%m-%d %H:%M:%S")
                updated_at = datetime.strptime(data[6], "%Y-%m-%d %H:%M:%S")

                # Criar instância da classe Directions
                direction = Directions(
                    record_id=record_id,
                    origin_id=origin_id,
                    destination_id=destination_id,
                    distance=distance,
                    trip_long=trip_long,
                    created_at=created_at,
                    updated_at=updated_at
                )

                # Adicionar a instância à lista
                directions_data.append(direction)

            except ValueError as e:
                print(f"Erro ao converter dados: {e}")

    # Retornar a lista de instâncias
    return directions_data

# Restante do código permanece inalterado


def insert_data_into_directions_table(data):
    # Inicializa uma lista para armazenar as instruções SQL
    sql_statements = []

    # Itera sobre as instâncias de Directions e gera instruções SQL
    for direction in data:
        sql = f"INSERT INTO directions (record_id, origin_id, destination_id, distance, trip_long, created_at, updated_at) " \
              f"VALUES ({direction.record_id}, {direction.origin_id}, {direction.destination_id}, " \
              f"{direction.distance}, '{direction.trip_long}', '{direction.created_at.strftime('%Y-%m-%d %H:%M:%S')}', " \
              f"'{direction.updated_at.strftime('%Y-%m-%d %H:%M:%S')}');"
        
        # Adiciona a instrução SQL à lista
        sql_statements.append(sql)

    # Retorna a lista de instruções SQL como uma única string
    return '\n'.join(sql_statements)

# Testar a função
directions_instances = read_directions_data_from_csv()

# Exemplo de como acessar os atributos de uma instância
for direction in directions_instances:
    print(f"Record ID: {direction.record_id}, Origin ID: {direction.origin_id}, Destination ID: {direction.destination_id}, Distance: {direction.distance}, Trip Long: {direction.trip_long}")

# Teste a função
sql_string_directions = insert_data_into_directions_table(directions_instances)

# Imprime a string resultante
print(sql_string_directions)
