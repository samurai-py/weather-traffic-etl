import pandas as pd
from operators.transformers.weather import weather_transform
from operators.transformers.directions import directions_transform

def run_transform(weather_output_path='../../data/weather_cleaned_data.csv', directions_output_path='../../data/directions_cleaned_data.csv'):
    try:
        
        weather_result = weather_transform()
        directions_result = directions_transform()
        
        # Salve o DataFrame em um arquivo CSV
        weather_result.to_csv(weather_output_path, index=False)      
        directions_result.to_csv(directions_output_path, index=False)    
        
        return weather_output_path, directions_output_path
        
    except Exception as e:
        return f"Erro durante a transformação: {str(e)}"

if __name__ == "__main__":
    run_transform()
