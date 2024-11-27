import pandas as pd
from supabase_config import supabase_client
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import matplotlib.pyplot as plt

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

# Definir las características y los objetivos
features = ['id_region_encoded', 'cantidad_envios', 'id_evento_encoded', 'id_tipo_servicio_encoded', 'id_ruta_encoded', 'mes']
X = envios[features]
y_tarifa = envios['tarifa_promedio']
y_cantidad = envios['cantidad_envios']

# Entrenar modelos de Random Forest
rf_tarifa = RandomForestRegressor(n_estimators=100, random_state=42)
rf_tarifa.fit(X, y_tarifa)

rf_cantidad = RandomForestRegressor(n_estimators=100, random_state=42)
rf_cantidad.fit(X, y_cantidad)

# Streamlit para mostrar la aplicación
st.title('Predicción de la Demanda de Envíos por Región y Mes')

# Seleccionar mes y región
mes = st.selectbox('Mes', list(range(1, 13)))
region = st.selectbox('Región', envios['id_region'].unique())

# Crear entrada para predicción
region_encoded = label_encoder.transform([region])[0]
X_pred = pd.DataFrame({
    'id_region_encoded': [region_encoded],
    'cantidad_envios': [envios['cantidad_envios'].mean()],  # Usar valor promedio como base
    'id_evento_encoded': [0],  # Ajusta según contexto
    'id_tipo_servicio_encoded': [0],  # Ajusta según contexto
    'id_ruta_encoded': [0],  # Ajusta según contexto
    'mes': [mes]
})

# Hacer predicciones
pred_tarifa = rf_tarifa.predict(X_pred)[0]
pred_cantidad = rf_cantidad.predict(X_pred)[0]

# Mostrar resultados
st.write(f'### Predicción para la región {region} en el mes {mes}:')
st.metric(label="Cantidad Proyectada de Envíos", value=int(pred_cantidad))
st.metric(label="Tarifa Promedio Proyectada", value=round(pred_tarifa, 2))

# Gráfico comparativo: Históricos vs Predicciones
fig, ax = plt.subplots()
historico_region = envios[envios['id_region'] == region]
ax.plot(historico_region['mes'], historico_region['cantidad_envios'], label="Histórico Envíos", marker='o')
ax.axhline(y=pred_cantidad, color='r', linestyle='--', label='Predicción Envíos')
ax.set_title(f'Comparativa Histórica y Predicción en Región {region}')
ax.set_xlabel('Mes')
ax.set_ylabel('Cantidad de Envíos')
ax.legend()
st.pyplot(fig)

# Botón para exportar resultados a Excel
export_data = pd.DataFrame({
    'Mes': [mes],
    'Región': [region],
    'Cantidad Proyectada': [int(pred_cantidad)],
    'Tarifa Promedio Proyectada': [round(pred_tarifa, 2)]
})

if st.button('Exportar Predicción a Excel'):
    export_data.to_excel('prediccion_envios.xlsx', index=False)
    st.success('Archivo exportado como prediccion_envios.xlsx')

# Guardar predicciones en Supabase
if st.button('Guardar Predicción en Supabase'):
    supabase_client.table('predicciones').insert({
        'mes': mes,
        'region': region,
        'cantidad_proyectada': int(pred_cantidad),
        'tarifa_promedio_proyectada': round(pred_tarifa, 2)
    }).execute()
    st.success('Predicción guardada en la base de datos.')


