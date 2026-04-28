import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="Prometeus Elite", page_icon="🔥", layout="centered")

# --- ESTILS VISUALS (ROBUSTOS) ---
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
st.write("FULMINANT ULTIMATE EDITION - MOTOR FLEXIBLE (1 REPETICIÓ ADMESA)")

# --- PANELLS DE CONFIGURACIÓ ---
st.markdown("### 1. Desenes")
col_d1, col_d2 = st.columns(2)
with col_d1:
    st.write("**Decena Lliure (0)**")
    sel_decena_libre = st.radio("D_LL", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], horizontal=True, label_visibility="collapsed")
with col_d2:
    st.write("**Decenes Dobles (2)**")
    d_doble_1 = st.radio("D1", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], key="d1", horizontal=True, label_visibility="collapsed")
    d_doble_2 = st.radio("D2", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"], key="d2", horizontal=True, label_visibility="collapsed")

st.markdown("### 2. Unitat Repetida")
sel_un_rep = st.radio("UR", ["Aleatori", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, label_visibility="collapsed")

st.markdown("### 3. Unitats Vetades")
v1 = st.radio("V1", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v1")
v2 = st.radio("V2", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v2")
v3 = st.radio("V3", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v3")
v4 = st.radio("V4", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v4")

st.markdown("### 4. Filtre Mellizos")
sel_m_status = st.radio("M", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.markdown("### 5. Filtre Clumps")
sel_c_status = st.radio("C", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.divider()

# --- MOTOR DE CÀLCUL AMB FLEXIBILITAT (MAX 1 REPETICIÓ) ---

def motor_flexible():
    vetos = [v for v in [v1, v2, v3, v4] if v != "Cap"]
    tramos = [(1,10), (11,20), (21,30), (31,40), (41,50)]
    tramos_n = ["1-10", "11-20", "21-30", "31-40", "41-50"]
    mells_nums = {11, 22, 33, 44}
    
    resultats = []
    
    # Bucle per generar les dues apostes
    while len(resultats) < 2:
        success_aposta = False
        intents_local = 50000
        
        while not success_aposta and intents_local > 0:
            intents_local -= 1
            
            # Patró desenes
            idx_ll = random.randint(0,4) if sel_decena_libre == "Aleatori" else tramos_n.index(sel_decena_libre)
            rest = [i for i in range(5) if i != idx_ll]
            idx_db = []
            for d in [d_doble_1, d_doble_2]:
                if d != "Aleatori":
                    val = tramos_n.index(d)
                    if val != idx_ll: idx_db.append(val)
            idx_db = list(set(idx_db))
            while len(idx_db) < 2:
                op = random.choice(rest)
                if op not in idx_db: idx_db.append(op)
            idx_si = [i for i in rest if i not in idx_db]
            
            temp_comb = []
            possible = True
            
            # Generació per desenes
            for i in idx_db:
                p = [n for n in range(tramos[i][0], tramos[i][1]+1) if n % 10 not in vetos]
                if len(p) < 2: possible = False; break
                temp_comb.extend(random.sample(p, 2))
            for i in idx_si:
                p = [n for n in range(tramos[i][0], tramos[i][1]+1) if n % 10 not in vetos]
                if len(p) < 1: possible = False; break
                temp_comb.extend(random.sample(p, 1))
            
            if not possible: continue
            
            # Filtre Paritat
            if sum(1 for n in temp_comb if n % 2 == 0) != 3: continue
            
            # Filtre Unitats
            terms = [n % 10 for n in temp_comb]
            counts = {x: terms.count(x) for x in set(terms)}
            if list(counts.values()).count(2) != 1: continue 
            if sel_un_rep != "Aleatori" and counts.get(sel_un_rep) != 2: continue
            
            # Filtre Mellizos
            pm = [n for n in temp_comb if n in mells_nums]
            if sel_m_status == "ON":
                if len(pm) != 1: continue
            else:
                if len(pm) > 0: continue
            
            # Filtre Clumps
            temp_comb.sort()
            seg = sum(1 for j in range(len(temp_comb)-1) if temp_comb[j+1] == temp_comb[j]+1)
            if sel_c_status == "ON":
                if seg != 1: continue
            else:
                if seg > 0: continue
            
            # VALIDACIÓ DE REPETICIÓ ENTRE A I B
            if len(resultats) == 1:
                set_A = set(resultats[0])
                set_B = set(temp_comb)
                comuns = set_A.intersection(set_B)
                if len(comuns) > 1: continue # Si es repeteixen més d'1, descartem
            
            resultats.append(temp_comb)
            success_aposta = True
            
    return resultats

if st.button("🚀 GENERAR 2 APOSTES PROMETEUS ELITE"):
    with st.spinner('Calculant amb marge de repetició admès...'):
        apostes = motor_flexible()
        
    st.markdown("### 🔮 Combinacions (Màxim 1 repetit entre A i B)")
    for idx, a in enumerate(apostes):
        st.success(f"APOSTA {chr(65+idx)}: {' - '.join(map(str, sorted(a)))}")

st.markdown("<br><br>", unsafe_allow_html=True)
