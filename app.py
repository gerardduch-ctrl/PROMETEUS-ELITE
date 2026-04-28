import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="Prometeus Elite", page_icon="🔥", layout="centered")

# --- ESTILS VISUALS ---
st.markdown("""
    <style>
    .stButton>button { height: 75px; font-size: 24px; font-weight: bold; border-radius: 15px; background-color: #FF4B4B; color: white; margin-top: 25px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2); width: 100%; }
    h3 { margin-top: 25px; color: #1E1E1E; border-bottom: 2px solid #FF4B4B; width: 100%; padding-bottom: 8px; font-family: 'Helvetica', sans-serif; }
    .desc-text { font-size: 14px; color: #555; margin-bottom: 10px; font-style: italic; line-height: 1.4; }
    div.row-widget.stRadio > div{ flex-direction:row; justify-content: center; gap: 8px; flex-wrap: wrap; }
    .stSuccess { font-size: 22px !important; font-weight: bold; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    .veto-label { font-size: 12px; color: #888; text-align: center; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔥 PROMETEUS ELITE")
st.write("SISTEMA ANDROID EXCLUSIU PER A EUROMILLONES.")

# --- PANELLS DE CONFIGURACIÓ DESPLEGATS ---

st.markdown("### 1. Selector Decena Lliure (0 números)")
sel_decena_libre = st.radio("D_LL", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], horizontal=True, label_visibility="collapsed")

st.markdown("### 2. Selector Decenes Dobles (2 números c/u)")
st.markdown("<p class='desc-text'>Tria les dues desenes que vols forçar amb 2 números.</p>", unsafe_allow_html=True)
col_d1, col_d2 = st.columns(2)
with col_d1:
    d_doble_1 = st.radio("D1", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], key="d1", horizontal=True)
with col_d2:
    d_doble_2 = st.radio("D2", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], key="d2", horizontal=True)

st.markdown("### 3. Selector Unidad Repetida")
sel_un_rep = st.radio("UR", ["Aleatori", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, label_visibility="collapsed")

st.markdown("### 4. Selector Unitats Vetades")
st.markdown("<p class='desc-text'>Veta fins a 4 terminacions completes.</p>", unsafe_allow_html=True)
v1 = st.radio("V1", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v1")
v2 = st.radio("V2", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v2")
v3 = st.radio("V3", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v3")
v4 = st.radio("V4", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v4")

st.markdown("### 5. Filtres Especials (Mellizos i Clumps)")
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.write("**Mellizos**")
    sel_m_status = st.radio("M", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")
with col_f2:
    st.write("**Clumps**")
    sel_c_status = st.radio("C", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.divider()

# --- MOTOR LÒGIC (500k INTENTS) ---

def generar_aposta(vetos, prohibits, d_lliure, d_doble1, d_doble2, u_repe, mells_on, clumps_on):
    tramos = [(1,10), (11,20), (21,30), (31,40), (41,50)]
    tramos_n = ["1-10", "11-20", "21-30", "31-40", "41-50"]
    
    for _ in range(500000): 
        # 1. Definir l'esquema de desenes
        idx_lliure = random.randint(0,4) if d_lliure == "Aleatori" else tramos_n.index(d_lliure)
        restants = [i for i in range(5) if i != idx_lliure]
        
        idx_dobles = []
        if d_doble1 != "Aleatori": idx_dobles.append(tramos_n.index(d_doble1))
        if d_doble2 != "Aleatori": idx_dobles.append(tramos_n.index(d_doble2))
        
        # Omplir dobles si falten o si coincideixen (garantir 2 dobles diferents)
        idx_dobles = list(set(idx_dobles))
        while len(idx_dobles) < 2:
            nou_idx = random.choice(restants)
            if nou_idx not in idx_dobles: idx_dobles.append(nou_idx)
        
        idx_simples = [i for i in restants if i not in idx_dobles]
            
        comb = []
        possible = True
        for idx in idx_dobles:
            p = [n for n in range(tramos[idx][0], tramos[idx][1]+1) if n % 10 not in vetos and n not in prohibits]
            if len(p) < 2: possible = False; break
            comb.extend(random.sample(p, 2))
        for idx in idx_simples:
            p = [n for n in range(tramos[idx][0], tramos[idx][1]+1) if n % 10 not in vetos and n not in prohibits]
            if len(p) < 1: possible = False; break
            comb.extend(random.sample(p, 1))
            
        if not possible or len(comb) != 6: continue
        if sum(1 for n in comb if n % 2 == 0) != 3: continue
        
        terms = [n % 10 for n in comb]
        counts = {x: terms.count(x) for x in set(terms)}
        if list(counts.values()).count(2) != 1: continue 
        if u_repe != "Aleatori" and counts.get(u_repe) != 2: continue
        
        mells = {11, 22, 33, 44}
        p_mells = [n for n in comb if n in mells]
        if mells_on == "ON":
            if len(p_mells) != 1: continue
            if any(n % 10 in vetos for n in p_mells): continue
        else:
            if len(p_mells) > 0: continue
            
        comb.sort()
        seg = sum(1 for i in range(len(comb)-1) if comb[i+1] == comb[i]+1)
        if clumps_on == "ON":
            if seg != 1: continue
        else:
            if seg > 0: continue
            
        return comb
    return None

# --- BOTÓ I RESULTATS ---
if st.button("🚀 GENERAR APOSTES PROMETEUS ELITE"):
    vetos_final = [v for v in [v1, v2, v3, v4] if v != "Cap"]
    with st.spinner('Cribrant 500.000 combinacions...'):
        aA = generar_aposta(vetos_final, [], sel_decena_libre, d_doble_1, d_doble_2, sel_un_rep, sel_m_status, sel_c_status)
        if aA:
            aB = generar_aposta(vetos_final, aA, sel_decena_libre, d_doble_1, d_doble_2, sel_un_rep, sel_m_status, sel_c_status)
            if aB:
                st.markdown("### 🔮 Combinacions Resultants (12 inèdits)")
                st.success(f"APOSTA A: {' - '.join(map(str, sorted(aA)))}")
                st.success(f"APOSTA B: {' - '.join(map(str, sorted(aB)))}")
            else:
                st.error("No s'ha trobat la combinació B inèdita. Massa restriccions.")
        else:
            st.error("No s'ha trobat cap combinació A. Revisa els vetos.")

st.markdown("<br><br>", unsafe_allow_html=True)
