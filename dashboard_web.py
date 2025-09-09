import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Actividades Arcadis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
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
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .stMetric:hover {
            transform: translateY(-2px);
            transition: all 0.3s ease;
        }
        div[data-testid="stMetricValue"] {
            font-size: 24px;
            font-weight: bold;
            color: #1f77b4;
        }
        div[data-testid="stMetricDelta"] {
            color: #2ecc71;
        }
        .css-1r6slb0 {  /* Estilo para el sidebar */
            background-color: #f8f9fa;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        h2, h3 {
            color: #34495e;
        }
        </style>
    """, unsafe_allow_html=True)

    # Logo de Arcadis
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h4 style="color: #34495e;">Dashboard de Actividades</h4>
            <p style="color: #7f8c8d;">Arcadis - 2025</p>
        </div>
    """, unsafe_allow_html=True)

def anonimizar_datos(df):
    """Anonimiza los datos personales en el DataFrame"""
    if 'Nombre' in df.columns:
        # Crear un mapeo de nombres reales a anónimos
        nombres_unicos = df['Nombre'].unique()
        mapeo_nombres = {nombre: f'Usuario {i+1}' for i, nombre in enumerate(nombres_unicos)}
        df['Nombre'] = df['Nombre'].map(mapeo_nombres)
    
    if 'Asesor HSW' in df.columns:
        asesores_unicos = df['Asesor HSW'].unique()
        mapeo_asesores = {asesor: f'Asesor {i+1}' for i, asesor in enumerate(asesores_unicos)}
        df['Asesor HSW'] = df['Asesor HSW'].map(mapeo_asesores)
    
    return df

def cargar_datos():
    """Carga los datos desde los archivos CSV"""
    datos_mensuales = pd.read_csv('powerbi_datos_mensuales.csv')
    datos_trimestrales = pd.read_csv('powerbi_datos_trimestrales.csv')
    datos_detalle = pd.read_csv('powerbi_datos_detalle_anonimo.csv')
    return datos_mensuales, datos_trimestrales, datos_detalle

def crear_grafico_tendencia_mensual(datos_mensuales):
    """Crea un gráfico de línea para la tendencia mensual"""
    fig = px.line(datos_mensuales, 
                  x='Mes', 
                  y=['Actividades_Realizadas', 'Total_Actividades'],
                  title='Tendencia Mensual de Actividades',
                  labels={'value': 'Número de Actividades', 
                         'variable': 'Tipo',
                         'Mes': 'Mes',
                         'Actividades_Realizadas': 'Realizadas',
                         'Total_Actividades': 'Planificadas'},
                  markers=True,
                  template='plotly_white')
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        title={
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20)
        }
    )
    
    # Personalizar líneas y marcadores
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )
    
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

def calcular_tendencias(datos_mensuales):
    """Calcula las tendencias y variaciones de los datos"""
    tendencias = {}
    
    # Calcular variación respecto al mes anterior
    actividades_actual = datos_mensuales['Actividades_Realizadas'].iloc[-1]
    actividades_anterior = datos_mensuales['Actividades_Realizadas'].iloc[-2]
    variacion = ((actividades_actual - actividades_anterior) / actividades_anterior * 100 
                 if actividades_anterior != 0 else 0)
    
    tendencias['variacion_mensual'] = {
        'valor': variacion,
        'direccion': '↑' if variacion > 0 else '↓' if variacion < 0 else '→'
    }
    
    # Calcular promedio móvil de 3 meses
    datos_mensuales['MA3'] = datos_mensuales['Actividades_Realizadas'].rolling(window=3).mean()
    tendencia_3m = datos_mensuales['MA3'].iloc[-1] - datos_mensuales['MA3'].iloc[-2]
    
    tendencias['tendencia_trimestral'] = {
        'valor': tendencia_3m,
        'direccion': '↑' if tendencia_3m > 0 else '↓' if tendencia_3m < 0 else '→'
    }
    
    return tendencias

def main():
    # Aplicar estilo
    local_css()
    
    # Título principal
    st.title("📊 Dashboard de Actividades")
    
    try:
        # Cargar datos
        datos_mensuales, datos_trimestrales, datos_detalle = cargar_datos()
        # Calcular tendencias
        tendencias = calcular_tendencias(datos_mensuales)
        
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
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_actividades = datos_mensuales['Actividades_Realizadas'].sum()
                st.metric(
                    "Total Actividades Realizadas", 
                    f"{total_actividades:,}",
                    f"{tendencias['tendencia_trimestral']['direccion']} {abs(tendencias['tendencia_trimestral']['valor']):.1f}"
                )
            
            with col2:
                promedio = datos_mensuales['Actividades_Realizadas'].mean()
                st.metric(
                    "Promedio Mensual", 
                    f"{promedio:.1f}",
                    f"vs anterior: {tendencias['variacion_mensual']['valor']:.1f}%"
                )
            
            with col3:
                porcentaje = (datos_mensuales['Actividades_Realizadas'].sum() / 
                            datos_mensuales['Total_Actividades'].sum() * 100)
                st.metric(
                    "% Cumplimiento Total", 
                    f"{porcentaje:.1f}%",
                    f"Meta: 100%"
                )
            
            with col4:
                ultimo_mes = datos_mensuales.iloc[-1]
                cumplimiento_mes = (ultimo_mes['Actividades_Realizadas'] / 
                                  ultimo_mes['Total_Actividades'] * 100)
                st.metric(
                    f"% Cumplimiento {ultimo_mes['Mes']}", 
                    f"{cumplimiento_mes:.1f}%",
                    f"{tendencias['variacion_mensual']['direccion']} {abs(tendencias['variacion_mensual']['valor']):.1f}%"
                )
            
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
