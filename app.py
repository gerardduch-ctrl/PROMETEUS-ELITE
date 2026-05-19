import streamlit as st
import random
import itertools

# Configuración de página optimizada para móvil
st.set_page_config(
    page_title="PROMETEUS ELITE",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Limpios y Minimalistas
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
    .apuesta-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 12px;
        border-left: 5px solid #00E676;
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
    div[data-testid="stHorizontalBlock"] {
        gap: 4px !important;
    }
    </style>
""", unsafe_allow_html=True)

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

if "recientes_10" not in st.session_state: st.session_state.recientes_10 = []
if "recientes_15" not in st.session_state: st.session_state.recientes_15 = []
if "decena_libre" not in st.session_state: st.session_state.decena_libre = "1-10"
if "decenas_dobles" not in st.session_state: st.session_state.decenas_dobles = []
if "unidad_repetida" not in st.session_state: st.session_state.unidad_repetida = 4
if "unidades_vetadas" not in st.session_state: st.session_state.unidades_vetadas = []

# --- PARRILLAS RECIENTES ---
st.subheader("📊 Entrada de Resultados Recientes")
st.markdown("**Parrilla Recientes 10** (Máx. 10 números - 1 por apuesta)")
for i in range(5):
    cols = st.columns(10)
    for j in range(10):
        num = i * 10 + j + 1
        disabled = num in st.session_state.recientes_15
        is_selected = num in st.session_state.recientes_10
        label = f"★ {num}" if is_selected else str(num)
        if cols[j].button(label, key=f"r10_{num}", disabled=disabled, use_container_width=True):
            if num in st.session_state.recientes_10: st.session_state.recientes_10.remove(num)
            elif len(st.session_state.recientes_10) < 10: st.session_state.recientes_10.append(num)
            st.rerun()

st.markdown("**Parrilla Recientes 15** (Máx. 15 números - 2 por apuesta)")
for i in range(5):
    cols = st.columns(10)
    for j in range(10):
        num = i * 10 + j + 1
        disabled = num in st.session_state.recientes_10
        is_selected = num in st.session_state.recientes_15
        label = f"★ {num}" if is_selected else str(num)
        if cols[j].button(label, key=f"r15_{num}", disabled=disabled, use_container_width=True):
            if num in st.session_state.recientes_15: st.session_state.recientes_15.remove(num)
            elif len(st.session_state.recientes_15) < 15: st.session_state.recientes_15.append(num)
            st.rerun()

st.markdown("---")

# --- CONTROL DE DECENAS ---
st.subheader("🔢 Parámetros de Decenas")
st.markdown("**Selector Decena Libre** (Opción única)")
cols_dl = st.columns(5)
for idx, dec in enumerate(TRAMOS_DECENAS.keys()):
    is_libre = st.session_state.decena_libre == dec
    label = f"★ 🚫 {dec}" if is_libre else dec
    if cols_dl[idx].button(label, key=f"dl_{dec}", use_container_width=True):
        st.session_state.decena_libre = dec
        if dec in st.session_state.decenas_dobles: st.session_state.decenas_dobles.remove(dec)
        st.rerun()

st.markdown("**Selector Decenas Dobles** (Máx. 2 tramos)")
cols_dd = st.columns(5)
for idx, dec in enumerate(TRAMOS_DECENAS.keys()):
    disabled = dec == st.session_state.decena_libre
    is_doble = dec in st.session_state.decenas_dobles
    label = f"★ ⭐ {dec}" if is_doble else dec
    if cols_dd[idx].button(label, key=f"dd_{dec}", disabled=disabled, use_container_width=True):
        if dec in st.session_state.decenas_dobles: st.session_state.decenas_dobles.remove(dec)
        elif len(st.session_state.decenas_dobles) < 2: st.session_state.decenas_dobles.append(dec)
        st.rerun()

st.markdown("---")

# --- CONTROL DE UNIDADES ---
st.subheader("🎯 Parámetros de Unidades (Terminaciones)")
st.markdown("**Selector Unidad Repetida** (Opción única)")
cols_ur = st.columns(10)
for u in range(10):
    is_rep = st.session_state.unidad_repetida == u
    label = f"★ {u}" if is_rep else str(u)
    if cols_ur[u].button(label, key=f"ur_{u}", use_container_width=True):
        st.session_state.unidad_repetida = u
        if u in st.session_state.unidades_vetadas: st.session_state.unidades_vetadas.remove(u)
        st.rerun()

st.markdown("**Selector Unidad Vetada** (Máx. 2 unidades)")
cols_uv = st.columns(10)
for u in range(10):
    disabled = u == st.session_state.unidad_repetida
    is_vetada = u in st.session_state.unidades_vetadas
    label = f"★ ❌ {u}" if is_vetada else str(u)
    if cols_uv[u].button(label, key=f"uv_{u}", disabled=disabled, use_container_width=True):
        if u in st.session_state.unidades_vetadas: st.session_state.unidades_vetadas.remove(u)
        elif len(st.session_state.unidades_vetadas) < 2: st.session_state.unidades_vetadas.append(u)
        st.rerun()

st.markdown("---")

# --- FILTROS ESPECIALES ---
st.subheader("⚙️ Filtros Especiales")
c1, c2 = st.columns(2)
activar_mellizos = c1.radio("Selector Mellizos", ["NO", "SÍ"], index=0) == "SÍ"
activar_clumps = c2.radio("Selector Clumps", ["NO", "SÍ"], index=0) == "SÍ"

st.markdown("---")

# --- ASISTENTES DE FILTRADO VELOZ ---
def obtener_decena(num):
    if 1 <= num <= 10: return "1-10"
    if 11 <= num <= 20: return "11-20"
    if 21 <= num <= 30: return "21-30"
    if 31 <= num <= 40: return "31-40"
    if 41 <= num <= 50: return "41-50"
    return None

def validar_paridad(comb):
    return sum(1 for n in comb if n % 2 == 0) == 3

def validar_unidades(comb, u_rep, u_vet):
    terms = [n % 10 for n in comb]
    if any(u in u_vet for u in terms): return False
    if terms.count(u_rep) != 2: return False
    restantes = [t for t in terms if t != u_rep]
    return len(set(restantes)) == len(restantes)

def tiene_consecutivos(comb):
    sc = sorted(comb)
    return any(sc[i+1] - sc[i] == 1 for i in range(len(sc)-1))

def contar_consecutivos(comb):
    sc = sorted(comb)
    parejas = 0
    i = 0
    while i < len(sc) - 1:
        if sc[i+1] - sc[i] == 1:
            parejas += 1
            i += 2
        else:
            i += 1
    return parejas

# --- BOTÓN DE GENERACIÓN MULTI-MATRICIAL ---
if st.button("⚡ GENERAR COMBINACIONES PROMETEUS", use_container_width=True, type="primary"):
    
    # Universo Limpio de Raíz
    universo_valido = []
    for n in range(1, 51):
        if obtener_decena(n) == st.session_state.decena_libre: continue
        if n % 10 in st.session_state.unidades_vetadas: continue
        universo_valido.append(n)

    r10_limpio = [n for n in st.session_state.recientes_10 if n in universo_valido]
    r15_limpio = [n for n in st.session_state.recientes_15 if n in universo_valido]

    decenas_restantes = [d for d in TRAMOS_DECENAS.keys() if d != st.session_state.decena_libre]
    
    # BANCOS MATRICIALES INDEPENDIENTES POR APUESTA
    banco_ap1, banco_ap2, banco_ap3, banco_ap4 = [], [], [], []
    
    # Pre-generar un pool masivo de combinaciones válidas individuales (Fuerza Bruta Tipo Pool)
    for _ in range(30000):
        # Resolver decenas dinámicas si el usuario puso menos de 2
        if len(st.session_state.decenas_dobles) == 2:
            dobles_apuesta = st.session_state.decenas_dobles
        elif len(st.session_state.decenas_dobles) == 1:
            opciones_validas = [d for d in decenas_restantes if d not in st.session_state.decenas_dobles]
            dobles_apuesta = st.session_state.decenas_dobles + [random.choice(opciones_validas)]
        else:
            dobles_apuesta = random.sample(decenas_restantes, 2)
            
        simples_apuesta = [d for d in decenas_restantes if d not in dobles_apuesta]
        
        # Construcción directa de base
        apuesta = set()
        candidatos_u_rep = [n for n in universo_valido if n % 10 == st.session_state.unidad_repetida]
        if len(candidatos_u_rep) >= 2:
            apuesta.update(random.sample(candidatos_u_rep, 2))
        else:
            continue
            
        # Inyectar un Reciente 10 y dos Recientes 15 de manera aleatoria si existen
        if r10_limpio: apuesta.add(random.choice(r10_limpio))
        if r15_limpio: apuesta.update(random.sample(r15_limpio, min(len(r15_limpio), 2)))
        if len(apuesta) > 6: continue
            
        # Rellenar tramo por tramo
        lista_cand = list(apuesta)
        for dec in dobles_apuesta:
            nums = [n for n in universo_valido if obtener_decena(n) == dec and n not in lista_cand]
            random.shuffle(nums)
            while sum(1 for x in lista_cand if obtener_decena(x) == dec) < 2 and nums:
                lista_cand.append(nums.pop())
        for dec in simples_apuesta:
            nums = [n for n in universo_valido if obtener_decena(n) == dec and n not in lista_cand]
            random.shuffle(nums)
            while sum(1 for x in lista_cand if obtener_decena(x) == dec) < 1 and nums:
                lista_cand.append(nums.pop())
                
        if len(lista_cand) != 6: continue
        
        # Filtrado morfológico instantáneo
        conteos_dec = {d: 0 for d in TRAMOS_DECENAS.keys()}
        for n in lista_cand: conteos_dec[obtener_decena(n)] += 1
        if sum(1 for d in dobles_apuesta if conteos_dec[d] == 2) != 2: continue
        if not validar_paridad(lista_cand): continue
        if not validar_unidades(lista_cand, st.session_state.unidad_repetida, st.session_state.unidades_vetadas): continue
        
        # Clasificar la combinación en el banco correcto según Mellizos y Clumps
        cont_m = sum(1 for n in lista_cand if n in MELLIZOS)
        has_c = tiene_consecutivos(lista_cand)
        num_c = contar_consecutivos(lista_cand)
        
        # Clasificación Matricial Directa
        if activar_mellizos:
            if cont_m == 0 and not has_c: banco_ap1.append(sorted(lista_cand))
            if cont_m == 1 and not has_c: banco_ap2.append(sorted(lista_cand))
            if activar_clumps:
                if cont_m == 0 and num_c == 1: banco_ap3.append(sorted(lista_cand))
                if cont_m == 1 and num_c == 1: banco_ap4.append(sorted(lista_cand))
            else:
                if cont_m == 0 and not has_c: banco_ap3.append(sorted(lista_cand))
                if cont_m == 1 and not has_c: banco_ap4.append(sorted(lista_cand))
        else:
            if cont_m == 0:
                if activar_clumps:
                    if not has_c: banco_ap1.append(sorted(lista_cand))
                    if not has_c: banco_ap2.append(sorted(lista_cand))
                    if num_c == 1: banco_ap3.append(sorted(lista_cand))
                    if num_c == 1: banco_ap4.append(sorted(lista_cand))
                else:
                    if not has_c:
                        c_sorted = sorted(lista_cand)
                        banco_ap1.append(c_sorted)
                        banco_ap2.append(c_sorted)
                        banco_ap3.append(c_sorted)
                        banco_ap4.append(c_sorted)

    # --- FUERZA BRUTA DE INTERSECCIÓN CRUZADA ALTA VELOCIDAD ---
    exito = False
    apuestas_finales = []
    
    # Comprobar que ningún banco esté vacío debido a restricciones manuales incompatibles
    if banco_ap1 and banco_ap2 and banco_ap3 and banco_ap4:
        # Ejecuta hasta 5.000.000 de cruces indexados en milisegundos
        for intento_cruce in range(5000000):
            ap1 = random.choice(banco_ap1)
            ap2 = random.choice(banco_ap2)
            if len(set(ap1) & set(ap2)) > 1: continue
                
            ap3 = random.choice(banco_ap3)
            if len(set(ap1) & set(ap3)) > 1 or len(set(ap2) & set(ap3)) > 1: continue
                
            ap4 = random.choice(banco_ap4)
            if len(set(ap1) & set(ap4)) > 1 or len(set(ap2) & set(ap4)) > 1 or len(set(ap3) & set(ap4)) > 1: continue
                
            apuestas_finales = [ap1, ap2, ap3, ap4]
            exito = True
            break

    # --- RENDERIZADO ---
    if exito:
        st.success("🎯 Combinaciones PROMETEUS generadas con éxito instantáneo:")
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
        st.error("❌ Conflicto combinatorio. Has seleccionado números en 'Recientes' o parámetros de unidades que rompen las leyes de paridad o decenas. Cambia algún número marcado e intenta de nuevo.")
