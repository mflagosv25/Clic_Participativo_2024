# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 16:17:11 2024

@author: mflagosv
"""
"""
Junta las columnas [Sector_administrativo, Sector_poblacional] en "Sector",
y se diferencian en "Tipo sector: administrativo o poblacional"
Si hay mas de un sector en el registro se separan en independientes con el mismo IDActor
"""
import pandas as pd
import unidecode

def separate_sectors(df_input, columns_input:list, tipo):
    # Separar filas para cada valor de "Sector_poblacional"
    df = df_input[columns_input].copy()
    #Seleccionamos la columna que queremos separar
    column_input = columns_input[1]
    df.dropna(subset=[column_input], inplace=True)
    df['Sector'] = df[column_input].apply(lambda x: str(x).split(","))
    df = df.explode('Sector',ignore_index=True)
    df['Sector'] = df['Sector'].str.strip()
    df['Tipo_sector'] = tipo
    df.drop(columns = column_input, inplace=True)
    return df

def join_tables(df1,df2):
    # UNIR TABLAS POBLACIONAL Y ADMINISTRATIVA
    sector_df = pd.concat([df1,df2])
    sector_df['Sector'] = sector_df['Sector'].str.strip().str.title()
    sector_df['Sector'] = sector_df['Sector'].apply(unidecode.unidecode)
    return sector_df

def get_sector_actores(actores):
    # TABLA POBLACIONAL
    poblacional = separate_sectors(actores,
                                   ['ID_Actor','Sector_poblacional'],
                                   'Poblacional')
    # TABLA ADMINISTRATIVO
    administrativo = separate_sectors(actores,
                                      ['ID_Actor','Sector_administrativo'],
                                      'Administrativo')
    # UNIR TABLAS POBLACIONAL Y ADMINISTRATIVA
    sector_actores = join_tables(poblacional, administrativo)
    return sector_actores

def get_sector_instancias(instancias):
    # TABLA POBLACIONAL
    poblacional_ins = separate_sectors(instancias,
                                   ['Instancia_ID','Sector_poblacional'],
                                   'Poblacional')
    # TABLA ADMINISTRATIVO
    administrativo_ins = separate_sectors(instancias,
                                      ['Instancia_ID','Sector_administrativo'],
                                      'Administrativo')
    # UNIR TABLAS POBLACIONAL Y ADMINISTRATIVA
    sector_instancias = join_tables(poblacional_ins, administrativo_ins)
    return sector_instancias    

#%%
if __name__=='__main__':
    actores = pd.read_excel("Actores_unicos.xlsx")
    instancias = pd.read_excel("Instancias.xlsx")
    #----------ACTORES-------------------------------------------------------------------    
    sector_actores = get_sector_actores(actores)
    #----------INSTANCIAS----------------------------------------------------------------
    sector_instancias = get_sector_instancias(instancias)
    #%%
    # GUARDAR RESULTADO EN EXCEL
    #sector_instancias.to_excel("sector_instancias.xlsx", index=False)
    # GUARDAR RESULTADO EN EXCEL
    #sector_actores.to_excel("sector_actores.xlsx", index=False)
