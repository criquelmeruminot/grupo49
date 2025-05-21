import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# from mpl_toolkits.mplot3d import Axes3D # Si deciden incluir el 3D en el dashboard

# --- Configuración de la Página del Dashboard ---
st.set_page_config(layout="wide", page_title="Dashboard de Ventas - Supermercado")

# --- Función para Cargar y Cachar Datos ---
@st.cache_data
def cargar_datos_dashboard():
    df_dash = pd.read_csv('data.csv')
    df_dash['Date'] = pd.to_datetime(df_dash['Date'], format='%m/%d/%Y')
    df_dash['Mes'] = df_dash['Date'].dt.month_name()
    df_dash['Dia_semana'] = df_dash['Date'].dt.day_name()
    return df_dash

df_dashboard_completo = cargar_datos_dashboard()

# --- Título Principal ---
st.title('📊 Dashboard de Análisis de Ventas de Tienda de Conveniencia')
st.markdown("""
Este dashboard interactivo presenta un análisis visual de los datos de ventas, 
permitiendo explorar tendencias y comportamientos de los clientes.
Utilice los filtros en la barra lateral para segmentar la información.
""")

# --- Barra Lateral de Filtros ---
st.sidebar.header('Filtros Aplicables:')

ciudades_seleccionadas = st.sidebar.multiselect(
    "🏙️ Filtrar por Ciudad:",
    options=df_dashboard_completo['City'].unique(),
    default=df_dashboard_completo['City'].unique()
)

tipos_cliente_seleccionados = st.sidebar.multiselect(
    "👤 Filtrar por Tipo de Cliente:",
    options=df_dashboard_completo['Customer type'].unique(),
    default=df_dashboard_completo['Customer type'].unique()
)

lineas_producto_seleccionadas = st.sidebar.multiselect(
    "🛍️ Filtrar por Línea de Producto:",
    options=df_dashboard_completo['Product line'].unique(),
    default=df_dashboard_completo['Product line'].unique()
)

sucursal_seleccionadas = st.sidebar.multiselect(
    "🏪 Filtrar por Sucursal de Venta:",
    options=df_dashboard_completo['Branch'].unique(),
    default=df_dashboard_completo['Branch'].unique()
)

genero_seleccionado = st.sidebar.multiselect(
    "🧑‍🧒‍🧒 Filtrar por Género de Cliente:",
    options=df_dashboard_completo['Gender'].unique(),
    default=df_dashboard_completo['Gender'].unique()
)
# --- Aplicación de Filtros al DataFrame ---
df_filtrado_dash = df_dashboard_completo[
    (df_dashboard_completo['City'].isin(ciudades_seleccionadas)) &
    (df_dashboard_completo['Customer type'].isin(tipos_cliente_seleccionados)) &
    (df_dashboard_completo['Product line'].isin(lineas_producto_seleccionadas)) &
    (df_dashboard_completo['Branch'].isin(sucursal_seleccionadas)) &
    (df_dashboard_completo['Gender'].isin(genero_seleccionado))

]

if df_filtrado_dash.empty:
    st.warning("No se encontraron datos para los filtros seleccionados. Por favor, modifique su selección.")
