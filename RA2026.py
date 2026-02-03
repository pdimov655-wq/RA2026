import streamlit as st

# --- КОНСТАНТИ ---
EUR_TO_BGN = 1.95583
VAT_RATE = 1.20 

st.set_page_config(page_title="Investment Calc Pro", layout="wide")

# --- ИНИЦИАЛИЗАЦИЯ НА СЪСТОЯНИЕТО ---
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "turnover": None,
        "inv_net": None,
        "inv_gross": None,
        "discount": 0.0,
        "s_f": 0,
        "m_f": 0,
        "l_f": 0
    }

def clear_form():
    st.session_state.form_data = {
        "turnover": None, "inv_net": None, "inv_gross": None,
        "discount": 0.0, "s_f": 0, "m_f": 0, "l_f": 0
    }
    st.rerun()

st.title("📊 Калкулатор: Инвестиции и Рентабилност")
st.markdown("---")

col_inputs, col_results = st.columns([1, 1], gap="large")

with col_inputs:
    st.subheader("📝 Основни параметри")
    
    currency_mode = st.radio("Въвеждай в:", ["BGN (Лева)", "EUR (Евро)"], horizontal=True)
    
    # Оборот
    raw_turnover = st.number_input("Прогнозен Оборот (без ДДС)", min_value=0.0, step=100.0, 
                                   value=st.session_state.form_data["turnover"], placeholder="Въведете сума...")

    st.markdown("**Обща Инвестиция:**")
    inv_c1, inv_c2 = st.columns(2)
    with inv_c1:
        inv_net = st.number_input("Сума без ДДС", min_value=0.0, step=10.0, 
                                  value=st.session_state.form_data["inv_net"], placeholder="0.00")
    with inv_c2:
        inv_gross = st.number_input("Сума с ДДС", min_value=0.0, step=12.0, 
                                    value=st.session_state.form_data["inv_gross"], placeholder="0.00")

    # Логика за инвестицията (Priority: Net -> Gross)
    if inv_net:
        final_inv_net = inv_net
    elif inv_gross:
        final_inv_net = inv_gross / VAT_RATE
    else:
        final_inv_net = 0.0

    discount_pct = st.number_input("Процент допълнителна отстъпка (%)", min_value=0.0, max_value=100.0, 
                                   step=0.1, value=st.session_state.form_data["discount"])

    st.subheader("🍦 Оборудване (Брой)")
    f1, f2, f3 = st.columns(3)
    with f1: s_freezer = st.number_input("Под 1м (< 1м)", min_value=0, step=1, value=st.session_state.form_data["s_f"])
    with f2: m_freezer = st.number_input("Точно 1м (= 1м)", min_value=0, step=1, value=st.session_state.form_data["m_f"])
    with f3: l_freezer = st.number_input("Над 1м (> 1м)", min_value=0, step=1, value=st.session_state.form_data["l_f"])

    if st.button("🗑️ ИЗЧИСТИ ВСИЧКО"):
        clear_form()

# --- ИЗЧИСЛЕНИЯ ---
turnover_val = raw_turnover if raw_turnover is not None else 0.0

if currency_mode == "BGN (Лева)":
    turnover_eur = turnover_val / EUR_TO_BGN
    inv_eur_net = final_inv_net / EUR_TO_BGN
else:
    turnover_eur = turnover_val
    inv_eur_net = final_inv_net

turnover_bgn = turnover_eur * EUR_TO_BGN
inv_bgn_net = inv_eur_net * EUR_TO_BGN

total_freezers = s_freezer + m_freezer + l_freezer
min_req_turnover_eur = (s_freezer * 1023) + (m_freezer * 1534) + (l_freezer * 2556)

if total_freezers >= 3:
    allowed_max_pct = 19.0
else:
    allowed_max_pct = (s_freezer * 6.0) + (m_freezer * 8.0) + (l_freezer * 11.0)

base_expense_pct = (inv_eur_net / turnover_eur * 100) if turnover_eur > 0 else 0.0
final_result_pct = base_expense_pct + discount_pct

# --- РЕЗУЛТАТИ ---
with col_results:
    st.subheader("📈 Анализ на рентабилността")
    
    if turnover_val > 0:
        st.markdown("### 💰 Оборот по договор")
        st.write(f"**Евро:** {turnover_eur:,.2f} €")
        st.write(f"**Лева:** {turnover_bgn:,.2f} лв.")
        st.markdown("---")
        
        st.markdown("### 🏗️ Инвестиция")
        inv_col_a, inv_col_b = st.columns(2)
        with inv_col_a:
            st.write("**Без ДДС:**")
            st.write(f"{inv_eur_net:,.2f} €")
            st.write(f"{inv_bgn_net:,.2f} лв.")
        with inv_col_b:
            st.write("**С ДДС (20%):**")
            st.write(f"{inv_eur_net*VAT_RATE:,.2f} €")
            st.write(f"{inv_bgn_net*VAT_RATE:,.2f} лв.")
        st.markdown("---")
        
        is_ok = (final_result_pct <= allowed_max_pct) and (turnover_eur >= min_req_turnover_eur)
        color = "#28a745" if is_ok else "#dc3545"
        
        st.markdown(f"""
            <div style="background-color: {color}; padding: 25px; border-radius: 15px; text-align: center; color: white;">
                <h1 style="margin:0; font-size: 50px;">{final_result_pct:.2f}%</h1>
                <p style="margin:0; font-size: 18px; font-weight: bold;">ОБЩ РАЗХОД ПО ПОЛИТИКА</p>
                <p style="margin:5px 0 0 0; opacity: 0.9;">Лимит за избора: {allowed_max_pct}%</p>
            </div>
        """, unsafe_allow_html=True)
        
        if turnover_eur < min_req_turnover_eur:
            st.error(f"❌ **Недостатъчен оборот!** Минимум: {min_req_turnover_eur:,.2f} € ({min_req_turnover_eur*EUR_TO_BGN:,.2f} лв.)")
        if final_result_pct > allowed_max_pct:
            st.warning(f"⚠️ **Превишен лимит!** Процентът разход е твърде висок.")
        if is_ok:
            st.success("✅ **Сделката отговаря на изискванията.**")
    else:
        st.info("💡 Въведете данни вляво, за да видите резултатите.")
