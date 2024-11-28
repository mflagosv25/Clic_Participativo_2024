# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:16:53 2024

@author: mflagosv
"""

import pandas as pd
import re
import sys

# =============================================================================
# def concatenar_columnas(df, columnas, separador= " "):
#     colum_resultante = df[columnas].astype(str).agg(separador.join, axis=1)
#     return colum_resultante
# =============================================================================

def load_data(file_path):
    # =============================================================================
    # Columnas Obligatorias: 'Es_IRPC','Año','Tipo','Numero','Objeto','Secretarias',
    #                        'tipo_secretaria','Instancia_ID', "Sector_administrativo", 
    #                         "Sector_poblacional","Estado", "Actores", "Alcances", 
    #                         "Funciones", "Categoria"
    # =============================================================================
    if not file_path:
        sys.exit("No se cargó el archivo de entrada\nEjecute nuevamente, y cargue un archivo válido")
    nombre_archivo = list(file_path.keys())[0]
    df = pd.read_excel(nombre_archivo)
    return df

def concat_columns(registro):
    #'Tipo','Numero','de','Año','guion','Objeto'
    tipo = str(registro['Tipo'])
    numero = str(registro['Numero'])
    anio = str(registro['Año'])
    objeto = str(registro['Objeto'])
    new_colum = tipo + " " + numero + " de " + anio + " - " + objeto
    return new_colum

def reemp_enum(column):
    # Reemplazar enumeraciones por ';' en la columna 'Actores'
    new_colum = str(column).lower()
    patt1 = r'\b\d+\.'
    patt2 = r'\b(?:i{1,3}|iv|v{1,3}|ix|x{1,3})\.'
    patt3 = r'\b[a-z]\)'
    patt4 = r'\b[a-z]\.'
    patt5 = r'\b\d+\.\d+\b'
    l_patt = [patt1,patt2,patt3,patt4,patt5]
    for patt in l_patt:
         new_colum = re.sub(patt,';',new_colum)
    return new_colum

def remov_enum(column):
    # Remover enumeraciones de 'Actores'
    new_colum = str(column).lower()
    patt0= r'\d+\.\s*'
    patt1 = r'\b[a-z]\)'
    patt2 = r'\b[a-z]\.'
    patt3 = r'\b\d+\.\d+\.'
    patt4 = r'\b(?:i{1,3}|iv|v{1,3}|ix|x{1,3})\.'
    l_patt = [patt0,patt1,patt2,patt3,patt4]
    for i in range(len(l_patt)):
        if i == 2:
            new_colum = re.sub(l_patt[i],';',new_colum)
        else:
            new_colum = re.sub(l_patt[i],'',new_colum)
    return new_colum

def get_instancias(df):
    print("Obteniendo los registros para Instancias ...")
    instancias = df[df['Es_IRPC'] == "Si"].copy()
    # Convertir texto a minúsculas y eliminar acentos
    instancias = instancias.applymap(lambda x: str(x).lower() if isinstance(x, str) else x)
    # Modificar columna 'Norma' para tener un formato específico
    instancias['Norma'] = instancias[['Tipo','Numero','Año','Objeto']].apply(concat_columns,axis=1)
    # Rellenar valores nulos en columnas específicas
    instancias['Secretarias'].fillna("Sin secretaria", inplace=True)
    instancias['tipo_secretaria'].fillna("Sin secretaria", inplace=True)
    instancias['Instancia_ID'] = instancias['Instancia_ID'].apply(lambda x: str(x).upper())
    # Aplicar formato de mayúsculas a columnas específicas
    columns = ["Instancia", "Epigrafe", "Norma", "Objeto", "Sector_administrativo", 
               "Sector_poblacional", "Estado", "Secretarias", "tipo_secretaria",
               "Actores", "Alcances", "Funciones", "Categoria"]
    instancias[columns] = instancias[columns].applymap(lambda x: str(x).capitalize())
    return instancias

def get_funciones(instancias):
    print("Obteniendo los registros para Funciones ...")
    # Seleccionar las columnas necesarias y separar por el símbolo '-'
    funciones = instancias[["Instancia", "Instancia_ID", "Funciones"]].copy()
    funciones['Funciones'] = funciones['Funciones'].str.split('-')
    funciones = funciones.explode('Funciones')
    funciones['Funciones'] = funciones['Funciones'].str.strip()
    funciones['Funciones'] = funciones['Funciones'].apply(lambda x: str(x).replace("\n"," "))
    funciones.dropna(subset=['Funciones'], inplace=True)
    return funciones

def get_actores(instancias):
    print("Obteniendo los registros para Actores ...")
    actores = instancias[["Instancia", "Instancia_ID", "Actores"]].copy()
    # Reemplazar enumeraciones por ';' en la columna 'Actores'
    actores['Actores'] = actores['Actores'].apply(reemp_enum)
    # Limpiar y separar actores en filas individuales por '-' (o por ';'?)
    actores['Actores'] = actores['Actores'].str.replace(';;', ';')
    actores = actores.assign(Actores=actores['Actores'].str.split(';')).explode('Actores')
    #actores = actores.assign(Actores=actores['Actores'].str.split('-')).explode('Actores')
    actores['Actores'] = actores['Actores'].str.strip()
    actores = actores[~actores['Actores'].isna() & ~actores['Actores'].str.match(r'^[[:punct:][:space:]]*$')]
    # Remover enumeraciones de 'Actores'
    actores['Actores'] = actores['Actores'].apply(remov_enum)
    return actores

def get_secretarias(instancias):
    print("Obteniendo los registros para Secretarias ...")
    secretarias = instancias[["Instancia", "Instancia_ID", "tipo_secretaria", "Secretarias"]].copy()
    secretarias = secretarias.assign(Secretarias=secretarias['Secretarias'].str.split(',')).explode('Secretarias')
    secretarias['Secretarias'] = secretarias['Secretarias'].str.strip()
    secretarias['Secretarias'].fillna("Sin secretaria", inplace=True)
    secretarias['tipo_secretaria'].fillna("Sin secretaria", inplace=True)
    return secretarias

#%%
if __name__ == "__main__":
    # Leer el archivo Excel
    file_path = ".\\Datos_Entrada\\Instancias_ent.xlsx"
    formato_act = load_data(file_path)
    # ------------------ Instancias ---------------------
    instancias = get_instancias(formato_act)
    # ------------------ Funciones ---------------------
    funciones = get_funciones(instancias)
    #------------------- Actores ----------------------
    actores = get_actores(instancias)
    # ----------------- Secretarias ----------------------
    secretarias = get_secretarias(instancias)

#%% ----------------- Guardar ----------------------

# =============================================================================
# funciones.to_excel("funciones.xlsx", index=False)
# actores.to_excel("actores.xlsx", index=False)
# secretarias.to_excel("secretarias.xlsx", index=False)
# instancias.to_excel("Instancias.xlsx", index=False)
# =============================================================================
