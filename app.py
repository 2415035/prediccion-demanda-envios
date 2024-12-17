import pandas as pd
from supabase_config import supabase_client
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
#from sklearn.metrics import mean_absolute_error, mean_squared_error
import streamlit as st
import plotly.express as px

#Cargar datos de Supabase
response = supabase_client.table('envios').select('*').execute()
envios = pd.DataFrame(response.data)

#Cargar los nombres de las regiones
response_regiones = supabase_client.table('regiones').select('id_region, nombre_region').execute()
print(response_regiones.data)  # Verificar los datos recibidos
