import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="Prometeus Elite", page_icon="🔥", layout="centered")

# --- ESTILS VISUALS (FIDELS AL TEU PROJECTE) ---
st.markdown("""
    <style>
    .stButton>button { height: 75px; font-size: 24px; font-weight: bold; border-radius: 15px; background-color: #FF4B4B; color: white; margin-top: 25px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2); width: 100%; }
    h3 { margin-top: 25px; color: #1E1E1E; border-bottom: 2px solid #FF4B4B; width: 100%; padding-bottom: 8px; font-family: 'Helvetica', sans-serif; }
    .desc-text { font-size: 14px; color: #555; margin-bottom: 15px; font-style: italic; line-height: 1.4; }
    div.row-widget.stRadio > div{ flex-direction:row; justify-content: center; gap: 8px; flex-wrap: wrap; }
    .stSuccess { font-size: 22px !important; font-weight: bold; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    .veto-sub { font-size: 12px; color: #888; text-align: center; margin-top: -10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Encapçalament amb la teva imatge
st.image("prometeus.png", width=250) # Recorda tenir el fitxer prometeus.png al GitHub
st.title("🔥 PROMETEUS ELITE")
st.write("SISTEMA ANDROID EXCLUSIU PER A EUROMILLONES.")

# --- PANELLS DE CONFIGURACIÓ (ESTÈTICA ORIGINAL) ---

st.markdown("### 1. Selector Desenis")
st.markdown("<p class='desc-text'>Tria quina desena queda lliure (0 números) i quines dues tindran càrrega doble (2 números). Si no tries, serà aleatori.</p>", unsafe_allow_html=True)
col_d1, col_d2 = st.columns(2)
with col_d1:
    sel_decena_libre = st.selectbox("Decena LLIURE (0)", ["Cap", "1-10", "11-20", "21-30", "31-40", "41-50"])
with col_d2:
    sel_decenas_dobles = st.multiselect("Dues Desenis DOBLES (2)", ["1-10", "11-20", "21-30", "31-40", "41-50"], max_selections=2)

st.markdown("### 2. Selector Unidad Repetida")
st.markdown("<p class='desc-text'>Selecciona quina terminació (0-9) vols que es repeteixi exactament dues vegades en la combinació.</p>", unsafe_allow_html=True)
sel_un_rep = st.radio("UR", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, label_visibility="collapsed")

st.markdown("### 3. Selector Unidad Vetada")
st.markdown("<p class='desc-text'>Veta fins a 4 terminacions. Aquests números no apareixeran mai. El veto mana sobre la repetició.</p>", unsafe_allow_html=True)
v1 = st.radio("V1", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v1", label_visibility="collapsed")
v2 = st.radio("V2", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v2", label_visibility="collapsed")
v3 = st.radio("V3", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v3", label_visibility="collapsed")
v4 = st.radio("V4", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v4", label_visibility="collapsed")

st.markdown("### 4. Selector Mellizos")
st.markdown("<p class='desc-text'>Activa per incloure exactament un número besson (11, 22, 33, 44) per aposta.</p>", unsafe_allow_html=True)
sel_m_status = st.radio("M", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.markdown("### 5. Selector Clumps")
st.markdown("<p class='desc-text'>Activa per forçar l'aparició d'una única parella de números seguits per aposta.</p>", unsafe_allow_html=True)
sel_c_status = st.radio("C", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.divider()

# --- MOTOR LÒGIC PROMETEUS ELITE ---

def generar_aposta(vetos, prohibits, d_lliure, d_dobles, u_repe, mells_on, clumps_on):
    tramos = [(1,10), (11,20), (21,30), (31,40), (41,50)]
    tramos_n = ["1-10", "11-20", "21-30", "31-40", "41-50"]
    
    intentos = 0
    while intentos < 10000:
        intentos += 1
        # Definir configuració de desenes
        idx_lliure = random.randint(0,4) if d_lliure == "Cap" else tramos_n.index(d_lliure)
        restants = [i for i in range(5) if i != idx_lliure]
        
        if len(d_dobles) == 2:
            idx_dobles = [tramos_n.index(d) for d in d_dobles]
            idx_simples = [i for i in restants if i not in idx_dobles]
        else:
            idx_dobles = random.sample(restants, 2)
            idx_simples = [i for i in restants if i not in idx_dobles]
            
        comb = []
        for idx in idx_dobles:
            p = [n for n in range(tramos[idx][0], tramos[idx][1]+1) if n % 10 not in vetos and n not in prohibits]
            if len(p) < 2: break
            comb.extend(random.sample(p, 2))
        for idx in idx_simples:
            p = [n for n in range(tramos[idx][0], tramos[idx][1]+1) if n % 10 not in vetos and n not in prohibits]
            if len(p) < 1: break
            comb.extend(random.sample(p, 1))
            
        if len(comb) != 6: continue
        
        # Filtre Paritat (3P/3I)
        if sum(1 for n in comb if n % 2 == 0) != 3: continue
        
        # Filtre Unitats
        terms = [n % 10 for n in comb]
        counts = {x: terms.count(x) for x in set(terms)}
        if list(counts.values()).count(2) != 1: continue 
        if u_repe != "Cap" and counts.get(u_repe) != 2: continue
        
        # Filtre Mellizos
        mells = {11, 22, 33, 44}
        p_mells = [n for n in comb if n in mells]
        if mells_on == "ON":
            if len(p_mells) != 1: continue
        else:
            if len(p_mells) > 0: continue
            
        # Filtre Clumps
        comb.sort()
        seg = sum(1 for i in range(len(comb)-1) if comb[i+1] == comb[i]+1)
        if clumps_on == "ON":
            if seg != 1: continue
        else:
            if seg > 0: continue
            
        return comb
    return None

# --- ACCIÓ I RESULTATS ---
if st.button("🚀 GENERAR 2 APOSTES PROMETEUS ELITE"):
    vetos = [v for v in [v1, v2, v3, v4] if v != "Cap"]
    with st.spinner('Aplicant cribratge d\'alta precisió...'):
        aA = generar_aposta(vetos, [], sel_decena_libre, sel_decenas_dobles, sel_un_rep, sel_m_status, sel_c_status)
        if aA:
            aB = generar_aposta(vetos, aA, sel_decena_libre, sel_decenas_dobles, sel_un_rep, sel_m_status, sel_c_status)
            
            if aB:
                st.markdown("### 🔮 Resultats Inèdits (12 números)")
                st.success(f"APOSTA A: {' - '.join(map(str, sorted(aA)))}")
                st.success(f"APOSTA B: {' - '.join(map(str, sorted(aB)))}")
            else:
                st.error("⚠️ No s'ha pogut generar la segona aposta inèdita. Massa restriccions.")
        else:
            st.error("⚠️ Filtres massa estrictes. Revisa els vetos o les desenis.")

st.markdown("<br><br>", unsafe_allow_html=True)
