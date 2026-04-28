import streamlit as st
import random

# --- CONFIGURACIÓ DE PÀGINA ---
st.set_page_config(page_title="Prometeus Elite", page_icon="🔥", layout="centered")

# --- ESTILS VISUALS (MINIMALISTA I FUNCIONAL) ---
st.markdown("""
    <style>
    .stButton>button { height: 75px; font-size: 24px; font-weight: bold; border-radius: 15px; background-color: #FF4B4B; color: white; margin-top: 25px; box-shadow: 0px 4px 10px rgba(0,0,0,0.2); width: 100%; }
    h3 { margin-top: 25px; color: #1E1E1E; border-bottom: 2px solid #FF4B4B; width: 100%; padding-bottom: 8px; font-family: 'Helvetica', sans-serif; }
    .desc-text { font-size: 14px; color: #555; margin-bottom: 15px; font-style: italic; line-height: 1.4; }
    div.row-widget.stRadio > div{ flex-direction:row; justify-content: center; gap: 8px; flex-wrap: wrap; }
    .stSuccess { font-size: 22px !important; font-weight: bold; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

# Títol amb la icona del foc
st.title("🔥 PROMETEUS ELITE")
st.write("SISTEMA ANDROID EXCLUSIU PER A EUROMILLONES.")

# --- PANELLS DE CONFIGURACIÓ ---

st.markdown("### 1. Selector Desenis")
st.markdown("<p class='desc-text'>Tria quina desena queda lliure (0 números) i quines dues tindran càrrega doble (2 números).</p>", unsafe_allow_html=True)
col_d1, col_d2 = st.columns(2)
with col_d1:
    sel_decena_libre = st.selectbox("Decena LLIURE (0)", ["Aleatori", "1-10", "11-20", "21-30", "31-40", "41-50"])
with col_d2:
    sel_decenas_dobles = st.multiselect("Dues Desenis DOBLES (2)", ["1-10", "11-20", "21-30", "31-40", "41-50"], max_selections=2)

st.markdown("### 2. Selector Unidad Repetida")
st.markdown("<p class='desc-text'>Quina terminació vols que es repeteixi exactament dues vegades.</p>", unsafe_allow_html=True)
sel_un_rep = st.radio("UR", ["Aleatori", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, label_visibility="collapsed")

st.markdown("### 3. Selector Unidad Vetada")
st.markdown("<p class='desc-text'>Veta fins a 4 terminacions (màxim). El veto mana sobre la repetició.</p>", unsafe_allow_html=True)
v_multi = st.multiselect("Unitats Vetades", list(range(10)), max_selections=4, label_visibility="collapsed")

st.markdown("### 4. Selector Mellizos")
st.markdown("<p class='desc-text'>Activa per incloure exactament un número besson (11, 22, 33, 44) per aposta.</p>", unsafe_allow_html=True)
sel_m_status = st.radio("M", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.markdown("### 5. Selector Clumps")
st.markdown("<p class='desc-text'>Activa per forçar una parella de números seguits per aposta.</p>", unsafe_allow_html=True)
sel_c_status = st.radio("C", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.divider()

# --- MOTOR LÒGIC (EUROMILLONES 1-50) ---

def generar_aposta(vetos, prohibits, d_lliure, d_dobles, u_repe, mells_on, clumps_on):
    tramos = [(1,10), (11,20), (21,30), (31,40), (41,50)]
    tramos_n = ["1-10", "11-20", "21-30", "31-40", "41-50"]
    
    for _ in range(15000): # Intents de criba
        # 1. Configurar Desenis 2-2-1-1-0
        idx_lliure = random.randint(0,4) if d_lliure == "Aleatori" else tramos_n.index(d_lliure)
        restants = [i for i in range(5) if i != idx_lliure]
        
        if len(d_dobles) == 2:
            idx_dobles = [tramos_n.index(d) for d in d_dobles]
            idx_simples = [i for i in restants if i not in idx_dobles]
        else:
            idx_dobles = random.sample(restants, 2)
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
        
        # 2. Filtre Paritat (3P/3I)
        if sum(1 for n in comb if n % 2 == 0) != 3: continue
        
        # 3. Filtre Unitats (Terminacions)
        terms = [n % 10 for n in comb]
        counts = {x: terms.count(x) for x in set(terms)}
        if list(counts.values()).count(2) != 1: continue 
        if u_repe != "Aleatori" and counts.get(u_repe) != 2: continue
        
        # 4. Filtre Mellizos
        mells = {11, 22, 33, 44}
        p_mells = [n for n in comb if n in mells]
        if mells_on == "ON":
            if len(p_mells) != 1: continue
            if any(n % 10 in vetos for n in p_mells): continue # No pot ser de unitat vetada
        else:
            if len(p_mells) > 0: continue
            
        # 5. Filtre Clumps (Seguits)
        comb.sort()
        seg = sum(1 for i in range(len(comb)-1) if comb[i+1] == comb[i]+1)
        if clumps_on == "ON":
            if seg != 1: continue
        else:
            if seg > 0: continue
            
        return comb
    return None

# --- BOTO I RESULTATS ---
if st.button("🚀 GENERAR APOSTES PROMETEUS ELITE"):
    with st.spinner('Cribrant combinacions...'):
        aA = generar_aposta(v_multi, [], sel_decena_libre, sel_decenas_dobles, sel_un_rep, sel_m_status, sel_c_status)
        if aA:
            # Segona aposta amb prohibits d'A per garantir 12 números inédits
            aB = generar_aposta(v_multi, aA, sel_decena_libre, sel_decenas_dobles, sel_un_rep, sel_m_status, sel_c_status)
            
            if aB:
                st.markdown("### 🔮 Combinacions Resultants")
                st.success(f"APOSTA A: {' - '.join(map(str, sorted(aA)))}")
                st.success(f"APOSTA B: {' - '.join(map(str, sorted(aB)))}")
            else:
                st.error("No s'ha trobat una segona combinació que respecti els 12 números inèdits. Prova amb menys vetos.")
        else:
            st.error("Filtres massa estrictes. Revisa la configuració.")

st.markdown("<br><br>", unsafe_allow_html=True)
