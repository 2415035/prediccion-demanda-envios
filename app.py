import pandas as pd
from supabase_config import supabase_client
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import numpy as np

# Cargar datos de Supabase
response = supabase_client.table('envios').select('*').execute()
envios = pd.DataFrame(response.data)

# Preprocesar datos
envios['fecha_envio'] = pd.to_datetime(envios['fecha_envio'])
envios['mes'] = envios['fecha_envio'].dt.month

# Codificar las columnas categóricas
label_encoder = LabelEncoder()
envios['id_region_encoded'] = label_encoder.fit_transform(envios['id_region'])
envios['id_evento_encoded'] = label_encoder.fit_transform(envios['id_evento'])
envios['id_tipo_servicio_encoded'] = label_encoder.fit_transform(envios['id_tipo_servicio'])
envios['id_ruta_encoded'] = label_encoder.fit_transform(envios['id_ruta'])

# Crear un diccionario para mapear códigos de región a nombres
region_to_name = dict(zip(envios['id_region_encoded'], envios['id_region']))

# Definir las características y el objetivo
features = ['id_region_encoded', 'cantidad_envios', 'id_evento_encoded', 'id_tipo_servicio_encoded', 'id_ruta_encoded', 'mes']
X = envios[features]
y = envios['tarifa_promedio']

# Entrenar el modelo de Random Forest para regresión
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y)

# Streamlit para mostrar la aplicación
st.title('Predicción de la Demanda de Envíos por Región y Mes')

# Seleccionar mes y región
mes = st.selectbox('Mes', list(range(1, 13)))

# Mostrar el selector de región con los nombres
region_names = list(region_to_name.values())  # Nombres de regiones
region = st.selectbox('Región', region_names)

# Codificar la región seleccionada
region_encoded = label_encoder.transform([region])[0]

# Pedir al usuario la cantidad de envíos
cantidad_envios = st.number_input('Cantidad de envíos', min_value=0, value=0)

# Codificar las otras variables
id_evento = "Evento Desconocido"
id_tipo_servicio = "Servicio Desconocido"
id_ruta = "Ruta Desconocida"

id_evento_encoded = label_encoder.transform([id_evento])[0]
id_tipo_servicio_encoded = label_encoder.transform([id_tipo_servicio])[0]
id_ruta_encoded = label_encoder.transform([id_ruta])[0]

# Crear el array de características para la predicción
X_pred = np.array([[region_encoded, cantidad_envios, id_evento_encoded, id_tipo_servicio_encoded, id_ruta_encoded, mes]])

# Predecir la tarifa promedio
tarifa_predicha = rf.predict(X_pred)[0]

# Mostrar la predicción
st.write(f"Predicción de la tarifa promedio para la región {region} en el mes {mes} con {cantidad_envios} envíos: {tarifa_predicha}")
