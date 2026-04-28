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
st.write("FULMINANT ULTIMATE EDITION - EUROMILLONES.")

# --- PANELLS DE CONFIGURACIÓ AMB DESCRIPCIONS ---

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
st.markdown("<p class='desc-text'>Força terminacions dobles. Pots triar quina unitat (0-9) apareixerà exactament dues vegades en cada combinació. Si tries Aleatori, el sistema decidirà una per tu.</p>", unsafe_allow_html=True)
sel_un_rep = st.radio("UR", ["Aleatori", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, label_visibility="collapsed")

st.markdown("### 3. Unitats Vetades")
st.markdown("<p class='desc-text'>Criba de terminacions prohibides. Elimina totalment de les teves apostes fins a 4 terminacions. Recorda que si vetes una unitat, aquesta mai podrà ser la repetida.</p>", unsafe_allow_html=True)
v1 = st.radio("V1", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v1")
v2 = st.radio("V2", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v2")
v3 = st.radio("V3", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v3")
v4 = st.radio("V4", ["Cap", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9], horizontal=True, key="v4")

st.markdown("### 4. Filtre Mellizos")
st.markdown("<p class='desc-text'>Activa la presència de números bessons (11, 22, 33, 44). En mode ON, cada aposta contindrà exactament un número d'aquest grup, sempre que no estigui vetat.</p>", unsafe_allow_html=True)
sel_m_status = st.radio("M", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.markdown("### 5. Filtre Clumps")
st.markdown("<p class='desc-text'>Força l'aparició d'una única parella de números seguits (consecutius) per combinació. Ideal per buscar patrons de repetició en el sorteig.</p>", unsafe_allow_html=True)
sel_c_status = st.radio("C", ["OFF", "ON"], horizontal=True, label_visibility="collapsed")

st.divider()

# --- MOTOR LÒGIC D'ALTA POTÈNCIA (1M INTENTS) ---

def generar_aposta(vetos, prohibits, d_lliure, d_doble1, d_doble2, u_repe, mells_on, clumps_on):
    tramos = [(1,10), (11,20), (21,30), (31,40), (41,50)]
    tramos_n = ["1-10", "11-20", "21-30", "31-40", "41-50"]
    
    # 1.000.000 d'intents per a màxim "múscul"
    for _ in range(1000000): 
        idx_lliure = random.randint(0,4) if d_lliure == "Aleatori" else tramos_n.index(d_lliure)
        restants = [i for i in range(5) if i != idx_lliure]
        
        idx_dobles = []
        if d_doble1 != "Aleatori": idx_dobles.append(tramos_n.index(d_doble1))
        if d_doble2 != "Aleatori": idx_dobles.append(tramos_n.index(d_doble2))
        
        idx_dobles = list(set(idx_dobles))
        while len(idx_dobles) < 2:
            nou_idx = random.choice(restants)
            if nou_idx not in idx_dobles: idx_dobles.append(nou_idx)
        
        idx_simples = [i for i in restants if i not in idx_dobles]
            
        comb = []
        possible = True
        for idx in idx_dobles:
            pool = [n for n in range(tramos[idx][0], tramos[idx][1]+1) if n % 10 not in vetos and n not in prohibits]
            if len(pool) < 2: possible = False; break
            comb.extend(random.sample(pool, 2))
        if not possible: continue
        
        for idx in idx_simples:
            pool = [n for n in range(tramos[idx][0], tramos[idx][1]+1) if n % 10 not in vetos and n not in prohibits]
            if len(pool) < 1: possible = False; break
            comb.extend(random.sample(pool, 1))
            
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

# --- ACCIÓ I RESULTATS ---
if st.button("🚀 GENERAR 2 APOSTES PROMETEUS ELITE"):
    vetos_final = list(set([v for v in [v1, v2, v3, v4] if v != "Cap"]))
    with st.spinner('Cribrant 1.000.000 de combinacions...'):
        aA = generar_aposta(vetos_final, [], sel_decena_libre, d_doble_1, d_doble_2, sel_un_rep, sel_m_status, sel_c_status)
        if aA:
            # Garantim 12 números inèdits passant aA com a prohibits
            aB = generar_aposta(vetos_final, aA, sel_decena_libre, d_doble_1, d_doble_2, sel_un_rep, sel_m_status, sel_c_status)
            if aB:
                st.markdown("### 🔮 Combinacions Resultants (12 inèdits)")
                st.success(f"APOSTA A (3P/3I): {' - '.join(map(str, sorted(aA)))}")
                st.success(f"APOSTA B (3P/3I): {' - '.join(map(str, sorted(aB)))}")
            else:
                st.error("No s'ha trobat la combinació B inèdita. Redueix els vetos o canvia les desenes.")
        else:
            st.error("No s'ha trobat cap combinació que compleixi tots els filtres.")

st.markdown("<br><br>", unsafe_allow_html=True)
