import random
import string
from dateutil.relativedelta import relativedelta
import numpy as np
from numpy import loadtxt
import pandas as pd
import pickle
import re
from statistics import mean

import nltk
# nltk.download('popular')

from nltk.corpus import stopwords
from sklearn import preprocessing
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report,
                             confusion_matrix,
                             f1_score,
                             plot_confusion_matrix,
                             accuracy_score)


def generar_string(charnum):

    S= charnum
    event_id=''.join(random.choices(string.digits+string.ascii_letters,k=S))
    
    return event_id


def generar_event_id_valido(ids_list):
    new_eventid = generar_string(5)
    
    while new_eventid in ids_list:
        new_eventid = generar_string(5)
        
    return new_eventid


def encuentra_key(base,pozo,key1,key2):
    '''
    Funcion que dada una base de datos, y una clave, encuentra los indices de la fila donde se encuentra el key
    ----------------------------------------------------------------------------------------------------------
    
    - base: Dataframe con una columna de texto, lamada Operación
    - key: Cadena de caracteres que se vá a buscar en cada fila de la columna Operación  
    
    '''
    base = base[base["Nombre"]==pozo]
    base=base.sort_values(by=["Desde"])
    base=base.reset_index(drop=True)
        
    indice_ST=[]
    indice_T=[]
  
    for fila in range(0,len(base)):

        fullstring = base["Operación"][fila]
        substring = key1

        if substring in fullstring:
            indice_ST.append(fila)
    
    if len(indice_ST) > 0:
        ID = indice_ST[-1]
        ID_80=int(len(base)*0.80)

        if ID > ID_80:
            print ("El Key1 está dentro del ultimo 20% de las actividades")

        else:
            for fila in range(0,len(base)):
                fullstring = base["Operación"][fila]
                substring = key2

                if substring in fullstring:
                    indice_T.append(fila)

            ID=indice_T[-1]

        base.iloc[ID]
        print(pd.DataFrame(base.iloc[ID]).T["Hasta"]) 
        return pd.DataFrame(base.iloc[ID]).T
    
    return "El Key1 y Key 2 no están dentro del ultimo 20% de las actividades"


def predecir_modelo_deterministico(data, wellname):
    data["Operación"] = data["Operación"].str.lower().str.replace(r"\W"," ")
    data = data.dropna()
    data['Codigo'] = pd.to_numeric(data['Codigo'],errors = 'coerce')
    data = data.reset_index(drop=True)

    fecha_encontrada = encuentra_key(data,wellname,"setting","tubing")

    if type(fecha_encontrada)==str :
        fecha_encontrada = None

    elif type(fecha_encontrada) == pd.DataFrame:
        fecha_encontrada = fecha_encontrada['Hasta'].\
                                values[0].astype('datetime64[s]').item()\
                                         .strftime("%m/%d/%Y %H:%M")

    return fecha_encontrada

    



def predecir_NN():
    pass

def pre_pro_well(base,well):
    '''
    FUNCION QUE SELECCIONA UN POZO, TRANSFORMA LOS DATOS COMO INPUT DEL MODELO

    - base: Dataframe con los datos de todos los pozos.
    - well: cadena de caracteres con el nombre del pozo a evaluar    
    '''

    # Seleccion del pozo a preprocesar
    base = base[base["Nombre"]==well]
    
    #return base

    # Seleccion de la columna de tesxto
    X = base["Operación"]
    X = X.reset_index(drop=True)

    # Libreria de stopwords en ingles
    nltk.download('wordnet')
    nltk.download('omw-1.4')

    # Lista de textos vacia
    documents = []
    
    # Instanciacion del lematizador en ingles
    stemmer = WordNetLemmatizer()
    
    #return X

    # Ciclo for para que recorra todos las filas con las actividaes (textos)
    for sen in range(0, len(X)):

        # Removemos los caracteres especiales
        document = re.sub(r'\W', ' ', str(X[sen]))
        
        # Removemos todos las cadenas de caracteres de un solo caracter
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
        
        # Removemos caracteres sencillso al inicio
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
        
        # Substituimos dobles espacios por espacios sencillos
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Removemos caracteres numericos
        document = re.sub(r'\[[0-9]*\]',' ',document)
        
        # Convertimos todo a minusculas
        document = document.lower()
        
        # Realizamos Lematizacion
        document = document.split()

        document = [stemmer.lemmatize(word) for word in document]
        document = ' '.join(document)
        
        documents.append(document)
    
    return (documents,base)

