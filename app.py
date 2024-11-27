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

# Codificar la columna 'id_region' antes de usarla en el modelo
label_encoder_region = LabelEncoder()
envios['id_region_encoded'] = label_encoder_region.fit_transform(envios['id_region'])

# Codificar otras columnas categóricas necesarias
if 'id_evento' in envios.columns:
    label_encoder_evento = LabelEncoder()
    envios['id_evento_encoded'] = label_encoder_evento.fit_transform(envios['id_evento'])
else:
    st.write("Falta la columna 'id_evento' en el DataFrame")

if 'id_tipo_servicio' in envios.columns:
    label_encoder_servicio = LabelEncoder()
    envios['id_tipo_servicio_encoded'] = label_encoder_servicio.fit_transform(envios['id_tipo_servicio'])
else:
    st.write("Falta la columna 'id_tipo_servicio' en el DataFrame")

if 'id_ruta' in envios.columns:
    label_encoder_ruta = LabelEncoder()
    envios['id_ruta_encoded'] = label_encoder_ruta.fit_transform(envios['id_ruta'])
else:
    st.write("Falta la columna 'id_ruta' en el DataFrame")

# Verificar las columnas después de la codificación
st.write("Columnas después de la codificación:", envios.columns)

# Definir las características y el objetivo
features = ['id_region_encoded', 'cantidad_envios', 'id_evento_encoded', 'id_tipo_servicio_encoded', 'id_ruta_encoded', 'mes']

# Verificar si todas las características necesarias están presentes
missing_features = [feature for feature in features if feature not in envios.columns]
if missing_features:
    st.write(f"Faltan las siguientes características: {missing_features}")
else:
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
