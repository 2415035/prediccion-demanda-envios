import pandas as pd
from supabase_config import supabase_client
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import streamlit as st

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

# Lista de meses
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# Seleccionar mes por nombre
mes_nombre = st.selectbox('Mes', meses)

# Convertir el nombre del mes seleccionado al número correspondiente
mes = meses.index(mes_nombre) + 1  # Sumar 1 porque los índices de Python comienzan en 0

# Seleccionar región
region = st.selectbox('Selecciona la región', envios['id_region'].unique())

# Filtrar los datos
datos_filtros = envios[(envios['mes'] == mes) & (envios['id_region'] == region)]

# Mostrar las predicciones
if not datos_filtros.empty:
    st.write('Predicción de la demanda de envíos para la región', region, 'en el mes', mes_nombre)
    st.write(datos_filtros[['cantidad_envios', 'tarifa_promedio']])
else:
    st.write('No hay datos disponibles para la región', region, 'en el mes', mes_nombre)
