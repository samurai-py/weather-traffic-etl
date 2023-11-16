-- create_tables.sql

CREATE TABLE IF NOT EXISTS location (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    region VARCHAR(100),
    country VARCHAR(100),
    lat FLOAT,
    lon FLOAT,
    tz_id VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS weather (
    id INT PRIMARY KEY,
    record_id BIGINT REFERENCES records(id),
    location_id INT REFERENCES location(id),
    condition VARCHAR(100),
    temp_c FLOAT,
    temp_f FLOAT,
    is_day FLOAT,
    wind_mph FLOAT,
    pressure_mb FLOAT,
    precip_mm FLOAT,
    humidity FLOAT,
    cloud FLOAT,
    feelslike_c FLOAT,
    feelslike_f FLOAT,
    localtime TIMESTAMP,
    last_updated TIMESTAMP
);

CREATE TABLE IF NOT EXISTS directions (
    id INT PRIMARY KEY,
    record_id BIGINT REFERENCES records(id),
    origin_id INT REFERENCES location(id),
    destination_id INT REFERENCES location(id),
    distance FLOAT,
    trip_long VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS records (
    id BIGINT PRIMARY KEY,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
