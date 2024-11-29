# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:33:00 2024

@author: mflagosv
"""

import pandas as pd
import re
import unicodedata


def get_actores_limpio(df):
    # Realizar depuración del nombre de los actores
    actores = df.copy()
    actores['ID_Actor'] = ""
    # Realizar depuración del nombre de los actores
    actores['Actores'] = actores['Actores'].apply(normalizar_texto)
    # Copiar y depurar nuevamente para 'Actores_limpio'
    actores['Actores_limpio'] = actores['Actores'].apply(normalizar_texto)
    return actores

def clean_actores(act_inst):
    #--------- Función para limpiar texto "Actores_limpio
    act_inst['Actores_limpio'] = act_inst['Actores_limpio'].apply(remove_patt)
    act_inst['Actores_limpio'] = act_inst['Actores_limpio'].apply(remove_sing)
    #Eliminar números y ciertas palabras al inicio
    act_inst['Actores_limpio'] = act_inst['Actores_limpio'].str.replace(r'\d+', '', regex=True)
    act_inst['Actores_limpio'] = act_inst['Actores_limpio'].str.replace(r'^(las|el|los|del|la|de|por)\s+', '', regex=True)
    act_inst['Actores_limpio'] = act_inst['Actores_limpio'].str.replace(r'^(las|el|los|del|la|de|por)\s+', '', regex=True)
    act_inst['Actores_limpio'] = act_inst['Actores_limpio'].str.strip()
    act_inst = act_inst[act_inst['Actores'].str.len() > 3]
    act_inst = act_inst.dropna(subset = ['Actores']).copy()
    return(act_inst)

def count_actores(act_inst):
    act_inst['Conteo'] = act_inst['Actores'].apply(cont_plazas)
    # Eliminar caracteres no numéricos y convertir a numérico
    act_inst['Conteo'] = act_inst['Conteo'].apply(lambda x: re.sub(r'[^0-9.-]', '', str(x)))
    # Convertir valores no numéricos a NaN y luego a 1 en 'Conteo'
    act_inst['Conteo'] = pd.to_numeric(act_inst['Conteo'], errors='coerce').fillna(1)
    act_inst['Conteo'] = act_inst['Conteo'].astype(int)
    # Eliminar duplicados y limpiar espacios extra en 'Actores_limpio'   
    #dup = act_inst[act_inst.duplicated()]
    #print(f'\nSe encontraron {len(dup)} duplicados de actores')
    act_inst['Actores_limpio'] = act_inst['Actores_limpio'].str.replace('  ', ' ', regex=False)
    return act_inst

def normalizar_texto(texto):
    # Convertir a ASCII eliminando acentos y convertir a minúsculas
    texto = unicodedata.normalize('NFD', str(texto)).encode('ascii', 'ignore').decode('utf-8').lower()
    # Eliminar puntuaciones
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

def remove_patt(texto):
    # Patrones de texto a eliminar
    patrones = [
        "un delegado del", "delegados de las", "delegados de los", "delegado de las", "delegado de los", 
        "el director del", "el director general del", "director delegado del", "representante legal de la",
        "delegado designado por la", "delegado designado por el", "representantes de los", "representantes de las",
        "representantes de", "representante de las", "representante de la", "representante de los",
        "representante de cada una de las", "representante de", "representante del", "representante a la", 
        "representante con", "cada uno de los", "un", "uno", "una", "dos", "tres", "cuatro", "cinco", 
        "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince", 
        "o quien haga sus veces", "o su delegado quien lo presidira", "o su delegado", "quien lo presidira",
        "representante por", "representante legal de", "representante", "representantes", "delegado del",
        "delegado de la", "director", "rector de", "rectores de", "o quien haga sus veces", "o los nombrados para ello",
        "que ejercera la secretaria tecnica y lo presidira", "secretaria tecnica", "directores de", "delegadoa de las",
        "delegadoa", "docentes de la", "docentes del", "docentes de los", "el tecnico de", "egresados de las",
        "egresados de los", "egresado de los", "el legal del", "el legal", "el jefe de la", "suplentes o los nombrados para ello",
        "tecnico del", "el de la", "el de", "por cada de las", "delegado por cada", "delegado de", "ejecutivo de la",
        "presidente de la", "seran participantes con voz y sin voto las autoridades", "ejecutivo de la", 
        "actor reconocido por el", "actor reconocido por la", "director de la autoridad", "director de la direccion de"
    ]
    # Remover patrones de texto de la columna 'Actores_limpio'
    for patron in patrones:
        #patt = r'\b' + re.escape(patron) + r'\b'
        patt = rf'\b{patron}\b'
        texto = re.sub(patt,'',texto)
    texto = texto.strip().replace("\t","")
    return texto

def remove_sing(texto):
    # Hacer depuración de términos singulares
    dic_singulares = {
    "el ministro": "ministerio", "ministro de": "ministerio", "ministro del": "ministerio",
    "viceministro": "ministerio", "fiscal":"fiscalia", "contralor":"contraloria",
    "procurador": "procuraduria", "alcalde": "alcaldia", "alcaldes": "alcaldia",
    "consejero": "consejo", "jefe nacional": "jefatura nacional", "personeros": "personerias",
    "notarios": "notaria", "notarios": "notaria", "consejerias": "consejeria", "consejeros": "consejeria",
    "exdirector": "direccion", "presidenciales": "presidencial", "coordinadora": "coordinacion", 
    "superintendente": "superintendencia"
    }
    for singular, reemplazo in dic_singulares.items():
        patt = rf'\b{singular}\b'
        texto = re.sub(patt,reemplazo,texto)
    return texto

def cont_plazas(texto):
    dic_num = {
        "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7,
        "ocho": 8, "nueve": 9, "diez": 10
    }
    conteo = texto
    for palabra, numero in dic_num.items():
        patt = rf'\b{palabra}\b'
        if re.search(patt,texto):
            conteo = numero
    return conteo
def get_act_conteo(df):
    df_actores = df.copy()
    act_conteo = b_ac.get_actores_limpio(df_actores)
    act_conteo = b_ac.clean_actores(act_conteo)
    act_conteo = b_ac.count_actores(act_conteo)
    return act_conteo
#%%
if __name__ == "__main__":
#-----------Leer el archivo Excel
    df_actores = pd.read_excel("actores.xlsx")
#-----------Adecuación inicial del texto -> Actores limpio
    act_conteo = get_actores_limpio(df_actores)
#--------- Limpiar texto actores 
    act_conteo = clean_actores(act_conteo)
#--------- Realizar conteo del número de plazas
    act_conteo = count_actores(act_conteo)
#%%Guardar el archivo
    #act_conteo.to_excel("actores_conteo.xlsx", index=False)
# =============================================================================
#--- limpiar duplicados en la columna Actores_limpio y cambiar nombre a Actores, limpiar los nan y generar
#---- el archivo Actores_unicos[ID_Actor,Actores] - > Este archivo se debe editar a mano, verificando solo los nuevos Actores
#---- Además de agregar el ID a los nuevos actores
# act_unicos.to_excel("Actores_unicos.xlsx", index=False)
# =============================================================================
