import pandas as pd
import re

# Definir diccionarios para clasificaciones de sectores administrativos y poblacionales
dicc_sector_admin = {
    "agricultura": ["tierras", "agropecuari", "rural", "alimento", "campesino", "agricultu", "ganader", "agrari", "pesquer", "acuicultura"],
    "ambiente": ["oceano", "ramsar", "ambiental", "sostenible", "residuo", "gestores de residuos", "ecologi", "bosque", "humedal"],
    "ciencia" : ["tecnologia", "innovacion", "ciencia", "\\btic\\b"],
    "comercio" : ["panelero", "empleadores", "turismo", "industria",
               "comercio", "consumidor", "comerciantes", "servicios publicos", 
               "privada", "empresa", "productivo", "industria", "exporta", "turistico"],
    "cultura" : ["arte", "danza","\\bcultura\\b","literatura", "musica", "teatro",
              "circo", "museo","artesanal", "cinematograf", "actor","literatura",
              "filosofi","biblioteca","filmica","cultural"],
    "defensa" : ["fuerza publica", "militar", "ff mm", "policia", "ejercito", "socorro"],
    "deporte" : ["futbol", "deporte", "arbitral", "barra", "baloncesto", "deportiv"], 
    "educacion" : ["academia","universidad","universitario", "pedagogica",
                  "experto", "academico", "investiga", "escolar", "escuela",
                  "educacion", "egresado", "formacion", "estudiante","educativo",
                  "colegio", "educacion superior", "educativa", "facultad",
                  "tecnologica", "investigador", "profesor", "cientific"],
    "estadisticas" : ["estadistic"],
    "hacienda" : ["banco", "aseguradores", "finanzas","financiero", "banca", 
                   "inversion", "regalia"],
    "interior" : ["particip","descentraliza", "ordenamiento territorial",
                  "derechos humanos", "dd hh", "religiosa", "religion", 
                  "conferencia episcopal", "iglesia","desplazad", "derecho",
                  "lgbti","lesbiana" , "gay" , "bisexual" , "indigena",
                  "transgenero" , "travesti" , "transexual" , 
                  "intersex", "queer", "memoria historica",
                  "mujeres rom","mujer rom", "hombres rom", "gitano","gitana",
                  "afrodescendiente", "negra", "negros", "mulatos",
                  "mulatas","afrocolombian", "palenque",
                  "raizal","raizales", "etnia", "etnico",
                  "madres comunitarias", "accion comunal",
                  "desarrollo comunitario", "juntas administradoras locales"],
  
  "minas_y_energia" : ["mineria", "minero","energetic","energia", "petroleo",
                     "carbon","minera", "electri","gas", "hidrocarburo",
                     "pretroler"],
  "planeacion" : ["plan nacional de desarrollo"],
  "presidencia" : ["presidenci","president"],
  "prosperidad_social" : ["victima","paz", "conflicto armado","reconciliacion", 
                         "farc","guerrill", "ejercito de liberacion nacional",
                         "estabilizacion y la consolidacion", "reincorporacion", 
                         "desmovilizados", "derechos humanos", "dd hh", 
                         "autodefensas", "cultivos ilicitos", "secuestr",
                         "cultivos de uso ilicito", "desapareci","desaparic",
                         "desaparecido", "revolucionari","antipersona"],
  
  "relaciones_exteriores" : ["exterior", "extranjero", "exporta"],
  
  "salud" : ["salud","cruz roja", "medic", "autoapoyo", "\\bsida\\b",
            "hospital", "clinic", "enfermer", "terapia",
            "psicolog","paciente", "farmaceutic","psiquiat"],
  
  "tecnologias_de_la_informacion_y_las_comunicaciones" : ["periodista", "periodismo", 
                                                         "televis", "radio", "comunicaciones",
                                                         "informacion", "\\btic\\b",
                                                         "medios de comunicacion"],
  
  "trabajo" : ["sindicato", "trabajador", "obrera","desemplead","empleador",
             "obrero", "sindical", "trabajo", "empleo", "desempleo",
             "trabajadores","sindicato","laboral"],
  
  "transporte" : ["transport", "aereo","\\bvial\\b","movilidad", "\\btrafico\\b",
                "aviacion","\\bvias\\b", "aeronau", "aeroport"],
  
  "vivienda" : ["infraestructura","viviend", "construccion"],
  
  "justicia" : ["justicia", "juridic", "conciliacion"]
}

