import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="Prometeus Elite", page_icon="🔥", layout="centered")

# --- ESTILS VISUALS (INTACTES) ---
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
st.write("SISTEMA DE CÀLCUL AVANÇAT - MOTOR V3")

# --- PANELLS DE CONFIGURACIÓ (AMB DESCRIPCIONS) ---
st.markdown("### 1. Desenes")
st.markdown("<p class='desc-text'>Tria la desena lliure (0 números) i les dues dobles (2 números). El motor forçarà el patró 2-2-1-1-0.</p>", unsafe_allow_html=True)
col_d1, col_d2 = st.columns(2)
with col_d1:
    st.write("**Decena Lliure (0)**")
    sel_decena_libre = st.radio("D_LL", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], horizontal=True, label_visibility="collapsed")
with col_d2:
    st.write("**Decenes Dobles (2)**")
    d_doble_1 = st.radio("D1", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], key="d1", horizontal=True, label_visibility="collapsed")
    d_doble_2 = st.radio("D2", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], key="d2", horizontal=True, label_visibility="collapsed")

st.markdown("### 2. Unitat Repetida")
st.markdown("<p class='desc-text'>Força una terminació doble exacta per combinació.</p>", unsafe_allow_html=True)
sel_un_rep = st.radio("UR", ["Aleatori", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, label_visibility="collapsed")

st.markdown("### 3. Unitats Vetades")
st.markdown("<p class='desc-text'>Fins a 4 terminacions prohibides. El motor les extirpa abans de calcular.</p>", unsafe_allow_html=True)
v1 = st.radio("V1", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v1")
v2 = st.radio("V2", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v2")
v3 = st.radio("V3", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v3")
v4 = st.radio("V4", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v4")

st.markdown("### 4. Filtre Mellizos")
sel_m_status = st.radio("M", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.markdown("### 5. Filtre Clumps")
sel_c_status = st.radio("C", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

# --- MOTOR LÒGIC V3 (AGILE RECURSION) ---

def motor_elite(vetos, prohibits, d_ll, d_d1, d_d2, u_rep, mells_on, clumps_on):
    tramos = [(1,10), (11,20), (21,30), (31,40), (41,50)]
    tramos_n = ["1-10", "11-20", "21-30", "31-40", "41-50"]
    mells_nums = {11, 22, 33, 44}

    # El motor ho intenta 20.000 vegades per cada crida, però de forma molt optimitzada
    for _ in range(20000):
        # 1. Triar l'arquitectura de desenes
        ll_idx = random.randint(0,4) if d_ll == "Aleatori" else tramos_n.index(d_ll)
        rest = [i for i in range(5) if i != ll_idx]
        
        db_indices = []
        if d_d1 != "Aleatori": db_indices.append(tramos_n.index(d_d1))
        if d_d2 != "Aleatori": db_indices.append(tramos_n.index(d_d2))
        db_indices = list(set([i for i in db_indices if i != ll_idx]))
        
        while len(db_indices) < 2:
            opcio = random.choice(rest)
            if opcio not in db_indices: db_indices.append(opcio)
        
        si_indices = [i for i in rest if i not in db_indices]
        
        # 2. Assignació de números per bloc
        comb = []
        possible = True
        
        # Orde: Dobles primer, Simples després
        for idx in db_indices:
            p = [n for n in range(tramos[idx][0], tramos[idx][1]+1) if n % 10 not in vetos and n not in prohibits]
            if mells_on == "OFF": p = [n for n in p if n not in mells_nums]
            if len(p) < 2: possible = False; break
            comb.extend(random.sample(p, 2))
        
        if not possible: continue
            
        for idx in si_indices:
            p = [n for n in range(tramos[idx][0], tramos[idx][1]+1) if n % 10 not in vetos and n not in prohibits]
            if mells_on == "OFF": p = [n for n in p if n not in mells_nums]
            if len(p) < 1: possible = False; break
            comb.extend(random.sample(p, 1))
            
        if not possible or len(comb) != 6: continue

        # 3. Validació de filtres durs (Paritat i Unitats)
        if sum(1 for n in comb if n % 2 == 0) != 3: continue
        
        terms = [n % 10 for n in comb]
        if u_rep != "Aleatori":
            if terms.count(u_rep) != 2: continue
        if len(set(terms)) != 5: continue # Exactament una parella de repetició

        # 4. Validació de filtres especials
        if mells_on == "ON" and len(set(comb) & mells_nums) != 1: continue
        
        comb.sort()
        seg = sum(1 for i in range(len(comb)-1) if comb[i+1] == comb[i]+1)
        if clumps_on == "ON" and seg != 1: continue
        if clumps_on == "OFF" and seg > 0: continue
            
        return comb
    return None

# --- EXECUCIÓ ---
if st.button("🚀 EXECUTAR PROMETEUS ELITE"):
    vetos_final = list(set([v for v in [v1, v2, v3, v4] if v != "Cap"]))
    
    with st.spinner('Motor V3 analitzant probabilitats...'):
        success = False
        # El gran canvi: si la B falla, canvia la A també per evitar bloquejos terminatius
        for intent_global in range(500): 
            res_A = motor_elite(vetos_final, [], sel_decena_libre, d_doble_1, d_doble_2, sel_un_rep, sel_m_status, sel_c_status)
            if res_A:
                res_B = motor_elite(vetos_final, res_A, sel_decena_libre, d_doble_1, d_doble_2, sel_un_rep, sel_m_status, sel_c_status)
                if res_B:
                    st.markdown("### 🔮 Combinacions Resultants (12 Inèdits)")
                    st.success(f"APOSTA A: {' - '.join(map(str, sorted(res_A)))}")
                    st.success(f"APOSTA B: {' - '.join(map(str, sorted(res_B)))}")
                    success = True
                    break
        
        if not success:
            st.error("⚠️ Bloqueig lògic detectat. El motor no ha trobat 12 números inèdits amb aquests vetos. Prova de reduir els vetos d'unitats.")
