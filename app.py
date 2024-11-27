import pandas as pd
from supabase_config import supabase_client
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import streamlit as st

# Cargar datos de Supabase
response = supabase_client.table('envios').select('*').execute()
envios = pd.DataFrame(response.data)

# Cargar los nombres de las regiones
response_regiones = supabase_client.table('regiones').select('id_region, nombre_region').execute()
regiones = pd.DataFrame(response_regiones.data)

# Preprocesar los datos
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

# Crear un mapeo de los nombres de región
region_map = dict(zip(regiones['id_region'], regiones['nombre_region']))

# Mostrar un selectbox con los nombres de las regiones
region_name = st.selectbox('Selecciona la región', list(region_map.values()))

# Obtener el id_region correspondiente a la región seleccionada
region_id = list(region_map.keys())[list(region_map.values()).index(region_name)]

# Seleccionar mes
mes = st.selectbox('Mes', ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

# Convertir el mes seleccionado en el número correspondiente
mes_num = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'].index(mes) + 1

# Filtrar los datos
datos_filtros = envios[(envios['mes'] == mes_num) & (envios['id_region'] == region_id)]

# Mostrar las predicciones
if not datos_filtros.empty:
    st.write(f'Predicción de la demanda de envíos para la región {region_name} en el mes {mes}')
    st.write(datos_filtros[['cantidad_envios', 'tarifa_promedio']])
else:
    st.write(f'No hay datos disponibles para la región {region_name} en el mes {mes}')
