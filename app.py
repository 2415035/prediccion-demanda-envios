import pandas as pd
import streamlit as st
from supabase_config import supabase_client
import plotly.express as px

# Configuración de la aplicación Streamlit
st.title("Tabla de Envíos desde Supabase")

# Cargar datos de Supabase
response = supabase_client.table('envios').select('*').execute()

if response.data:  # Verificar si hay datos
    envios = pd.DataFrame(response.data)
    
    # Mostrar la tabla completa en Streamlit
    st.subheader("Datos de la Tabla 'Envíos'")
    st.dataframe(envios)

    # Agregar un gráfico de ejemplo (opcional)
    if "cantidad_envios" in envios.columns and "fecha_envio" in envios.columns:
        fig = px.line(envios, x="fecha_envio", y="cantidad_envios", title="Cantidad de Envíos por Fecha")
        st.plotly_chart(fig)
else:
    st.error("No se encontraron datos en la tabla 'envíos'. Verifica tu conexión o datos en Supabase.")

# Cargar nombres de regiones
response_regiones = supabase_client.table('regiones').select('id_region, nombre_region').execute()

if response_regiones.data:
    regiones = pd.DataFrame(response_regiones.data)
    st.subheader("Regiones disponibles")
    st.dataframe(regiones)
else:
    st.error("No se encontraron datos en la tabla 'regiones'.")

