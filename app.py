import pandas as pd
from supabase_config import supabase_client
from sklearn.ensemble import RandomForestRegressor  # Cambiado a RandomForestRegressor
import streamlit as st

# Cargar datos de Supabase
response = supabase_client.table('envios').select('*').execute()
envios = pd.DataFrame(response.data)

# Preprocesar datos
envios['fecha_envio'] = pd.to_datetime(envios['fecha_envio'])
envios['mes'] = envios['fecha_envio'].dt.month

# Definir las características y el objetivo
features = ['id_region', 'cantidad_envios', 'id_evento', 'id_tipo_servicio', 'id_ruta', 'mes']
X = envios[features]
y = envios['tarifa_promedio']

# Entrenar el modelo de Random Forest (Regresión)
rf = RandomForestRegressor(n_estimators=100, random_state=42)  # Usar regressor
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

