import pandas as pd
from supabase_config import supabase_client
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import numpy as np

# Cargar datos desde Supabase
response = supabase_client.table('envios').select('*').execute()
envios = pd.DataFrame(response.data)

# Validar si los datos fueron cargados
if envios.empty:
    st.error("No se pudieron cargar los datos de Supabase. Verifica tu conexión.")
    st.stop()

# Preprocesar datos
envios['fecha_envio'] = pd.to_datetime(envios['fecha_envio'])
envios['mes'] = envios['fecha_envio'].dt.month

# Codificar columnas categóricas
label_encoder = LabelEncoder()

# Asegurar que todos los valores están presentes antes del fit
envios['id_region'] = envios['id_region'].fillna("Región Desconocida")
envios['id_evento'] = envios['id_evento'].fillna("Evento Desconocido")
envios['id_tipo_servicio'] = envios['id_tipo_servicio'].fillna("Servicio Desconocido")
envios['id_ruta'] = envios['id_ruta'].fillna("Ruta Desconocida")

# Aplicar codificación con LabelEncoder
envios['id_region_encoded'] = label_encoder.fit_transform(envios['id_region'])
envios['id_evento_encoded'] = label_encoder.fit_transform(envios['id_evento'])
envios['id_tipo_servicio_encoded'] = label_encoder.fit_transform(envios['id_tipo_servicio'])
envios['id_ruta_encoded'] = label_encoder.fit_transform(envios['id_ruta'])

# Definir características (X) y objetivo (y)
features = ['id_region_encoded', 'cantidad_envios', 'id_evento_encoded', 'id_tipo_servicio_encoded', 'id_ruta_encoded', 'mes']
X = envios[features]
y = envios['tarifa_promedio']

# Manejar valores faltantes en el objetivo
if y.isnull().any():
    st.error("Existen valores nulos en la columna 'tarifa_promedio'. Corrige los datos en la fuente.")
    st.stop()

# Entrenar el modelo de Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y)

# Streamlit para mostrar la aplicación
st.title('Predicción de la Demanda de Envíos por Región y Mes')

# Seleccionar mes y región
mes = st.selectbox('Mes', list(range(1, 13)))
region = st.selectbox('Región', envios['id_region'].unique())

# Validar que la región seleccionada está en el conjunto de datos
try:
    region_encoded = label_encoder.transform([region])[0]
except ValueError:
    st.error(f"La región seleccionada '{region}' no está disponible en los datos procesados.")
    st.stop()

# Filtrar los datos para el mes y la región seleccionada
datos_filtrados = envios[(envios['mes'] == mes) & (envios['id_region_encoded'] == region_encoded)]

# Mostrar resultados o mensaje si no hay datos
if not datos_filtrados.empty:
    st.write(f'Predicción de la demanda de envíos para la región {region} en el mes {mes}')
    st.write(datos_filtrados[['cantidad_envios', 'tarifa_promedio']])
else:
    st.write(f'No hay datos disponibles para la región {region} en el mes {mes}')



