import pandas as pd

file_path = r"C:\Users\javier_guillen\Downloads\marketplace\marketplace_dashboard\Data\productos.xlsx"

def cargar_datos():
    return pd.read_excel(file_path, engine="openpyxl")