else:
    # --- Diseño del Dashboard en Columnas ---
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader('Ingresos por Línea de Producto')
        ingresos_prod_dash = df_filtrado_dash.groupby('Product line')['Total'].sum().reset_index().sort_values('Total', ascending=False)
        fig_ing_prod, ax_ing_prod = plt.subplots(figsize=(7, 5))
        sns.barplot(x="Total", y="Product line", data=ingresos_prod_dash, ax=ax_ing_prod, palette="mako")
        ax_ing_prod.set_xlabel("Ingresos Totales ($)")
        ax_ing_prod.set_ylabel("Línea de Producto")
        st.pyplot(fig_ing_prod)
        with st.expander("Análisis del Gráfico"):
            st.write("Este gráfico permite identificar las líneas de producto más rentables según los filtros aplicados.")

        st.subheader('Distribución de Calificaciones de Clientes')
        fig_rating_dash, ax_rating_dash = plt.subplots(figsize=(7, 5))
        sns.histplot(data=df_filtrado_dash, x='Rating', bins=10, kde=True, color='teal', ax=ax_rating_dash)
        ax_rating_dash.set_xlabel('Calificación')
        ax_rating_dash.set_ylabel('Frecuencia')
        st.pyplot(fig_rating_dash)
        with st.expander("Análisis del Gráfico"):
            st.write("Visualiza la satisfacción de los clientes. Una distribución sesgada hacia calificaciones altas es deseable.")

    with col_der:
        st.subheader('Métodos de Pago Preferidos')
        fig_pago_dash, ax_pago_dash = plt.subplots(figsize=(7, 5))
        sns.countplot(y='Payment', data=df_filtrado_dash, order=df_filtrado_dash['Payment'].value_counts().index, ax=ax_pago_dash, palette='flare')
        ax_pago_dash.set_xlabel('Número de Transacciones')
        ax_pago_dash.set_ylabel('Método de Pago')
        st.pyplot(fig_pago_dash)
        with st.expander("Análisis del Gráfico"):
            st.write("Muestra las preferencias de pago de los clientes, información útil para optimizar procesos de cobro.")

        st.subheader('Gasto Total por Tipo de Cliente')
        fig_gasto_tipo_dash, ax_gasto_tipo_dash = plt.subplots(figsize=(7, 5))
        sns.boxplot(x='Customer type', y='Total', data=df_filtrado_dash, ax=ax_gasto_tipo_dash, palette='crest')
        ax_gasto_tipo_dash.set_xlabel('Tipo de Cliente')
        ax_gasto_tipo_dash.set_ylabel('Gasto Total ($)')
        st.pyplot(fig_gasto_tipo_dash)
        with st.expander("Análisis del Gráfico"):
            st.write("Compara el comportamiento de gasto entre miembros y clientes normales, útil para evaluar programas de lealtad.")

    # Gráfico de Evolución de Ventas (ocupa más ancho)
    st.markdown("---")
    st.subheader('Evolución de Ventas Totales Diarias (Filtrado)')
    ventas_dia_dash = df_filtrado_dash.groupby(df_filtrado_dash['Date'].dt.date)['Total'].sum().reset_index()
    ventas_dia_dash.sort_values(by='Date', inplace=True)
    fig_ventas_dia, ax_ventas_dia = plt.subplots(figsize=(12, 5))
    sns.lineplot(x='Date', y='Total', data=ventas_dia_dash, marker='o', ax=ax_ventas_dia)
    ax_ventas_dia.set_xlabel('Fecha')
    ax_ventas_dia.set_ylabel('Ventas Totales ($)')
    plt.xticks(rotation=45)
    st.pyplot(fig_ventas_dia)
    with st.expander("Análisis del Gráfico"):
        st.write("Observa las tendencias de ventas a lo largo del tiempo para los segmentos seleccionados.")


# --- Reflexión sobre el Dashboard y Pensamiento Crítico ---
st.sidebar.markdown("---")
st.sidebar.subheader("Reflexión sobre el Dashboard")
st.sidebar.info("""
La interactividad de este dashboard, mediante los filtros de Ciudad, Tipo de Cliente y Línea de Producto, 
potencia significativamente la capacidad de análisis. Permite al usuario final:
- Segmentar la información para descubrir patrones específicos no visibles en un análisis agregado.
- Comparar comportamientos entre diferentes grupos (e.g., ¿los 'Miembros' de Yangon compran más 'Accesorios de moda' que los 'Normales' en Mandalay?).
- Validar hipótesis de negocio de forma rápida y visual.
Esto facilita una toma de decisiones más ágil y basada en evidencia, mejorando la capacidad de respuesta de la cadena de tiendas a las necesidades de sus clientes y a las dinámicas del mercado.
""")
