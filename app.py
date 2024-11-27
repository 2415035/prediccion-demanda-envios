import pandas as pd
from supabase_config import supabase_client
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import streamlit as st

# Cargar datos de Supabase
response = supabase_client.table('envios').select('*').execute()
envios = pd.DataFrame(response.data)

# Cargar datos de regiones desde Supabase (para tener los nombres de las regiones)
response_regiones = supabase_client.table('regiones').select('*').execute()
regiones = pd.DataFrame(response_regiones.data)

# Preprocesar datos
envios['fecha_envio'] = pd.to_datetime(envios['fecha_envio'])
envios['mes'] = envios['fecha_envio'].dt.month

# Verificar las columnas iniciales
st.write("Columnas en el DataFrame de envios:", envios.columns)

# Crear un diccionario que mapea el id_region a nombre de la región
id_region_to_nombre = dict(zip(regiones['id_region'], regiones['nombre_region']))

# Mostrar el selector de región con los nombres
region_names = list(id_region_to_nombre.values())  # Nombres de las regiones
region = st.selectbox('Región', region_names)

# Convertir el nombre de la región seleccionado de vuelta al id_region
region_id = [key for key, value in id_region_to_nombre.items() if value == region][0]

# Verificar si las columnas de codificación existen
if 'id_evento' in envios.columns and 'id_tipo_servicio' in envios.columns and 'id_ruta' in envios.columns:
    # Codificar las columnas categóricas
    label_encoder_evento = LabelEncoder()
    envios['id_evento_encoded'] = label_encoder_evento.fit_transform(envios['id_evento'])

    label_encoder_servicio = LabelEncoder()
    envios['id_tipo_servicio_encoded'] = label_encoder_servicio.fit_transform(envios['id_tipo_servicio'])

    label_encoder_ruta = LabelEncoder()
    envios['id_ruta_encoded'] = label_encoder_ruta.fit_transform(envios['id_ruta'])
else:
    st.write("Faltan columnas necesarias para la codificación.")

# Verificar las columnas después de la codificación
st.write("Columnas después de la codificación:", envios.columns)

# Definir las características y el objetivo
features = ['id_region_encoded', 'cantidad_envios', 'id_evento_encoded', 'id_tipo_servicio_encoded', 'id_ruta_encoded', 'mes']
X = envios[features]
y = envios['tarifa_promedio']

# Entrenar el modelo de Random Forest para regresión
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y)

# Predicciones
predicciones = rf.predict(X)

# Streamlit para mostrar la aplicación
st.title('Predicción de la Demanda de Envíos por Región y Mes')

# Seleccionar mes y región
mes = st.selectbox('Mes', list(range(1, 13)))

# Filtrar los datos
datos_filtros = envios[(envios['mes'] == mes) & (envios['id_region'] == region_id)]

# Mostrar las predicciones
if not datos_filtros.empty:
    st.write('Predicción de la demanda de envíos para la región', region, 'en el mes', mes)
    st.write(datos_filtros[['cantidad_envios', 'tarifa_promedio']])
else:
    st.write('No hay datos disponibles para la región', region, 'en el mes', mes)
