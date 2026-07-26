import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Rugo Ranch AI - Gestor Profesional",
    page_icon="🤠",
    layout="wide",
)

# Estilo personalizado estilo Ranch
st.markdown(
    """
    <style>
    .main { background-color: #f8f6f0; }
    .stApp { font-family: 'Georgia', serif; }
    h1, h2, h3 { color: #1b3b2b; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #1b3b2b; color: white; border-radius: 5px; font-weight: bold; }
    .stButton>button:hover { background-color: #8c6d3b; color: white; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🤠 RUGO RANCH AI — Sistema de Gestión Integral")
st.subheader("Panel Profesional de Control Ganadero")

# Inicializar Base de Datos en Sesión
if "inventario_animales" not in st.session_state:
    st.session_state.inventario_animales = pd.DataFrame(
        [
            {
                "Tag/Arete": "VAC-001",
                "Especie": "Bovino",
                "Raza": "Angus",
                "Peso (kg)": 450,
                "Estado Salud": "Sano",
                "Alimentación": "Pastoreo + 2kg Concentrado",
            },
            {
                "Tag/Arete": "OVE-012",
                "Especie": "Ovino",
                "Raza": "Dorper",
                "Peso (kg)": 45,
                "Estado Salud": "Atención (FAMACHA 3)",
                "Alimentación": "Pastoreo",
            },
        ]
    )

if "registro_finanzas" not in st.session_state:
    st.session_state.registro_finanzas = pd.DataFrame(
        [
            {
                "Fecha": "2026-07-20",
                "Tipo": "Gasto",
                "Categoría": "Alimento/Heno",
                "Monto ($)": 350.0,
                "Detalle": "50 pacas de heno",
            },
            {
                "Fecha": "2026-07-25",
                "Tipo": "Ingreso",
                "Categoría": "Venta de Crías",
                "Monto ($)": 800.0,
                "Detalle": "Venta 2 corderos",
            },
        ]
    )

if "registro_medico" not in st.session_state:
    st.session_state.registro_medico = pd.DataFrame(
        [
            {
                "Fecha": "2026-06-15",
                "Tag/Arete": "VAC-001",
                "Tratamiento/Vacuna": "Desparasitante Interno",
                "Próxima Dosis": "2026-12-15",
            }
        ]
    )

# Configuración Sidebar
st.sidebar.header("📋 Configuración Rápida")
acres = st.sidebar.number_input("Superficie Total (Acres)", value=9.0, step=0.5)
pacas_heno = st.sidebar.number_input(
    "Inventario Heno (Pacas)", value=50, step=5
)
potreros = st.sidebar.slider(
    "Número de Potreros", min_value=2, max_value=8, value=4
)

# Conteo automático desde el inventario
df_anim = st.session_state.inventario_animales
vacas = len(df_anim[df_anim["Especie"] == "Bovino"])
ovejas = len(df_anim[df_anim["Especie"] == "Ovino"])

ms_vacas = vacas * 12.5
ms_ovejas = ovejas * 1.8
ms_total_diaria = ms_vacas + ms_ovejas

# Tabs de la App
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "🏷️ Inventario Animales",
        "🌱 Pastoreo",
        "🩺 Salud y FAMACHA©",
        "💰 Finanzas y Gastos",
        "📦 Insumos y Reglas",
    ]
)

# TAB 1: INVENTARIO DE ANIMALES
with tab1:
    st.header("Gestión Individual por Tag/Arete")

    col_form, col_tabla = st.columns([1, 2])

    with col_form:
        st.subheader("Registrar / Modificar Animal")
        tag = st.text_input("Número de Tag / Arete", placeholder="Ej. VAC-002")
        especie = st.selectbox("Especie", ["Bovino", "Ovino"])
        raza = st.text_input("Raza", placeholder="Ej. Angus, Dorper, Katahdin")
        peso = st.number_input("Peso Actual (kg)", value=50.0, step=1.0)
        salud = st.selectbox(
            "Estado de Salud",
            ["Sano", "Atención (FAMACHA 3)", "En Tratamiento", "Cuarentena"],
        )
        dieta = st.text_input(
            "Ración / Alimentación Especial",
            value="Pastoreo + Sales Minerales",
        )

        if st.button("Guardar Animal"):
            if tag:
                # Reemplazar si existe o agregar nuevo
                df_temp = st.session_state.inventario_animales
                df_temp = df_temp[df_temp["Tag/Arete"] != tag]
                nuevo_animal = pd.DataFrame(
                    [
                        {
                            "Tag/Arete": tag,
                            "Especie": especie,
                            "Raza": raza,
                            "Peso (kg)": peso,
                            "Estado Salud": salud,
                            "Alimentación": dieta,
                        }
                    ]
                )
                st.session_state.inventario_animales = pd.concat(
                    [df_temp, nuevo_animal], ignore_index=True
                )
                st.success(f"✅ Animal {tag} guardado con éxito.")
                st.rerun()
            else:
                st.error("Por favor ingresa un Tag o número de arete válido.")

    with col_tabla:
        st.subheader("Censo Actual del Rancho")
        st.dataframe(st.session_state.inventario_animales, use_container_width=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Bovinos", f"{vacas} cabezas")
        m2.metric("Total Ovinos", f"{ovejas} cabezas")
        peso_prom = (
            df_anim["Peso (kg)"].mean() if not df_anim.empty else 0
        )
        m3.metric("Peso Promedio Hato", f"{peso_prom:.1f} kg")

# TAB 2: PASTOREO
with tab1:  # (Mantener lógica previa de pastoreo en Tab 2)
    pass
with tab2:
    st.header("Planificador de Rotación de Potreros")
    col1, col2 = st.columns(2)
    with col1:
        potrero_actual = st.selectbox(
            "Potrero Actual", [f"Potrero {i+1}" for i in range(potreros)]
        )
        altura_pasto = st.slider(
            "Altura del Pasto (cm)", min_value=0, max_value=40, value=18
        )
    with col2:
        st.metric(
            "Consumo Diario Estimado", f"{ms_total_diaria:.1f} kg MS/día"
        )
        st.metric("Carga Actual", f"{vacas} Vacas / {ovejas} Ovejas")

    st.divider()
    if altura_pasto > 20:
        dias_estancia = int((altura_pasto - 8) * 0.4)
        st.success(
            f"✅ **Estado Óptimo:** Mantener animales en {potrero_actual}. Días estimados de estancia restante: **{dias_estancia} días**."
        )
    elif 8 <= altura_pasto <= 20:
        idx = int(potrero_actual.split()[-1])
        siguiente = f"Potrero {(idx % potreros) + 1}"
        st.warning(
            f"⚠️ **Alerta de Movimiento:** Prepara el traslado hacia **{siguiente}** en 24-48 hrs."
        )
    else:
        st.error(
            "🚨 **Riesgo Crítico de Sobrepastoreo:** Mueve el ganado o suplementa con heno inmediatamente."
        )

# TAB 3: SALUD Y FAMACHA + HISTORIAL MÉDICO
with tab3:
    st.header("Control de Salud y Tratamientos")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.subheader("Evaluación Rápida FAMACHA© (Ovejas)")
        fam_tag = st.selectbox(
            "Selecciona Ovino",
            df_anim[df_anim["Especie"] == "Ovino"]["Tag/Arete"].tolist()
            if not df_anim.empty
            else ["N/A"],
        )
        famacha_score = st.radio(
            "Grado Mucosa Ocular:",
            ["Grado 1 (Sano)", "Grado 2 (OK)", "Grado 3 (Alerta)", "Grado 4/5 (Anemia Crítica)"],
        )
        if "Grado 4/5" in famacha_score:
            st.error("🔴 **Acción Inmediata:** Desparasitar y aislar.")
        elif "Grado 3" in famacha_score:
            st.warning("🟡 **Atención:** Monitorear peso en 7 días.")
        else:
            st.success("🟢 **Saludable:** Sin tratamiento antiparasitario.")

    with col_f2:
        st.subheader("Registrar Vacuna / Tratamiento")
        med_tag = st.selectbox(
            "Animal Tratado",
            df_anim["Tag/Arete"].tolist() if not df_anim.empty else ["N/A"],
        )
        tratamiento = st.text_input("Tratamiento / Vacuna aplicada")
        fecha_prox = st.date_input("Próxima dosis / Refuerzo")

        if st.button("Registrar Tratamiento"):
            nuevo_med = pd.DataFrame(
                [
                    {
                        "Fecha": datetime.date.today().strftime("%Y-%m-%d"),
                        "Tag/Arete": med_tag,
                        "Tratamiento/Vacuna": tratamiento,
                        "Próxima Dosis": fecha_prox.strftime("%Y-%m-%d"),
                    }
                ]
            )
            st.session_state.registro_medico = pd.concat(
                [st.session_state.registro_medico, nuevo_med], ignore_index=True
            )
            st.success("Tratamiento registrado.")

    st.subheader("Historial Médico")
    st.dataframe(st.session_state.registro_medico, use_container_width=True)

# TAB 4: FINANZAS Y GASTOS
with tab4:
    st.header("Libro Contable del Rancho")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Nuevo Registro")
        tipo_trans = st.selectbox("Tipo", ["Gasto", "Ingreso"])
        cat_trans = st.selectbox(
            "Categoría",
            [
                "Alimento/Heno",
                "Medicina/Veterinario",
                "Mantenimiento Cercas",
                "Venta de Crías",
                "Venta de Lana/Leche",
                "Otros",
            ],
        )
        monto = st.number_input("Monto ($)", min_value=0.0, step=10.0)
        detalle = st.text_input("Descripción / Detalle")

        if st.button("Guardar Transacción"):
            nueva_trans = pd.DataFrame(
                [
                    {
                        "Fecha": datetime.date.today().strftime("%Y-%m-%d"),
                        "Tipo": tipo_trans,
                        "Categoría": cat_trans,
                        "Monto ($)": monto,
                        "Detalle": detalle,
                    }
                ]
            )
            st.session_state.registro_finanzas = pd.concat(
                [st.session_state.registro_finanzas, nueva_trans],
                ignore_index=True,
            )
            st.success("Transacción contable agregada.")
            st.rerun()

    with c2:
        st.subheader("Balance Económico")
        df_fin = st.session_state.registro_finanzas

        ingresos = df_fin[df_fin["Tipo"] == "Ingreso"]["Monto ($)"].sum()
        gastos = df_fin[df_fin["Tipo"] == "Gasto"]["Monto ($)"].sum()
        balance = ingresos - gastos

        f1, f2, f3 = st.columns(3)
        f1.metric("Ingresos Totales", f"${ingresos:,.2f}")
        f2.metric("Gastos Totales", f"${gastos:,.2f}")
        f3.metric("Balance Neto", f"${balance:,.2f}")

        st.dataframe(df_fin, use_container_width=True)

# TAB 5: INSUMOS Y REGLAS
with tab5:
    st.header("Inventario de Insumos y Reglas Críticas")

    kg_heno_por_paca = 15
    dias_heno_cobertura = (pacas_heno * kg_heno_por_paca) / (
        ms_total_diaria if ms_total_diaria > 0 else 1
    )

    col_a, col_b = st.columns(2)
    col_a.metric(
        "Días de Cobertura de Heno", value=f"{int(dias_heno_cobertura)} días"
    )

    if dias_heno_cobertura < 60:
        col_b.error("🚨 **Reserva Baja:** Se sugiere comprar más heno.")
    else:
        col_b.success("✅ **Nivel de Heno Seguro**.")

    st.divider()
    st.subheader("⚠️ Regla Antitóxica Permanente")
    st.warning(
        " Recordatorio: Usar exclusivamente sales minerales **SINO O LIBRES DE COBRE** en prados mixtos. El cobre en dosis vacunas mata a las ovejas."
    )
