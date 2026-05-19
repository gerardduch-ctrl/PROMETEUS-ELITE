import streamlit as st
import random

# Configuración de página optimizada para móvil
st.set_page_config(
    page_title="PROMETEUS ELITE",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS radicales para garantizar visualización perfecta en móviles Android
st.markdown("""
    <style>
    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Título y subtítulos */
    .main-title {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #FFFFFF;
        text-align: center;
        font-weight: 800;
        font-size: 32px;
        letter-spacing: 2px;
        margin-bottom: 2px;
    }
    .subtitle {
        text-align: center;
        color: #888888;
        font-size: 14px;
        margin-bottom: 30px;
    }
    
    /* Botones Numéricos de las Parrillas por defecto */
    .stButton > button {
        border-radius: 6px !important;
        padding: 4px 0px !important;
        font-size: 14px !important;
        font-weight: bold !important;
        height: 38px !important;
        background-color: #262626 !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    
    /* FORZAR COLOR ROJO RADICAL PARA ELEMENTOS SELECCIONADOS */
    div.st_seleccionado button {
        background-color: #FF1744 !important; /* Rojo Intenso */
        color: #FFFFFF !important;            /* Texto Blanco */
        border: 2px solid #FFFFFF !important;  /* Borde Blanco */
        box-shadow: 0px 0px 12px #FF1744 !important; /* Resplandor Rojo */
    }
    
    /* Forzar que el texto interno del botón seleccionado también sea blanco en móvil */
    div.st_seleccionado button p {
        color: #FFFFFF !important;
        font-weight: 900 !important;
    }
    
    /* Tarjetas de resultados */
    .apuesta-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
        border-left: 5px solid #FF1744;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
    }
    .apuesta-titulo {
        font-size: 14px;
        color: #888888;
        margin-bottom: 5px;
        font-weight: bold;
    }
    .apuesta-numeros {
        font-size: 24px;
        font-weight: bold;
        color: #FFFFFF;
        letter-spacing: 4px;
    }
    
    /* Optimización de rejillas horizontales en móviles */
    div[data-testid="stHorizontalBlock"] {
        gap: 3px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown('<div class="main-title">PROMETEUS ELITE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">SISTEMA DE CRIBA MULTIPLE PARA EUROMILLONES</div>', unsafe_allow_html=True)

TRAMOS_DECENAS = {
    "1-10": list(range(1, 11)),
    "11-20": list(range(11, 21)),
    "21-30": list(range(21, 31)),
    "31-40": list(range(31, 41)),
    "41-50": list(range(41, 51))
}
MELLIZOS = [11, 22, 33, 44]

# --- INICIALIZACIÓN DE ESTADOS ---
if "recientes_10" not in st.session_state: st.session_state.recientes_10 = []
if "recientes_15" not in st.session_state: st.session_state.recientes_15 = []
if "decena_libre" not in st.session_state: st.session_state.decena_libre = "1-10"
if "decenas_dobles" not in st.session_state: st.session_state.decenas_dobles = []
if "unidad_repetida" not in st.session_state: st.session_state.unidad_repetida = 4
if "unidades_vetadas" not in st.session_state: st.session_state.unidades_vetadas = []

# --- BLOQUE 1: PARRILLAS RECIENTES ---
st.subheader("📊 Entrada de Resultados Recientes")

st.markdown(f"**Parrilla Recientes 10** (Seleccionados: {len(st.session_state.recientes_10)}/10)")
for i in range(5):
    cols = st.columns(10)
    for j in range(10):
        num = i * 10 + j + 1
        disabled = num in st.session_state.recientes_15
        is_selected = num in st.session_state.recientes_10
        
        if is_selected:
            with cols[j]:
                st.markdown('<div class="st_seleccionado">', unsafe_allow_html=True)
                if st.button(f"{num}", key=f"r10_{num}", disabled=disabled, use_container_width=True):
                    st.session_state.recientes_10.remove(num)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            if cols[j].button(f"{num}", key=f"r10_{num}", disabled=disabled, use_container_width=True):
                if len(st.session_state.recientes_10) < 10:
                    st.session_state.recientes_10.append(num)
                    st.rerun()

st.markdown(f"**Parrilla Recientes 15** (Seleccionados: {len(st.session_state.recientes_15)}/15)")
for i in range(5):
    cols = st.columns(10)
    for j in range(10):
        num = i * 10 + j + 1
        disabled = num in st.session_state.recientes_10
        is_selected = num in st.session_state.recientes_15
        
        if is_selected:
            with cols[j]:
                st.markdown('<div class="st_seleccionado">', unsafe_allow_html=True)
                if st.button(f"{num}", key=f"r15_{num}", disabled=disabled, use_container_width=True):
                    st.session_state.recientes_15.remove(num)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            if cols[j].button(f"{num}", key=f"r15_{num}", disabled=disabled, use_container_width=True):
                if len(st.session_state.recientes_15) < 15:
                    st.session_state.recientes_15.append(num)
                    st.rerun()

st.markdown("---")

# --- BLOQUE 2: CONTROL DE DECENAS ---
st.subheader("🔢 Parámetros de Decenas")

st.markdown("**Selector Decena Libre** (Opción única)")
cols_dl = st.columns(5)
for idx, dec in enumerate(TRAMOS_DECENAS.keys()):
    is_libre = st.session_state.decena_libre == dec
    if is_libre:
        with cols_dl[idx]:
            st.markdown('<div class="st_seleccionado">', unsafe_allow_html=True)
            st.button(f"🚫 {dec}", key=f"dl_{dec}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        if cols_dl[idx].button(dec, key=f"dl_{dec}", use_container_width=True):
            st.session_state.decena_libre = dec
            if dec in st.session_state.decenas_dobles:
                st.session_state.decenas_dobles.remove(dec)
            st.rerun()

st.markdown("**Selector Decenas Dobles** (Máx. 2 tramos)")
cols_dd = st.columns(5)
for idx, dec in enumerate(TRAMOS_DECENAS.keys()):
    disabled = dec == st.session_state.decena_libre
    is_doble = dec in st.session_state.decenas_dobles
    
    if is_doble:
        with cols_dd[idx]:
            st.markdown('<div class="st_seleccionado">', unsafe_allow_html=True)
            if st.button(f"⭐ {dec}", key=f"dd_{dec}", disabled=disabled, use_container_width=True):
                st.session_state.decenas_dobles.remove(dec)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        if cols_dd[idx].button(dec, key=f"dd_{dec}", disabled=disabled, use_container_width=True):
            if len(st.session_state.decenas_dobles) < 2:
                st.session_state.decenas_dobles.append(dec)
                st.rerun()

st.markdown("---")

# --- BLOQUE 3: CONTROL DE UNIDADES ---
st.subheader("🎯 Parámetros de Unidades (Terminaciones)")

st.markdown("**Selector Unidad Repetida** (Opción única)")
cols_ur = st.columns(10)
for u in range(10):
    is_rep = st.session_state.unidad_repetida == u
    if is_rep:
        with cols_ur[u]:
            st.markdown('<div class="st_seleccionado">', unsafe_allow_html=True)
            st.button(f"✨ {u}", key=f"ur_{u}", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        if cols_ur[u].button(str(u), key=f"ur_{u}", use_container_width=True):
            st.session_state.unidad_repetida = u
            if u in st.session_state.unidades_vetadas:
                st.session_state.unidades_vetadas.remove(u)
            st.rerun()

st.markdown("**Selector Unidad Vetada** (Máx. 2 unidades)")
cols_uv = st.columns(10)
for u in range(10):
    disabled = u == st.session_state.unidad_repetida
    is_vetada = u in st.session_state.unidades_vetadas
    
    if is_vetada:
        with cols_uv[u]:
            st.markdown('<div class="st_seleccionado">', unsafe_allow_html=True)
            if st.button(f"❌ {u}", key=f"uv_{u}", disabled=disabled, use_container_width=True):
                st.session_state.unidades_vetadas.remove(u)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        if cols_uv[u].button(str(u), key=f"uv_{u}", disabled=disabled, use_container_width=True):
            if len(st.session_state.unidades_vetadas) < 2:
                st.session_state.unidades_vetadas.append(u)
                st.rerun()

st.markdown("---")

# --- BLOQUE 4: INTERRUPTORES ESPECIALES ---
st.subheader("⚙️ Filtros Especiales")
c1, c2 = st.columns(2)
activar_mellizos = c1.radio("Selector Mellizos", ["NO", "SÍ"], index=0) == "SÍ"
activar_clumps = c2.radio("Selector Clumps", ["NO", "SÍ"], index=0) == "SÍ"

st.markdown("---")

# --- MOTOR DE GENERACIÓN MATEMÁTICA ---
def validar_paridad(combinacion):
    pares = sum(1 for n in combinacion if n % 2 == 0)
    return pares == 3

def obtener_decena(num):
    if 1 <= num <= 10: return "1-10"
    if 11 <= num <= 20: return "11-20"
    if 21 <= num <= 30: return "21-30"
    if 31 <= num <= 40: return "31-40"
    if 41 <= num <= 50: return "41-50"
    return None

def validar_unidades(combinacion, u_repetida, u_vetadas):
    terminaciones = [n % 10 for n in combinacion]
    if any(u in u_vetadas for u in terminaciones):
        return False
    if terminaciones.count(u_repetida) != 2:
        return False
    restantes = [t for t in terminaciones if t != u_repetida]
    return len(set(restantes)) == len(restantes)

def tiene_consecutivos(combinacion):
    sorted_comb = sorted(combinacion)
    for i in range(len(sorted_comb) - 1):
        if sorted_comb[i+1] - sorted_comb[i] == 1:
            return True
    return False

def contar_consecutivos(combinacion):
    sorted_comb = sorted(combinacion)
    parejas = 0
    i = 0
    while i < len(sorted_comb) - 1:
        if sorted_comb[i+1] - sorted_comb[i] == 1:
            parejas += 1
            i += 2
        else:
            i += 1
    return parejas

def cumplir_interseccion(nuevas_apuestas):
    for i in range(len(nuevas_apuestas)):
        for j in range(i + 1, len(nuevas_apuestas)):
            interseccion = set(nuevas_apuestas[i]) & set(nuevas_apuestas[j])
            if len(interseccion) > 1:
                return False
    return True

# --- BOTÓN DE GENERACIÓN ---
if st.button("⚡ GENERAR COMBINACIONES PROMETEUS", use_container_width=True, type="primary"):
    
    universo_valido = []
    for n in range(1, 51):
        dec_n = obtener_decena(n)
        uni_n = n % 10
        if dec_n == st.session_state.decena_libre: continue
        if uni_n in st.session_state.unidades_vetadas: continue
        universo_valido.append(n)
        
    r10_limpio = [n for n in st.session_state.recientes_10 if n in universo_valido]
    r15_limpio = [n for n in st.session_state.recientes_15 if n in universo_valido]
    resto_universo = [n for n in universo_valido if n not in r10_limpio and n not in r15_limpio]
    
    apuestas_finales = []
    intentos_globales = 0
    exito = False
    
    while intentos_globales < 8000 and not exito:
        apuestas_finales = []
        decenas_restantes = [d for d in TRAMOS_DECENAS.keys() if d != st.session_state.decena_libre]
        
        for num_apuesta in [1, 2, 3, 4]:
            if len(st.session_state.decenas_dobles) == 2:
                dobles_apuesta = st.session_state.decenas_dobles
            elif len(st.session_state.decenas_dobles) == 1:
                opciones_extra = [d for d in decenas_restantes if d != st.session_state.decenas_dobles]
                dobles_apuesta = st.session_state.decenas_dobles + [random.choice(opciones_extra)]
            else:
                dobles_apuesta = random.sample(decenas_restantes, 2)
                
            simples_apuesta = [d for d in decenas_restantes if d not in dobles_apuesta]
            
            apuesta_valida = None
            for _ in range(3000):
                apuesta = []
                
                n10 = random.choice(r10_limpio) if r10_limpio else None
                n15 = random.sample(r15_limpio, min(len(r15_limpio), 2)) if r15_limpio else []
                
                bolsa_llenado = [n for n in resto_universo]
                random.shuffle(bolsa_llenado)
                
                comb_candidata = []
                if n10: comb_candidata.append(n10)
                comb_candidata.extend(n15)
                
                for n in bolsa_llenado:
                    if len(comb_candidata) >= 6: break
                    dec = obtener_decena(n)
                    actuales_dec = sum(1 for x in comb_candidata if obtener_decena(x) == dec)
                    
                    if dec in dobles_apuesta and actuales_dec < 2:
                        comb_candidata.append(n)
                    elif dec in simples_apuesta and actuales_dec < 1:
                        comb_candidata.append(n)
                
                if len(comb_candidata) < 6: continue
                comb = comb_candidata[:6]
                
                if not validar_paridad(comb): continue
                
                conteos_dec = {d: 0 for d in TRAMOS_DECENAS.keys()}
                for n in comb:
                    conteos_dec[obtener_decena(n)] += 1
                
                if conteos_dec[st.session_state.decena_libre] != 0: continue
                if sum(1 for d in dobles_apuesta if conteos_dec[d] == 2) != 2: continue
                if sum(1 for d in simples_apuesta if conteos_dec[d] == 1) != 2: continue
                
                if not validar_unidades(comb, st.session_state.unidad_repetida, st.session_state.unidades_vetadas): continue
                
                mellizos_en_comb = [n for n in comb if n in MELLIZOS]
                if activar_mellizos:
                    if num_apuesta in [2, 4]:
                        if len(mellizos_en_comb) != 1: continue
                    else:
                        if len(mellizos_en_comb) != 0: continue
                else:
                    if len(mellizos_en_comb) != 0: continue
                    
                if activar_clumps:
                    if num_apuesta in [3, 4]:
                        if contar_consecutivos(comb) != 1: continue
                    else:
                        if tiene_consecutivos(comb): continue
                else:
                    if tiene_consecutivos(comb): continue
                
                apuesta_valida = sorted(comb)
                break
            
            if apuesta_valida:
                apuestas_finales.append(apuesta_valida)
            else:
                break
                
        if len(apuestas_finales) == 4 and cumplir_interseccion(apuestas_finales):
            exito = True
            break
        intentos_globales += 1

    # --- RENDERIZADO DE RESULTADOS ---
    if exito:
        st.success("🎯 Combinaciones generadas con éxito:")
        for idx, ap in enumerate(apuestas_finales, 1):
            clump_tag = " 🔸 [Clump]" if idx in [3, 4] and activar_clumps else ""
            mellizo_tag = " 🔹 [Mellizo]" if idx in [2, 4] and activar_mellizos else ""
            
            st.markdown(f"""
            <div class="apuesta-card">
                <div class="apuesta-titulo">APUESTA MULTIPLE {idx}{mellizo_tag}{clump_tag}</div>
                <div class="apuesta-numeros">{" · ".join(f"{n:02d}" for n in ap)}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("❌ Configuración imposible. Relaje algún filtro o veto para generar las apuestas.")
