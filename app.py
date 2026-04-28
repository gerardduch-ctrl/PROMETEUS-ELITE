import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="Prometeus Elite", page_icon="🔥", layout="centered")

# --- ESTILS VISUALS (NO ES TOQUEN) ---
st.markdown("""
    <style>
    .stButton>button { height: 75px; font-size: 24px; font-weight: bold; border-radius: 15px; background-color: #FF4B4B; color: white; margin-top: 25px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2); width: 100%; }
    h3 { margin-top: 25px; color: #1E1E1E; border-bottom: 2px solid #FF4B4B; width: 100%; padding-bottom: 8px; font-family: 'Helvetica', sans-serif; }
    .desc-text { font-size: 14px; color: #555; margin-bottom: 10px; font-style: italic; line-height: 1.4; }
    div.row-widget.stRadio > div{ flex-direction:row; justify-content: center; gap: 8px; flex-wrap: wrap; }
    .stSuccess { font-size: 22px !important; font-weight: bold; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 PROMETEUS ELITE")
st.write("FULMINANT ULTIMATE EDITION - EUROMILLONES.")

# --- PANELLS DE CONFIGURACIÓ ---
st.markdown("### 1. Desenes")
st.markdown("<p class='desc-text'>Controla la densitat per grup. Tria quina desena vols que quedi totalment lliure (0 números) i quines dues vols carregar amb doble probabilitat (2 números cada una) per respectar el patró 2-2-1-1-0.</p>", unsafe_allow_html=True)
col_d1, col_d2 = st.columns(2)
with col_d1:
    st.write("**Decena Lliure (0)**")
    sel_decena_libre = st.radio("D_LL", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], horizontal=True, label_visibility="collapsed")
with col_d2:
    st.write("**Decenes Dobles (2)**")
    d_doble_1 = st.radio("D1", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], key="d1", horizontal=True, label_visibility="collapsed")
    d_doble_2 = st.radio("D2", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], key="d2", horizontal=True, label_visibility="collapsed")

st.markdown("### 2. Unitat Repetida")
st.markdown("<p class='desc-text'>Força terminacions dobles. Pots triar quina unitat (0-9) apareixerà exactament dues vegades en cada combinació.</p>", unsafe_allow_html=True)
sel_un_rep = st.radio("UR", ["Aleatori", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, label_visibility="collapsed")

st.markdown("### 3. Unitats Vetades")
st.markdown("<p class='desc-text'>Criba de terminacions prohibides. Elimina totalment de les teves apostes fins a 4 terminacions.</p>", unsafe_allow_html=True)
v1 = st.radio("V1", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v1")
v2 = st.radio("V2", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v2")
v3 = st.radio("V3", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v3")
v4 = st.radio("V4", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v4")

st.markdown("### 4. Filtre Mellizos")
sel_m_status = st.radio("M", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.markdown("### 5. Filtre Clumps")
sel_c_status = st.radio("C", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

# --- MOTOR D'ULTRA-PRECISIÓ ---
def generar_aposta(vetos, prohibits, d_lliure, d_doble1, d_doble2, u_repe, mells_on, clumps_on):
    tramos = [(1,10), (11,20), (21,30), (31,40), (41,50)]
    tramos_n = ["1-10", "11-20", "21-30", "31-40", "41-50"]
    mells_nums = {11, 22, 33, 44}

    for _ in range(50000): # Menys intents però més intel·ligents
        # 1. Triar desenes
        idx_ll = random.randint(0,4) if d_lliure == "Aleatori" else tramos_n.index(d_lliure)
        restants = [i for i in range(5) if i != idx_ll]
        
        idx_db = []
        for d in [d_doble1, d_doble2]:
            if d != "Aleatori": idx_db.append(tramos_n.index(d))
        idx_db = list(set(idx_db))
        while len(idx_db) < 2:
            nou = random.choice(restants)
            if nou not in idx_db: idx_db.append(nou)
        
        idx_si = [i for i in restants if i not in idx_db]
        
        # 2. Construir pools de números filtrats
        pools = []
        for i, qty in [(idx_db[0], 2), (idx_db[1], 2), (idx_si[0], 1), (idx_si[1], 1)]:
            p = [n for n in range(tramos[i][0], tramos[i][1]+1) if n % 10 not in vetos and n not in prohibits]
            if mells_on == "OFF": p = [n for n in p if n not in mells_nums]
            if len(p) < qty: return None # Aquest camí no és vàlid
            pools.append((p, qty))

        # 3. Generar combinació i validar
        comb = []
        for p, qty in pools:
            comb.extend(random.sample(p, qty))
        
        if sum(1 for n in comb if n % 2 == 0) != 3: continue
        
        # Unitat repetida
        terms = [n % 10 for n in comb]
        if u_repe != "Aleatori":
            if terms.count(u_repe) != 2: continue
        if len(set(terms)) != 5: continue # Garanteix exactament una parella de terminació
        
        # Mellizos exactes
        if mells_on == "ON" and len(set(comb) & mells_nums) != 1: continue
        
        # Clumps exactes
        comb.sort()
        seg = sum(1 for i in range(len(comb)-1) if comb[i+1] == comb[i]+1)
        if clumps_on == "ON" and seg != 1: continue
        if clumps_on == "OFF" and seg > 0: continue
            
        return comb
    return None

if st.button("🚀 GENERAR 2 APOSTES PROMETEUS ELITE"):
    vetos_final = list(set([v for v in [v1, v2, v3, v4] if v != "Cap"]))
    with st.spinner('Motor intel·ligent calculant...'):
        # El motor ara és tan ràpid que pot intentar milers de configuracions de desenes si cal
        exit_A = False
        for _ in range(100):
            aA = generar_aposta(vetos_final, [], sel_decena_libre, d_doble_1, d_doble_2, sel_un_rep, sel_m_status, sel_c_status)
            if aA:
                aB = generar_aposta(vetos_final, aA, sel_decena_libre, d_doble_1, d_doble_2, sel_un_rep, sel_m_status, sel_c_status)
                if aB:
                    st.markdown("### 🔮 Combinacions Resultants (12 inèdits)")
                    st.success(f"APOSTA A: {' - '.join(map(str, sorted(aA)))}")
                    st.success(f"APOSTA B: {' - '.join(map(str, sorted(aB)))}")
                    exit_A = True; break
        if not exit_A:
            st.error("⚠️ El sistema no troba 12 números inèdits amb aquests vetos. Prova de treure un veto d'unitat.")
