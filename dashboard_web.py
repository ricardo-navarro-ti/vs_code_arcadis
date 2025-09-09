import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Actividades",
    page_icon="📊",
    layout="wide"
)

# Función para aplicar estilo
def local_css():
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def cargar_datos():
    """Carga los datos desde los archivos CSV"""
    datos_mensuales = pd.read_csv('powerbi_datos_mensuales.csv')
    datos_trimestrales = pd.read_csv('powerbi_datos_trimestrales.csv')
    datos_detalle = pd.read_csv('powerbi_datos_detalle.csv')
    return datos_mensuales, datos_trimestrales, datos_detalle

def crear_grafico_tendencia_mensual(datos_mensuales):
    """Crea un gráfico de línea para la tendencia mensual"""
    fig = px.line(datos_mensuales, 
                  x='Mes', 
                  y=['Actividades_Realizadas', 'Total_Actividades'],
                  title='Tendencia Mensual de Actividades',
                  labels={'value': 'Número de Actividades', 'variable': 'Tipo'},
                  markers=True)
    fig.update_layout(height=400)
    return fig

def crear_grafico_trimestral(datos_trimestrales):
    """Crea un gráfico de barras para comparación trimestral"""
    fig = px.bar(datos_trimestrales,
                 x='Trimestre',
                 y=['Actividades_Realizadas', 'Total_Actividades'],
                 title='Comparación Trimestral',
                 barmode='group',
                 labels={'value': 'Número de Actividades', 'variable': 'Tipo'})
    fig.update_layout(height=400)
    return fig

def crear_mapa_calor_actividades(datos_detalle):
    """Crea un mapa de calor de actividades por área y mes"""
    meses = ['Ene', 'feb', 'mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sept', 'Oct', 'Nov', 'Dic']
    datos_pivot = datos_detalle.groupby('Gerencia área / area')[meses].sum()
    
    fig = go.Figure(data=go.Heatmap(
        z=datos_pivot.values,
        x=meses,
        y=datos_pivot.index,
        colorscale='RdYlBu_r'))
    
    fig.update_layout(
        title='Mapa de Calor: Actividades por Área y Mes',
        height=400)
    return fig

def main():
    # Aplicar estilo
    local_css()
    
    # Título principal
    st.title("📊 Dashboard de Actividades")
    
    try:
        # Cargar datos
        datos_mensuales, datos_trimestrales, datos_detalle = cargar_datos()
        
        # Menú de navegación
        with st.sidebar:
            selected = option_menu(
                "Navegación",
                ["Resumen", "Análisis Temporal", "Detalle por Áreas"],
                icons=['house', 'graph-up', 'people'],
                menu_icon="cast",
                default_index=0
            )
        
        if selected == "Resumen":
            # Métricas principales
            col1, col2, col3 = st.columns(3)
            with col1:
                total_actividades = datos_mensuales['Actividades_Realizadas'].sum()
                st.metric("Total Actividades Realizadas", f"{total_actividades:,}")
            
            with col2:
                promedio = datos_mensuales['Actividades_Realizadas'].mean()
                st.metric("Promedio Mensual", f"{promedio:.1f}")
            
            with col3:
                porcentaje = (datos_mensuales['Actividades_Realizadas'].sum() / 
                            datos_mensuales['Total_Actividades'].sum() * 100)
                st.metric("% Cumplimiento Total", f"{porcentaje:.1f}%")
            
            # Gráficos principales
            st.plotly_chart(crear_grafico_tendencia_mensual(datos_mensuales), use_container_width=True)
            st.plotly_chart(crear_grafico_trimestral(datos_trimestrales), use_container_width=True)
            
        elif selected == "Análisis Temporal":
            # Análisis detallado por tiempo
            st.subheader("Análisis Temporal Detallado")
            
            # Tabla de datos mensuales con formato
            st.write("### Datos Mensuales")
            st.dataframe(datos_mensuales.style.background_gradient(subset=['Porcentaje_Realizacion']))
            
            # Gráfico de tendencia mensual
            st.plotly_chart(crear_grafico_tendencia_mensual(datos_mensuales), use_container_width=True)
            
        elif selected == "Detalle por Áreas":
            # Análisis por áreas
            st.subheader("Análisis por Áreas")
            
            # Filtro de área
            areas = datos_detalle['Gerencia área / area'].unique()
            area_seleccionada = st.selectbox("Seleccionar Área:", areas)
            
            # Datos filtrados
            datos_filtrados = datos_detalle[datos_detalle['Gerencia área / area'] == area_seleccionada]
            
            # Mostrar mapa de calor
            st.plotly_chart(crear_mapa_calor_actividades(datos_detalle), use_container_width=True)
            
            # Tabla de detalle
            st.write(f"### Detalle de {area_seleccionada}")
            st.dataframe(datos_filtrados)

    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        st.info("Por favor, asegúrate de que los archivos CSV estén en el directorio correcto.")

if __name__ == "__main__":
    main()
