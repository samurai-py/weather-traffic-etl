
class Column:
    def __init__(self, name, data_type, is_primary_key=False, references=None, default=None):
        self.name = name
        self.data_type = data_type
        self.is_primary_key = is_primary_key
        self.references = references  # Nome da tabela referenciada, se aplicável
        self.default = default

class Table:
    
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns

    def create_table_sql(self):
        # Gera a instrução SQL para criar a tabela
        sql = f"CREATE TABLE IF NOT EXISTS {self.name} (\n"
        for column in self.columns:
            sql += f"    {column.name} {column.data_type}"
            if column.is_primary_key:
                sql += " PRIMARY KEY"
            if column.default:
                sql += f" DEFAULT {column.default}"
            if column.references:
                sql += f" REFERENCES {column.references}"
            sql += ",\n"
        sql = sql.rstrip(",\n") + "\n);"
        return sql

# Defina as colunas para a tabela Location
location_columns = [
    Column(name="id", data_type="INT", is_primary_key=True),
    Column(name="name", data_type="VARCHAR(100)"),
    Column(name="region", data_type="VARCHAR(100)"),
    Column(name="country", data_type="VARCHAR(100)"),
    Column(name="lat", data_type="FLOAT"),
    Column(name="lon", data_type="FLOAT"),
    Column(name="tz_id", data_type="VARCHAR(100)"),
]

# Defina as colunas para a tabela Weather
weather_columns = [
    Column(name="id", data_type="INT", is_primary_key=True),
    Column(name="record_id", data_type="BIGINT", references="records(id)"),
    Column(name="location_id", data_type="INT", references="location(id)"),
    Column(name="condition", data_type="VARCHAR(100)"),
    Column(name="temp_c", data_type="FLOAT"),
    Column(name="temp_f", data_type="FLOAT"),
    Column(name="is_day", data_type="FLOAT"),
    Column(name="wind_mph", data_type="FLOAT"),
    Column(name="pressure_mb", data_type="FLOAT"),
    Column(name="precip_mm", data_type="FLOAT"),
    Column(name="humidity", data_type="FLOAT"),
    Column(name="cloud", data_type="FLOAT"),
    Column(name="feelslike_c", data_type="FLOAT"),
    Column(name="feelslike_f", data_type="FLOAT"),
    Column(name="localtime", data_type="TIMESTAMP"),
    Column(name="last_updated", data_type="TIMESTAMP"),
]

# Defina as colunas para a tabela Directions
directions_columns = [
    Column(name="id", data_type="INT", is_primary_key=True),
    Column(name="record_id", data_type="BIGINT", references="records(id)"),
    Column(name="origin_id", data_type="INT", references="location(id)"),
    Column(name="destination_id", data_type="INT", references="location(id)"),
    Column(name="distance", data_type="FLOAT"),
    Column(name="trip_long", data_type="VARCHAR(100)"),
    Column(name="created_at", data_type="TIMESTAMP"),
    Column(name="updated_at", data_type="TIMESTAMP"),
]

# Defina as colunas para a tabela Records
records_columns = [
    Column(name="id", data_type="BIGINT", is_primary_key=True, default="nextval('records_id_seq'::regclass)"),
    Column(name="uuid", data_type="VARCHAR(36)", default="uuid_generate_v4()"),
    Column(name="created_at", data_type="TIMESTAMP", default="now()"),
    Column(name="updated_at", data_type="TIMESTAMP", default="now()"),
]

# Crie a tabela Location
location_table = Table(name="location", columns=location_columns)
# Crie a tabela Weather
weather_table = Table(name="weather", columns=weather_columns)
# Crie a tabela Directions
directions_table = Table(name="directions", columns=directions_columns)
# Crie a tabela Records
records_table = Table(name="records", columns=records_columns)

# Obter a instrução SQL para criar as tabelas
create_location_table_sql = location_table.create_table_sql()
create_weather_table_sql = weather_table.create_table_sql()
create_directions_table_sql = directions_table.create_table_sql()
create_records_table_sql = records_table.create_table_sql()

print(create_location_table_sql)
print(create_weather_table_sql)
print(create_directions_table_sql)
print(create_records_table_sql)
