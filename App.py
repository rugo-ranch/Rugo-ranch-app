import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Rugo Ranch AI - Gestor Inteligente",
    page_icon="🤠",
    layout="wide"
)

# Estilo personalizado
st.markdown("""
    <style>
    .main { background-color: #f8f6f0; }
    .stApp { font-family: 'Georgia', serif; }
    h1, h2, h3 { color: #1b3b2b; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #1b3b2b; color: white; border-radius: 5px; font-weight: bold; }
    .stButton>button:hover { background-color: #8c6d3b; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🤠 RUGO RANCH AI — Sistema de Gestión Inteligente")
st.subheader("Panel de Control para Ganadería Integrada")

st.sidebar.header("📋 Configuración del Rancho")
acres = st.sidebar.number_input("Superficie Total (Acres)", value=9.0, step=0.5)
vacas = st.sidebar.number_input("Número de Bovinos (Vacas/Novillos)", value=3, step=1)
ovejas = st.sidebar.number_input("Número de Ovinos (Ovejas)", value=12, step=1)
pacas_heno = st.sidebar.number_input("Inventario de Pacas de Heno", value=50, step=5)
potreros = st.sidebar.slider("Número de Potreros", min_value=2, max_value=8, value=4)

# Cálculos Base
ms_vacas = vacas * 12.5
ms_ovejas = ovejas * 1.8
ms_total_diaria = ms_vacas + ms_ovejas

# Tabs principales
tab1, tab2, tab3 = st.tabs(["🌱 Control de Pastoreo", "🩺 Salud y FAMACHA©", "📦 Inventario y Alertas"])

with tab1:
    st.header("Planificador de Rotación de Potreros")
    col1, col2 = st.columns(2)
    
    with col1:
        potrero_actual = st.selectbox("Potrero Actual en Uso", [f"Potrero {i+1}" for i in range(potreros)])
        altura_pasto = st.slider("Altura Promedio del Pasto (cm)", min_value=0, max_value=40, value=18)
    
    with col2:
        st.metric(label="Consumo Total Diario (Materia Seca)", value=f"{ms_total_diaria:.1f} kg/día")
        st.metric(label="Consumo Bovina / Ovina", value=f"{ms_vacas:.1f} kg / {ms_ovejas:.1f} kg")

    st.divider()

    if altura_pasto > 20:
        dias_estancia = int((altura_pasto - 8) * 0.4)
        st.success(f"✅ **Estado Óptimo:** Mantener animales en {potrero_actual}. Días estimados de estancia restante: **{dias_estancia} días**.")
    elif 8 <= altura_pasto <= 20:
        idx = int(potrero_actual.split()[-1])
        siguiente_potrero = f"Potrero {(idx % potreros) + 1}"
        st.warning(f"⚠️ **Alerta de Movimiento:** El pasto está bajando. Prepara el traslado hacia el **{siguiente_potrero}** en las próximas 24–48 horas.")
    else:
        st.error("🚨 **Riesgo Crítico de Sobrepastoreo:** Mueve inmediatamente al rebaño o inicia la suplementación con heno.")

with tab2:
    st.header("Asistente de Salud y Evaluación FAMACHA©")
    st.write("Registra el estado ocular de las ovejas para detectar anemia por parásitos (*Haemonchus contortus*).")
    
    famacha_score = st.radio("Selecciona el grado FAMACHA detectado en la mucosa ocular:", [
        "Grado 1 (Rojo Vivo - Saludable)",
        "Grado 2 (Rosa Fuerte - Ok)",
        "Grado 3 (Rosa Pálido - Alerta)",
        "Grado 4 (Blanco / Rosa muy pálido - Severo)",
        "Grado 5 (Blanco - Crítico)"
    ])
    
    if "Grado 1" in famacha_score or "Grado 2" in famacha_score:
        st.success("🟢 **Sin Anemia:** No desparasitar. Mantiene la eficacia de los antiparasitarios.")
    elif "Grado 3" in famacha_score:
        st.warning("🟡 **Afectación Moderada:** Monitorear semanalmente y verificar si hay pérdida de peso.")
    else:
        st.error("🔴 **Anemia Severa / Crítica:** Desparasitar de inmediato con la dosis exacta según peso corporal.")

with tab3:
    st.header("Auditoría Automática de Insumos y Riesgos")
    
    kg_heno_por_paca = 15
    dias_heno_cobertura = (pacas_heno * kg_heno_por_paca) / (ms_total_diaria if ms_total_diaria > 0 else 1)
    
    col_a, col_b = st.columns(2)
    col_a.metric("Días de Cobertura de Heno Restantes", value=f"{int(dias_heno_cobertura)} días")
    
    if dias_heno_cobertura < 60:
        col_b.error("🚨 **Inventario Bajo:** Se recomienda comprar reserva invernal antes del cambio de temporada.")
    else:
        col_b.success("✅ **Inventario Suficiente:** Cobertura adecuada para la temporada.")
        
    st.divider()
    st.subheader("Reglas de Seguridad Integrada")
    st.info("🔒 **Regla Antitóxica:** Mantener siempre sales minerales LIBRES DE COBRE en zonas compartidas por vacas y ovejas.")
