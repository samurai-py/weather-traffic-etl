from operators.loaders.mapper.mapper import Location, Weather, Directions, Records
from operators.loaders.database.database import Column, Table

def run_load(table_name):
    
    # Crie as tabelas se não existirem
    db.create_tables()

    # Nome da tabela fornecido como parâmetro
    if table_name == 'locations':
        data = read_location_data_from_csv()  # Substitua por sua lógica de leitura de dados do CSV
        insert_data_into_location_table(data)
    elif table_name == 'weather':
        data = read_weather_data_from_csv()  # Substitua por sua lógica de leitura de dados do CSV
        insert_data_into_weather_table(data)
    elif table_name == 'directions':
        data = read_directions_data_from_csv()  # Substitua por sua lógica de leitura de dados do CSV
        insert_data_into_directions_table(data)
    elif table_name == 'records':
        data = read_records_data_from_csv()  # Substitua por sua lógica de leitura de dados do CSV
        insert_data_into_records_table(data)
    else:
        print("Tabela não reconhecida.")

def read_location_data_from_csv():
      # Nome do arquivo CSV
    csv_filename = '../../data/weather_cleaned_data.csv'

    # Lista para armazenar instâncias da classe Location
    locations = []

    # Lógica para ler dados do CSV para a tabela 'location'
    with open(csv_filename, 'r', encoding='utf-8') as file:
        # Ignorar cabeçalho
        next(file)

        for line in file:
            # Dividir os dados da linha
            data = line.strip().split(',')

            # Criar instância da classe Location
            location = Location(
                name=data[0],
                region=data[1],
                country=data[2],
                lat=float(data[3]),
                lon=float(data[4]),
                tz_id=data[5]
            )

            # Adicionar a instância à lista
            locations.append(location)

    # Retornar a lista de instâncias
    return locations

def insert_data_into_location_table(data):
    # Inicializa uma lista para armazenar as instruções SQL
    sql_statements = []

    # Itera sobre as instâncias de Location e gera instruções SQL
    for location in data:
        sql = f"INSERT INTO locations (name, region, country, lat, lon, tz_id) VALUES ('{location.name}', '{location.region}', '{location.country}', {location.lat}, {location.lon}, '{location.tz_id}');"
        
        # Adiciona a instrução SQL à lista
        sql_statements.append(sql)

    # Retorna a lista de instruções SQL como uma única string
    return '\n'.join(sql_statements)

def read_weather_data_from_csv():
    # Nome do arquivo CSV
    csv_filename = 'data/weather_cleaned_data.csv'

    # Lista para armazenar instâncias da classe Weather
    weather_data = []

    # Lógica para ler dados do CSV para a tabela 'weather'
    with open(csv_filename, 'r', encoding='utf-8') as file:
        # Ignorar cabeçalho
        next(file)

        for line in file:
            # Dividir os dados da linha
            data = line.strip().split(',')

            # Criar instância da classe Weather
            weather = Weather(
                name=data[0],
                condition=data[6],
                temp_c=float(data[7]),
                temp_f=float(data[8]),
                is_day=float(data[9]),
                wind_mph=float(data[10]),
                pressure_mb=float(data[11]),
                precip_mm=float(data[12]),
                humidity=float(data[13]),
                cloud=float(data[14]),
                feelslike_c=float(data[15]),
                feelslike_f=float(data[16]),
                created_at=datetime.strptime(data[17], "%Y-%m-%d %H:%M:%S"),
                updated_at=datetime.strptime(data[18], "%Y-%m-%d %H:%M:%S")
            )

            # Adicionar a instância à lista
            weather_data.append(weather)

    # Retornar a lista de instâncias
    return weather_data

def insert_data_into_weather_table(data):
    # Inicializa uma lista para armazenar as instruções SQL
    sql_statements = []

    # Itera sobre as instâncias de Weather e gera instruções SQL
    for weather in data:
        sql = f"INSERT INTO weather (name, condition, temp_c, temp_f, is_day, wind_mph, pressure_mb, precip_mm, humidity, cloud, feelslike_c, feelslike_f, created_at, updated_at) VALUES ('{weather.name}', '{weather.condition}', {weather.temp_c}, {weather.temp_f}, {weather.is_day}, {weather.wind_mph}, {weather.pressure_mb}, {weather.precip_mm}, {weather.humidity}, {weather.cloud}, {weather.feelslike_c}, {weather.feelslike_f}, '{weather.created_at}', '{weather.updated_at}');"
        
        # Adiciona a instrução SQL à lista
        sql_statements.append(sql)

    # Retorna a lista de instruções SQL como uma única string
    return '\n'.join(sql_statements)

def read_directions_data_from_csv():
    # Lógica para ler dados do CSV para a tabela 'directions'
    pass

def insert_data_into_directions_table(data):
    # Lógica para inserir dados na tabela 'directions'
    pass

def read_records_data_from_csv():
    # Lógica para ler dados do CSV para a tabela 'records'
    pass

def insert_data_into_records_table(data):
    # Lógica para inserir dados na tabela 'records'
    pass