#--------------------------------------------------

dicc_sector_pobl = {
    # Grupos étnicos
    "indigenas": ["indigena", "wayuu"],
    "etnias": ["etnia", "etnico"],
    "gitanos": ["mujeres rom", "mujer rom", "hombres rom", 
                "gitano", "gitana", r"\brom\b"],
    "afrodescendientes": ["afrodescendiente", "negra", "negros", "mulatos", 
                          "mulatas", "afrocolombian", "palenque"],
    "raizales": ["raizal", "raizales"],
    # Grupos etarios
    "jovenes": ["juventud", "jovenes", "juvenil", "adolescen"],
    "ninez": ["ninez", "infancia", "infantil", "infante", 
              r"\bninos\b", r"\bninas\b"],
    "adultos_mayores": ["adultos mayores", "pensionad", "personas mayores", 
                        "geriatri", "persona mayor", "adulto mayor"],
    # Grupos por género
    "mujeres": ["mujer"],
    "lgbti": ["lgbti", "lesbiana", "gay", "bisexual", 
              "transgenero", "travesti", "transexual", 
              "intersex", "queer"],
    # Grupos por condiciones físicas
    "discapacidad": ["discapaci", "sordo", "ciego", "lengua de senas", 
                     "interprete", "sordoceguera"],
    # Grupos académicos o de expertos
    "academia_o_expertos": ["academia", "universidad", "universitario", "trayectoria", 
                            "experto", "academico", "investiga", "estudiante", 
                            "educacion", "egresado", "formacion", 
                            "colegio", "educacion superior", "educativa", "facultad", 
                            "tecnica", "tecnologica", "investigador", "profesor", "cientific"],
    "civil": ["hombre", "persona natural", "persona civil", 
              "madres comunitarias", "accion comunal", 
              "desarrollo comunitario", 
              "juntas administradoras locales"],
    # Grupos religiosos
    "religion": ["religiosa", "religion", "catolic", "protestantes", "religioso", 
                 "judio", "musulman", "conferencia episcopal", "iglesia"],
    # Grupos vulnerables
    "desplazados": ["desplazad"]
}

def get_sector(texto,diccionario):
    # Función para clasificar el sector administrativo de cada instancia
    sector_found = ""
    for sector, keywords in diccionario.items():
        for keyword in keywords:
            if re.search(keyword,str(texto),re.IGNORECASE):
                sector_found = f'{sector_found} {sector}'
                break
    sector_found = sector_found.replace("NA", "").strip()
    sector_found = remover_duplicados(sector_found)
    sector_found = sector_found.replace("_", " ")
    return sector_found

def remover_duplicados(texto):
    # Función para remover palabras duplicadas en una cadena de texto
    palabras_unicas = list(dict.fromkeys(texto.split()))
    return ", ".join(palabras_unicas)

def apply_classification(data):
    # Aplicar las funciónes de clasificación administrativa y poblacional
    data['Sector_administrativo'] = data['Actores'].apply(get_sector,
                                                 diccionario=dicc_sector_admin)
    data["Sector_poblacional"] = data['Actores'].apply(get_sector,
                                                 diccionario=dicc_sector_pobl)
    return data

def organize_actores(data):
    # Configurar categoría y organizar los datos
    data["Actores"] = data["Actores"].str.replace(r"^las\s+|^el\s+|^los\s+|^del\s+|^la\s+|^de\s+|^por\s+", 
                                              "", regex=True)
    data["Categoria"] = "Sociedad Civil"
    data = data.sort_values(by="Actores").reset_index(drop=True)
    data["siglas"] = ""
    return data

def select_columns(df_act_inst):
    df = df_act_inst[["ID_Actor","Actores_limpio"]].copy()
    df.rename(columns = {'Actores_limpio':'Actores'}, inplace = True)
    return df
    
#%%
if __name__ == '__main__':
    df_act_inst = pd.read_excel('Actores_instancias.xlsx')
    data = select_columns(df_act_inst)
    # Aplicar la función de clasificación administrativa y poblacional
    data = apply_classification(data)
    # Configurar categoría y organizar los datos
    data = organize_actores(data)
#%% Guardar el archivo en Excel
    # Eliminar duplicados de la columna [Actores]
    #data.to_excel("Actores_unicos_ini.xlsx", index=False)
    
