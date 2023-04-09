import pandas as pd
import os

def read_csv_file(file_path):
    return pd.read_csv(file_path)

def read_excel_file(file_path):
    return pd.read_excel(file_path, engine='openpyxl')

def read_json_file(file_path):
    return pd.read_json(file_path)

def load_data(file_path):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == ".csv":
        return read_csv_file(file_path)
    elif file_extension == ".xlsx":
        return read_excel_file(file_path)
    elif file_extension == ".json":
        return read_json_file(file_path)
    else:
        raise Exception(f"Unsupported file type: {file_extension}")
    
    
    

if __name__ == "__main__":
    # Example usage
    file_path = "your_data_file.csv" # Replace with the path to your data file
    data = load_data(file_path)
    print(data)