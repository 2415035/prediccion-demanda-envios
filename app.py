#Aquí irá el código principal de la predicción usando Random Forest y la interfaz de usuario de Streamlit.

import pandas as pd
from supabase_config import supabase_client
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import streamlit as st

# Cargar datos de Supabase
response = supabase_client.table('envios').select('*').execute()
envios = pd.DataFrame(response.data)

# Preprocesar datos
envios['fecha_envio'] = pd.to_datetime(envios['fecha_envio'])
envios['mes'] = envios['fecha_envio'].dt.month

# Codificar variables categóricas usando LabelEncoder
label_encoder = LabelEncoder()

# Codificar cada columna categórica
envios['id_region'] = label_encoder.fit_transform(envios['id_region'])
envios['id_evento'] = label_encoder.fit_transform(envios['id_evento'])
envios['id_tipo_servicio'] = label_encoder.fit_transform(envios['id_tipo_servicio'])
envios['id_ruta'] = label_encoder.fit_transform(envios['id_ruta'])

# Definir las características (X) y el objetivo (y)
features = ['id_region', 'cantidad_envios', 'id_evento', 'id_tipo_servicio', 'id_ruta', 'mes']
X = envios[features]
y = envios['tarifa_promedio']

# Entrenar el modelo de Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# Predicciones
predicciones = rf.predict(X)

# Streamlit para mostrar la aplicación
st.title('Predicción de la Demanda de Envíos por Región y Mes')

# Seleccionar mes y región
mes = st.selectbox('Mes', list(range(1, 13)))
region = st.selectbox('Región', envios['id_region'].unique())

# Filtrar los datos
datos_filtros = envios[(envios['mes'] == mes) & (envios['id_region'] == region)]

# Mostrar las predicciones
if not datos_filtros.empty:
    st.write('Predicción de la demanda de envíos para la región', region, 'en el mes', mes)
    st.write(datos_filtros[['cantidad_envios', 'tarifa_promedio']])
else:
    st.write('No hay datos disponibles para la región', region, 'en el mes', mes)
