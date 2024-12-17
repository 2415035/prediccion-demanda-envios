import pandas as pd
from supabase_config import supabase_client
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error
import streamlit as st
import plotly.express as px

#Cargar datos de Supabase
response = supabase_client.table('envios').select('*').execute()
envios = pd.DataFrame(response.data)

# Cargar los nombres de las regiones
response_regiones = supabase_client.table('regiones').select('id_region, nombre_region').execute()
regiones = pd.DataFrame(response_regiones.data)

# Verificar si la tabla 'regiones' está vacía
if len(regiones) == 0:
    st.write("La tabla 'regiones' está vacía.")
else:
    st.write("Tabla 'regiones' cargada con éxito. Primeras filas:", regiones.head())

# Verificar si la columna 'id_region' existe
if 'id_region' in regiones.columns:
    st.write("La columna 'id_region' existe.")
else:
    st.write("La columna 'id_region' NO existe.")

# Verificar los nombres de las columnas
st.write("Columnas de la tabla 'regiones':", regiones.columns)