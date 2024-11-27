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

# Streamlit para mostrar la aplicación
st.title('Predicción de la Demanda de Envíos por Región y Mes')

# Seleccionar mes y región
mes = st.selectbox('Mes', list(range(1, 13)))
region = st.selectbox('Región', envios['id_region'].unique())

# Codificar la región seleccionada
region_encoded = label_encoder.transform([region])[0]

# Pedir al usuario la cantidad de envíos (este dato es necesario para hacer la predicción)
cantidad_envios = st.number_input('Cantidad de envíos', min_value=0, value=0)

# Codificar las otras variables (puedes usar valores predeterminados o valores específicos para el evento y servicio)
id_evento = "Evento Desconocido"  # Este es un valor predeterminado
id_tipo_servicio = "Servicio Desconocido"  # Este es un valor predeterminado
id_ruta = "Ruta Desconocida"  # Este es un valor predeterminado

# Codificar estas variables
id_evento_encoded = label_encoder.transform([id_evento])[0]
id_tipo_servicio_encoded = label_encoder.transform([id_tipo_servicio])[0]
id_ruta_encoded = label_encoder.transform([id_ruta])[0]

# Crear el array de características para la predicción
X_pred = np.array([[region_encoded, cantidad_envios, id_evento_encoded, id_tipo_servicio_encoded, id_ruta_encoded, mes]])

# Predecir la tarifa promedio
tarifa_predicha = rf.predict(X_pred)[0]

# Mostrar la predicción
st.write(f"Predicción de la tarifa promedio para la región {region} en el mes {mes} con {cantidad_envios} envíos: {tarifa_predicha}")






