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
    /* Forzar que los radio buttons se muestren en línea horizontal si es posible */
    div[data-testid="stRadio"] > div {
        flex-direction: row !important;
        gap: 15px;
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
if "decena_libre" not in st.session_state: st.session_state.decena_libre = "1-10"
if "unidad_repetida" not in st.session_state: st.session_state.unidad_repetida = "Al azar"

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
# BLOQUE 2: SELECTORES DE DECENAS (DESPLEGADOS)
# ==========================================
st.markdown('<div class="seccion-titulo">🔢 Configuración de Decenas</div>', unsafe_allow_html=True)

st.write("**Selector Decena Libre** (Tendrá 0 números - Elige una)")
cols_libres = st.columns(5)
for idx, dec in enumerate(TRAMOS.keys()):
    is_libre = st.session_state.decena_libre == dec
    label_l = f"🛑 {dec}" if is_libre else dec
    if cols_libres[idx].button(label_l, key=f"libre_btn_{dec}", use_container_width=True):
        st.session_state.decena_libre = dec
        if dec in st.session_state.dobles:
            st.session_state.dobles.remove(dec)
        st.rerun()

st.write("**Selector Decenas Dobles** (Tendrán 2 números cada una - Máx. 2)")
cols_dec = st.columns(5)
opciones_decenas = [k for k in TRAMOS.keys() if k != st.session_state.decena_libre]
for idx, dec in enumerate(TRAMOS.keys()):
    if dec == st.session_state.decena_libre:
        cols_dec[idx].button(f" Libre", key=f"doble_dis_{dec}", disabled=True, use_container_width=True)
        continue
    is_doble = dec in st.session_state.dobles
    label_d = f"🟢 Doble {dec}" if is_doble else dec
    if cols_dec[idx].button(label_d, key=f"doble_{dec}", use_container_width=True):
        if is_doble:
            st.session_state.dobles.remove(dec)
        elif len(st.session_state.dobles) < 2:
            st.session_state.dobles.append(dec)
        st.rerun()

# ==========================================
# BLOQUE 3: SELECTORES DE UNIDADES (DESPLEGADOS)
# ==========================================
st.markdown('<div class="seccion-titulo">🎯 Control de Terminaciones</div>', unsafe_allow_html=True)

st.write("**Selector Unidad Repetida** (Fija la terminación común)")
cols_rep = st.columns(11)
opciones_rep = ["Al azar"] + list(range(10))
for idx, op in enumerate(opciones_rep):
    is_sel = st.session_state.unidad_repetida == op
    label_r = f"⭐ {op}" if is_sel else str(op)
    if cols_rep[idx].button(label_r, key=f"rep_btn_{op}", use_container_width=True):
        st.session_state.unidad_repetida = op
        st.rerun()

st.write("**Selector Unidad Vetada** (Excluye terminaciones completas - Máx. 4)")
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
    selector_mellizos = st.radio("Selector Mellizos (Apuestas 2 y 4)", ["NO", "SÍ"], index=0)
with col_sw2:
    selector_clumps = st.radio("Selector Clumps (Apuestas 3 y 4)", ["NO", "SÍ"], index=0)

# ==========================================
# MOTOR ULTRA-POTENCIADO POR FILTRADO INVERSO DIRECTO
# ==========================================
def cumple_filtros_estrictos(comb, d_libre, d_dobles, u_repetida, vetadas, num_apuesta):
    # 1. Paridad Estricta (3 pares y 3 impares)
    if sum(1 for x in comb if x % 2 == 0) != 3: return False

    # 2. Estructura Exacta Decenas (2-2-1-1-0)
    counts_decenas = {k: 0 for k in TRAMOS.keys()}
    for x in comb:
        for k, v in TRAMOS.items():
            if x in v: counts_decenas[k] += 1
    if counts_decenas[d_libre] != 0: return False
    if len([k for k, v in counts_decenas.items() if v == 2]) != 2: return False
    if len([k for k, v in counts_decenas.items() if v == 1]) != 2: return False
    for d in d_dobles:
        if counts_decenas[d] != 2: return False

    # 3. Control de Terminaciones Únicas
    terminaciones = [x % 10 for x in comb]
    if any(t in vetadas for t in terminaciones): return False
    counts_term = {t: terminaciones.count(t) for t in set(terminaciones)}
    rep_2 = [t for t, c in counts_term.items() if c == 2]
    if len(rep_2) != 1 or len(counts_term) != 5: return False
    if u_repetida != "Al azar" and rep_2[0] != u_repetida: return False

    # 4. Filtro de Mellizos (11, 22, 33, 44)
    num_mellizos = sum(1 for x in comb if x in MELLIZOS_LIST)
    if selector_mellizos == "SÍ" and num_apuesta in [2, 4]:
        if num_mellizos != 1: return False
        # El mellizo no puede estar en la decena libre ni unidad vetada (Regla de Escape si todo está bloqueado)
        mellizo_real = [x for x in comb if x in MELLIZOS_LIST][0]
        if mellizo_real in TRAMOS[d_libre] or (mellizo_real % 10) in vetadas:
            pass # Se permite por regla de escape acordada si es imposible
    else:
        if num_mellizos > 0: return False # Excluidos por defecto

    # 5. Filtro de Clumps (Números Seguidos)
    consecutivos = sum(1 for idx in range(5) if comb[idx+1] - comb[idx] == 1)
    if selector_clumps == "SÍ" and num_apuesta in [3, 4]:
        if consecutivos != 1: return False
    else:
        if consecutivos > 0: return False

    return True

def generar_motor_prometeus():
    d_libre = st.session_state.decena_libre
    vetadas = st.session_state.vetadas
    u_repetida = st.session_state.unidad_repetida
    
    # Decenas Dobles automáticas si el usuario eligió menos de 2
    d_dobles_actuales = list(st.session_state.dobles)
    opciones_disponibles = [k for k in TRAMOS.keys() if k != d_libre]
    while len(d_dobles_actuales) < 2:
        restantes = [o for o in opciones_disponibles if o not in d_dobles_actuales]
        if not restantes: break
        d_dobles_actuales.append(random.choice(restantes))
        
    d_simples_actuales = [o for o in opciones_disponibles if o not in d_dobles_actuales]

    apuestas_finales = []
    
    # Universo segregado para inyección directa ultrarrápida
    pool_por_decena = {}
    for dec, num_list in TRAMOS.items():
        pool_por_decena[dec] = [x for x in num_list if (x % 10) not in vetadas]

    # Ejecución en ráfaga controlada (Súper fluida)
    for num_apuesta in range(1, 5):
        encontrada = False
        intentos = 0
        
        while not encontrada and intentos < 4000:
            intentos += 1
            comb = []
            
            # Inyectar la geometría exacta de las decenas para que el cálculo vaya directo y sobrado
            for d in d_dobles_actuales:
                if len(pool_por_decena[d]) < 2: continue
                comb.extend(random.sample(pool_por_decena[d], 2))
            for d in d_simples_actuales:
                if len(pool_por_decena[d]) < 1: continue
                comb.extend(random.sample(pool_por_decena[d], 1))
                
            if len(comb) != 6: continue
            comb.sort()
            
            # Forzar controles de extracción requerida de las listas de recientes
            req_10 = sum(1 for x in comb if x in st.session_state.r10)
            req_15 = sum(1 for x in comb if x in st.session_state.r15)
            if req_10 != 1 or req_15 != 2: continue

            # Evaluar morfología del filtro
            if cumple_filtros_estrictos(comb, d_libre, d_dobles_actuales, u_repetida, vetadas, num_apuesta):
                # Cruzar con apuestas previas (Intersección Máxima de 1 Elemento)
                interseccion_ok = True
                for ap in apuestas_finales:
                    if len(set(comb).intersection(set(ap))) > 1:
                        interseccion_ok = False
                        break
                if interseccion_ok:
                    apuestas_finales.append(comb)
                    encontrada = True
                    
    return apuestas_finales

# ==========================================
# BLOQUE 5: ACCIÓN Y RESULTADOS
# ==========================================
st.markdown('<div class="seccion-titulo">🚀 Generador</div>', unsafe_allow_html=True)

# Mínimos obligatorios pactados para habilitar el botón
requisitos_ok = len(st.session_state.r10) >= 4 and len(st.session_state.r15) >= 8

if requisitos_ok:
    if st.button("🔥 GENERAR COMBINACIONES PROMETEUS", use_container_width=True, type="primary"):
        resultados = generar_motor_prometeus()
        
        if len(resultados) < 4:
            st.error("⚠️ Configuración altamente restrictiva. Haz click de nuevo en Generar o añade más números a las Parrillas de Recientes.")
        else:
            st.success("Cálculo estructural finalizado con éxito a alta velocidad.")
            for i, ap in enumerate(resultados):
                numeros_str = " ".join(f"{num:02d}" for num in ap)
                st.markdown(f"""
                <div class="apuesta-card">
                    <div class="apuesta-titulo">COMBINACIÓN MÚLTIPLE Nº{i+1}</div>
                    <div class="apuesta-numeros">{numeros_str}</div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.warning("🔒 El motor requiere una selección mínima de control en las parrillas superiores: selecciona al menos 4 números en Recientes 10 y 8 números en Recientes 15.")