def identificacion_OCM(base,well):
    '''
    Función que usa un modelo de NPL para identificar las actividades y encontrar el inicio de OCM
    ----------------------------------------------------------------------------------------------

    - well = Cadena de caracteres con el nombre del pozo a probar

    Retorna
    - 
    '''
    #-----------------------------------------------------------------------------
    # LECTURA Y PREPARACION DE DATOS
    #-----------------------------------------------------------------------------

    # Lectura de Datos
    ##path='Data.xlsx'
    ##base = pd.read_excel(path)
    base = base.dropna()
    base = base.reset_index(drop=True)

    data = base

    # Eliminacion de columnas innecesarias y cambio de nombre de columnas
    data = data.rename({'Operación':"Operacion"}, axis=1)

    #-----------------------------------------------------------------------------
    # CARGA DE MODELOS
    #-----------------------------------------------------------------------------

    # Cargue del modelo entrenado
    model_rf = pickle.load(open("rf.sav", 'rb'))

    # Cargue del vectorizador entrenado
    vectorizer = pickle.load(open("vectorizer.sav", 'rb'))

    # Cargue del codificador de etiquetas
    le = pickle.load(open("label_encoder.sav", 'rb'))

    #-----------------------------------------------------------------------------
    # PREPROCESAMIENTO DE LA INFORMACION PARA LA PREDICCION DEL POZO SOLICITADO
    #-----------------------------------------------------------------------------

    # Preparamos los datos para la prediccion sobre un pozo especifico
    X_val,base_val = pre_pro_well(base,well)
    #return pre_pro_well(base,well)

    # Usamos el vectorizador para transformar los datos para la prediccion
    X_val = vectorizer.transform(X_val)

    #-----------------------------------------------------------------------------
    # PREDICCION SOBRE DATOS PREPROCESADOS
    #-----------------------------------------------------------------------------

    # Prediccion
    y_val = model_rf.predict(X_val)

    #-----------------------------------------------------------------------------
    # VISUALIZACION DE LA PREDICCION
    #-----------------------------------------------------------------------------

    # Union con datos del pozo
    base_val["Target"] = le.inverse_transform(y_val)

    # Organizacion del dataframe
    base_val = base_val[['Codigo', 'Target', 'Nombre', 'Desde', 'Hasta',"MDFrom","MDto" , "Operación"]]
    
    #-----------------------------------------------------------------------------
    # BUSQUEDA DE INICIO DE OCM
    #-----------------------------------------------------------------------------

    # Organizacion de la base en orden descendente
    base_val = base_val.sort_values(by=['Desde'],ascending=False)
    base_val = base_val.reset_index(drop=True)

    # Algoritmo para deteccion de inicio de OCM
    fila = 1
    while (base_val.Target[fila] == base_val.Target[fila-1]):
        fila=fila+1
    else:
        ID_OCM=fila

    ODR_Finish = base_val.Hasta[ID_OCM]

    base_val = base_val.sort_values(by=['Desde'],ascending=True)
    base_val = base_val.reset_index(drop=True)

    ODR_Finish = ODR_Finish.strftime("%m/%d/%Y %H:%M")
    
    respuesta =str("El Final del evento ODR en el Pozo " + str(well) + " se da en la fecha: " + str(ODR_Finish)+"\n")
    
    return(base_val,respuesta,ODR_Finish)