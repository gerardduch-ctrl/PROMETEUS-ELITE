
import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="Prometeus Elite", page_icon="🔥", layout="centered")

# --- ESTILS VISUALS (Minimalista) ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 60px; font-size: 20px; font-weight: bold; border-radius: 10px; background-color: #000000; color: white; border: 2px solid #FF4B4B; }
    h3 { color: #FF4B4B; border-bottom: 1px solid #ddd; padding-bottom: 5px; }
    .card { background-color: #f9f9f9; padding: 20px; border-radius: 15px; border-left: 5px solid #FF4B4B; margin-bottom: 20px; }
    .number-circle { display: inline-block; width: 40px; height: 40px; line-height: 40px; border-radius: 50%; background: #262730; color: white; text-align: center; margin: 4px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# IMAGEN PROMETEUS (Placeholder - Debes poner tu URL o archivo local)
# st.image("prometeus.png", width=150)
st.title("🔥 PROMETEUS ELITE")
st.write("SISTEMA ANDROID PARA EUROMILLONES")

# --- SELECTORES (INTERFAZ) ---
with st.expander("🛠️ CONFIGURACIÓN DE FILTROS", expanded=True):
    st.markdown("### Selector Decenas")
    # Tramos: 1-10, 11-20, 21-30, 31-40, 41-50
    dec_libre = st.selectbox("Decena LIBRE (0 números)", ["Aleatorio", "1-10", "11-20", "21-30", "31-40", "41-50"])
    dec_dobles = st.multiselect("Dos Decenas DOBLES (2 números c/u)", ["1-10", "11-20", "21-30", "31-40", "41-50"], max_selections=2)

    st.markdown("### Selector Unidades")
    u_repe = st.selectbox("Unidad que se REPITE", ["Aleatorio"] + list(range(10)))
    u_veto = st.multiselect("Unidades VETADAS (Máximo 4)", list(range(10)), max_selections=4)

    st.markdown("### Selectores Especiales")
    col1, col2 = st.columns(2)
    with col1:
        s_mellizos = st.checkbox("SELECTOR MELLIZOS (11, 22, 33, 44)")
    with col2:
        s_clumps = st.checkbox("SELECTOR CLUMPS (2 seguidos)")

# --- LÓGICA DE FILTRADO ---
def generar_combinacion(vetados, forbidden_nums, d_libre, d_dobles, u_repetida, mellizos_on, clumps_on):
    tramos = [(1,10), (11,20), (21,30), (31,40), (41,50)]
    tramos_nombres = ["1-10", "11-20", "21-30", "31-40", "41-50"]
    
    # 1. Definir patrón de decenas 2-2-1-1-0
    if d_libre == "Aleatorio":
        libre_idx = random.randint(0, 4)
    else:
        libre_idx = tramos_nombres.index(d_libre)
    
    restantes = [i for i in range(5) if i != libre_idx]
    
    if len(d_dobles) == 2:
        dobles_indices = [tramos_nombres.index(d) for d in d_dobles]
        simples_indices = [i for i in restantes if i not in dobles_indices]
    else:
        dobles_indices = random.sample(restantes, 2)
        simples_indices = [i for i in restantes if i not in dobles_indices]

    intentos = 0
    while intentos < 5000:
        intentos += 1
        comb = []
        
        # Generar números por decena según patrón
        for idx in dobles_indices:
            pool = [n for n in range(tramos[idx][0], tramos[idx][1]+1) if n % 10 not in vetados and n not in forbidden_nums]
            if len(pool) < 2: break
            comb.extend(random.sample(pool, 2))
        for idx in simples_indices:
            pool = [n for n in range(tramos[idx][0], tramos[idx][1]+1) if n % 10 not in vetados and n not in forbidden_nums]
            if len(pool) < 1: break
            comb.extend(random.sample(pool, 1))
        
        if len(comb) != 6: continue
        
        # Filtro Paridad (3P/3I)
        if sum(1 for n in comb if n % 2 == 0) != 3: continue
        
        # Filtro Unidades (Terminaciones)
        terminaciones = [n % 10 for n in comb]
        counts = {x: terminaciones.count(x) for x in set(terminaciones)}
        if list(counts.values()).count(2) != 1: continue # Solo una unidad repetida
        if u_repetida != "Aleatorio" and counts.get(u_repetida) != 2: continue

        # Filtro Mellizos (11, 22, 33, 44)
        mells = {11, 22, 33, 44}
        present_mells = [n for n in comb if n in mells]
        if mellizos_on:
            if len(present_mells) != 1: continue
        else:
            if len(present_mells) > 0: continue
            
        # Filtro Clumps (Seguidos)
        comb.sort()
        seguits = sum(1 for i in range(len(comb)-1) if comb[i+1] == comb[i]+1)
        if clumps_on:
            if seguits != 1: continue
        else:
            if seguits > 0: continue
            
        return comb
    return None

# --- BOTÓN GENERAR ---
if st.button("PROFETIZAR COMBINACIONES"):
    # Generar Apuesta A
    aA = generar_combinacion(u_veto, [], dec_libre, dec_dobles, u_repe, s_mellizos, s_clumps)
    
    if aA:
        # Generar Apuesta B (Inéditos respecto a A)
        aB = generar_combinacion(u_veto, aA, dec_libre, dec_dobles, u_repe, s_mellizos, s_clumps)
        
        if aB:
            st.markdown("### 🔮 RESULTADO PROMETEUS ELITE")
            
            for i, a in enumerate([aA, aB]):
                with st.container():
                    st.markdown(f"<div class='card'><b>COMBINACIÓN {chr(65+i)}</b><br>", unsafe_allow_html=True)
                    nums_html = "".join([f"<div class='number-circle'>{n}</div>" for n in sorted(a)])
                    st.markdown(nums_html, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("No se pudo generar la segunda apuesta inédita. Prueba a reducir vetos.")
    else:
        st.error("Combinación imposible con esos filtros. Revisa los vetos o las decenas.")

st.info("Reglas aplicadas: 12 números únicos, Paridad 3P/3I, Patrón Decenas 2-2-1-1-0.")
