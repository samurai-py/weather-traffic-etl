from datetime import datetime


class Records:
    def __init__(self, id, uuid, created_at, updated_at):
        self.id = id
        self.uuid = uuid
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_csv(cls, row):
        return cls(
            id=int(row['id']),
            uuid=int(row['uuid']),
            created_at=datetime.strptime(row['created_at'], "%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.strptime(row['updated_at'], "%Y-%m-%d %H:%M:%S")
        )


class Location:
    def __init__(self, name, region, country, lat, lon, tz_id):
        self.name = name
        self.region = region
        self.country = country
        self.lat = lat
        self.lon = lon
        self.tz_id = tz_id

    @classmethod
    def from_csv(cls, row):
        return cls(
            name=row['name'],
            region=row['region'],
            country=row['country'],
            lat=float(row['lat']),
            lon=float(row['lon']),
            tz_id=row['tz_id']
        )
        
        
class Weather:
    def __init__(self, name, condition, temp_c, temp_f, is_day, wind_mph, pressure_mb, precip_mm, humidity, cloud, feelslike_c, feelslike_f, created_at, updated_at):
        self.name = name
        self.condition = condition
        self.temp_c = temp_c
        self.temp_f = temp_f
        self.is_day = is_day
        self.wind_mph = wind_mph
        self.pressure_mb = pressure_mb
        self.precip_mm = precip_mm
        self.humidity = humidity
        self.cloud = cloud
        self.feelslike_c = feelslike_c
        self.feelslike_f = feelslike_f
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_csv(cls, row):
        return cls(
            name=row['name'],
            condition=row['condition'],
            temp_c=float(row['temp_c']),
            temp_f=float(row['temp_f']),
            is_day=float(row['is_day']),
            wind_mph=float(row['wind_mph']),
            pressure_mb=float(row['pressure_mb']),
            precip_mm=float(row['precip_mm']),
            humidity=float(row['humidity']),
            cloud=float(row['cloud']),
            feelslike_c=float(row['feelslike_c']),
            feelslike_f=float(row['feelslike_f']),
            created_at=datetime.strptime(row['localtime'], "%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.strptime(row['last_updated'], "%Y-%m-%d %H:%M:%S")
        )
        

class Directions:
    def __init__(self, record_id, origin_id, destination_id, distance, trip_long, created_at, updated_at):
        self.record_id = record_id
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.distance = distance
        self.trip_long = trip_long
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_csv(cls, row):
        return cls(
            record_id=int(row['record_id']),
            origin_id=int(row['origin_id']),
            destination_id=int(row['destination_id']),
            distance=float(row['distance']),
            trip_long=row['trip_long'],
            created_at=datetime.strptime(row['created_at'], "%Y-%m-%d %H:%M:%S"),
            updated_at=datetime.strptime(row['updated_at'], "%Y-%m-%d %H:%M:%S")
        )