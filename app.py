import streamlit as st
import random

# ==========================================
# CONFIGURACIÓN DE PÁGINA ULTRA-MINIMALISTA
# ==========================================
st.set_page_config(
    page_title="PROMETEUS ELITE",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS de Alta Densidad Visual para Móvil
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .main-title {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #FFFFFF;
        text-align: center;
        font-weight: 800;
        font-size: 30px;
        letter-spacing: 2px;
        margin-top: 10px;
        margin-bottom: 2px;
    }
    .subtitle {
        text-align: center;
        color: #00E676;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1px;
        margin-bottom: 25px;
    }
    .seccion-titulo {
        font-size: 14px;
        font-weight: bold;
        color: #FFFFFF;
        background-color: #262626;
        padding: 6px 12px;
        border-radius: 5px;
        margin-top: 20px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    .apuesta-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 5px solid #00E676;
    }
    .apuesta-titulo {
        font-size: 12px;
        color: #888888;
        margin-bottom: 4px;
        font-weight: bold;
    }
    .apuesta-numeros {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
        letter-spacing: 3px;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 4px !important;
    }
    .stButton>button {
        padding: 4px 2px !important;
        font-size: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">PROMETEUS ELITE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">PROMETEUS ELITE ULTRA 6/50</div>', unsafe_allow_html=True)

# Tramos de decenas fijos y Mellizos
TRAMOS = {
    "1-10": list(range(1, 11)),
    "11-20": list(range(11, 21)),
    "21-30": list(range(21, 31)),
    "31-40": list(range(31, 41)),
    "41-50": list(range(41, 51))
}
MELLIZOS_LIST = [11, 22, 33, 44]

# Inicialización del Session State
if "r10" not in st.session_state: st.session_state.r10 = []
if "r15" not in st.session_state: st.session_state.r15 = []
if "vetadas" not in st.session_state: st.session_state.vetadas = []
if "dobles" not in st.session_state: st.session_state.dobles = []

# ==========================================
# BLOQUE 1: PARRILLAS DE NÚMEROS RECIENTES
# ==========================================
st.markdown('<div class="seccion-titulo">📊 Listas de Control Recientes</div>', unsafe_allow_html=True)

# Parrilla Recientes 10
st.markdown(f"**Parrilla Recientes 10** ({len(st.session_state.r10)}/10 seleccionados - Mínimo 4)")
for i in range(5):
    cols = st.columns(10)
    for j in range(10):
        num = i * 10 + j + 1
        is_selected = num in st.session_state.r10
        disabled = num in st.session_state.r15
        label = f"★ {num}" if is_selected else str(num)
        if cols[j].button(label, key=f"btn_r10_{num}", disabled=disabled, use_container_width=True):
            if is_selected:
                st.session_state.r10.remove(num)
            elif len(st.session_state.r10) < 10:
                st.session_state.r10.append(num)
            st.rerun()

# Parrilla Recientes 15
st.markdown(f"**Parrilla Recientes 15** ({len(st.session_state.r15)}/15 seleccionados - Mínimo 8)")
for i in range(5):
    cols = st.columns(10)
    for j in range(10):
        num = i * 10 + j + 1
        is_selected = num in st.session_state.r15
        disabled = num in st.session_state.r10
        label = f"★ {num}" if is_selected else str(num)
        if cols[j].button(label, key=f"btn_r15_{num}", disabled=disabled, use_container_width=True):
            if is_selected:
                st.session_state.r15.remove(num)
            elif len(st.session_state.r15) < 15:
                st.session_state.r15.append(num)
            st.rerun()

# ==========================================
# BLOQUE 2: SELECTORES DE DECENAS
# ==========================================
st.markdown('<div class="seccion-titulo">🔢 Configuración de Decenas</div>', unsafe_allow_html=True)

decena_libre = st.selectbox("Selector Decena Libre (Tendrá 0 números)", list(TRAMOS.keys()))

st.write("Selector Decenas Dobles (Tendrán 2 números cada una - Máx. 2)")
cols_dec = st.columns(5)
opciones_decenas = [k for k in TRAMOS.keys() if k != decena_libre]
for idx, dec in enumerate(opciones_decenas):
    is_doble = dec in st.session_state.dobles
    if cols_dec[idx].button(f" Doble {dec}" if is_doble else dec, key=f"doble_{dec}", use_container_width=True):
        if is_doble:
            st.session_state.dobles.remove(dec)
        elif len(st.session_state.dobles) < 2:
            st.session_state.dobles.append(dec)
        st.rerun()

# ==========================================
# BLOQUE 3: SELECTORES DE UNIDADES Y TERMINACIONES
# ==========================================
st.markdown('<div class="seccion-titulo">🎯 Control de Terminaciones</div>', unsafe_allow_html=True)

unidad_repetida_sel = st.selectbox("Selector Unidad Repetida", ["Al azar"] + list(range(10)))

st.write("Selector Unidad Vetada (Excluye terminaciones completas - Máx. 4)")
cols_uni = st.columns(10)
for u in range(10):
    is_vetada = u in st.session_state.vetadas
    label_u = f"❌ {u}" if is_vetada else str(u)
    if cols_uni[u].button(label_u, key=f"vetar_{u}", use_container_width=True):
        if is_vetada:
            st.session_state.vetadas.remove(u)
        elif len(st.session_state.vetadas) < 4:
            st.session_state.vetadas.append(u)
        st.rerun()

# ==========================================
# BLOQUE 4: INTERRUPTORES ESPECIALES
# ==========================================
st.markdown('<div class="seccion-titulo">⚡ Filtros Especiales</div>', unsafe_allow_html=True)
col_sw1, col_sw2 = st.columns(2)
with col_sw1:
    selector_mellizos = st.radio("Selector Mellizos (Apuestas 2 y 4)", ["NO", "SÍ"])
with col_sw2:
    selector_clumps = st.radio("Selector Clumps (Apuestas 3 y 4)", ["NO", "SÍ"])

# ==========================================
# MOTOR DE CÁLCULO DE ALTA POTENCIA
# ==========================================
def cumple_filtros_individuales(comb, d_libre, d_dobles, u_repetida, vetadas):
    # Paridad (3 pares, 3 impares)
    pares = sum(1 for x in comb if x % 2 == 0)
    if pares != 3: return False

    # Estructura Decenas
    counts_decenas = {k: 0 for k in TRAMOS.keys()}
    for x in comb:
        for k, v in TRAMOS.items():
            if x in v: counts_decenas[k] += 1
            
    if counts_decenas[d_libre] != 0: return False
    dobles_reales = [k for k, v in counts_decenas.items() if v == 2]
    simples_reales = [k for k, v in counts_decenas.items() if v == 1]
    if len(dobles_reales) != 2 or len(simples_reales) != 2: return False
    for d in d_dobles:
        if counts_decenas[d] != 2: return False

    # Terminaciones
    terminaciones = [x % 10 for x in comb]
    if any(t in vetadas for t in terminaciones): return False
    counts_term = {t: terminaciones.count(t) for t in set(terminaciones)}
    rep_2 = [t for t, c in counts_term.items() if c == 2]
    if len(rep_2) != 1 or len(counts_term) != 5: return False
    if u_repetida != "Al azar" and rep_2[0] != u_repetida: return False

    return True

def generar_motor_prometeus():
    # Universo Depurado
    universo = [x for x in range(1, 51) if (x % 10) not in st.session_state.vetadas and x not in TRAMOS[decena_libre]]
    
    # Asignación de Decenas Dobles Automáticas si falta rellenar
    d_dobles_actuales = list(st.session_state.dobles)
    opciones_disponibles = [k for k in TRAMOS.keys() if k != decena_libre]
    while len(d_dobles_actuales) < 2:
        restantes = [o for o in opciones_disponibles if o not in d_dobles_actuales]
        if not restantes: break
        d_dobles_actuales.append(random.choice(restantes))

    apuestas_finales = []
    intentos_globales = 0
    
    # Garantizar números disponibles de listas de recientes
    r10_pool = list(st.session_state.r10)
    r15_pool = list(st.session_state.r15)
    
    while len(apuestas_finales) < 4 and intentos_globales < 5000:
        intentos_globales += 1
        num_apuesta = len(apuestas_finales) + 1
        
        # Muestreo de Recientes
        c_r10 = random.sample(r10_pool, 1)
        c_r15 = random.sample(r15_pool, 2)
        base_recientes = c_r10 + c_r15
        
        # Filtrar universo eliminando lo ya escogido en las fuentes de recientes
        resto_universo = [x for x in universo if x not in base_recientes]
        if len(resto_universo) < 3: continue
        
        c_resto = random.sample(resto_universo, 3)
        candidata = sorted(base_recientes + c_resto)
        
        # Regla de Mellizos
        tiene_mellizo = any(m in candidata for m in MELLIZOS_LIST)
        es_apuesta_melliza = num_apuesta in [2, 4] and selector_mellizos == "SÍ"
        
        if es_apuesta_melliza:
            # Forzar un mellizo si no lo tiene (Regla de escape interna si están vetados)
            if not tiene_mellizo:
                mellizos_validos = [m for m in MELLIZOS_LIST if (m % 10) not in st.session_state.vetadas and m not in TRAMOS[decena_libre]]
                if mellizos_validos:
                    candidata[0] = random.choice(mellizos_validos)
                    candidata = sorted(list(set(candidata)))
                    if len(candidata) < 6: continue
            # Validar que tenga exactamente un mellizo
            if sum(1 for x in candidata if x in MELLIZOS_LIST) != 1: continue
        else:
            if selector_mellizos == "SÍ" and tiene_mellizo: continue
            elif selector_mellizos == "NO" and tiene_mellizo: continue # Filtro base excluidos

        # Regla de Clumps (Números Seguidos)
        consecutivos = sum(1 for idx in range(5) if candidata[idx+1] - candidata[idx] == 1)
        es_apuesta_clump = num_apuesta in [3, 4] and selector_clumps == "SÍ"
        
        if es_apuesta_clump:
            if consecutivos != 1: continue
            # Validar escape de unidad vetada o decena libre en el clump
            par_consecutivo = [(candidata[idx], candidata[idx+1]) for idx in range(5) if candidata[idx+1] - candidata[idx] == 1]
            if any(n in TRAMOS[decena_libre] or (n % 10) in st.session_state.vetadas for n in par_consecutivo[0]): continue
        else:
            if consecutivos > 0: continue

        # Validaciones de Filtros Individuales Estrictos
        if not cumple_filtros_individuales(candidata, decena_libre, d_dobles_actuales, unidad_repetida_sel, st.session_state.vetadas):
            continue

        # Validación Cruzada: Máximo 1 coincidencia con apuestas ya aprobadas
        interseccion_ok = True
        for ap in apuestas_finales:
            coincidencias = len(set(candidata).intersection(set(ap)))
            if modificaciones > 1 or  coincidencias > 1:
                interseccion_ok = False
                break
        
        if interseccion_ok:
            apuestas_finales.append(candidata)

    return apuestas_finales

# ==========================================
# BLOQUE 5: ACCIÓN Y RESULTADOS
# ==========================================
st.markdown('<div class="seccion-titulo">🚀 Generador</div>', unsafe_allow_html=True)

# Validación de mínimos de seguridad antes de habilitar el botón
requisitos_ok = len(st.session_state.r10) >= 4 and len(st.session_state.r15) >= 8

if requisitos_ok:
    if st.button("🔥 GENERAR COMBINACIONES PROMETEUS", use_container_width=True, type="primary"):
        resultados = generar_motor_prometeus()
        
        if len(resultados) < 4:
            st.error("La combinación de filtros es restrictiva. Inténtalo de nuevo o amplía los números de las parrillas.")
        else:
            st.success("Cálculo finalizado con éxito de forma fluida.")
            for i, ap in enumerate(resultados):
                numeros_str = " ".join(f"{num:02d}" for num in ap)
                st.markdown(f"""
                <div class="apuesta-card">
                    <div class="apuesta-titulo">COMBINACIÓN MÚLTIPLE Nº{i+1}</div>
                    <div class="apuesta-numeros">{numeros_str}</div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.warning("Faltan números en las Parrillas Recientes para cumplir con el mínimo de control de seguridad (Mínimo 4 en Recientes 10 y 8 en Recientes 15).")
