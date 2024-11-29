# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 21:59:25 2024

@author: mflagosv
"""

import pandas as pd
#from openpyxl import Workbook

# Función para guardar DataFrames en un archivo Excel con hojas personalizadas
def save_dataframes(dataframes, sheet_names):
    """
    Guarda múltiples DataFrames en un archivo Excel con nombres personalizados para las hojas.

    :param dataframes: Lista de DataFrames a guardar.
    :param sheet_names: Lista de nombres para las hojas correspondientes a los DataFrames.
    :param file_name: Nombre del archivo Excel (debe incluir extensión .xlsx).
    """
    # Crear un nuevo archivo Excel
    with pd.ExcelWriter('ConsolidadoArchivos.xlsx', engine='openpyxl') as writer:
        for df, sheet_name in zip(dataframes, sheet_names):
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print("Archivo Excel guardado como 'ConsolidadoArchivos.xlsx'.")

if __name__ == "__main__":
    df1 = pd.DataFrame({
        "Nombre": ["Ana", "Luis", "Carlos"],
        "Edad": [25, 30, 35],
        "Ciudad": ["Madrid", "Bogotá", "Santiago"]
    })
     
    df2 = pd.DataFrame({
        "Producto": ["A", "B", "C"],
        "Precio": [100, 200, 300],
        "Cantidad": [10, 15, 20]
    })
    dataframes = [df1,df2]
    sheet_names = ['df1','df2']
    #save_dataframes(dataframes, sheet_names)


    