import streamlit as st

# --- КОНСТАНТИ ---
EUR_TO_BGN = 1.95583
VAT_RATE = 1.20 

st.set_page_config(page_title="Investment Calc Pro", layout="wide")

# --- ИНИЦИАЛИЗАЦИЯ НА СЪСТОЯНИЕТО ---
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "turnover": None, "inv_net": None, "inv_gross": None,
        "discount": 0.0, "s_f": 0, "m_f": 0, "l_f": 0
    }

def clear_form():
    st.session_state.form_data = {
        "turnover": None, "inv_net": None, "inv_gross": None,
        "discount": 0.0, "s_f": 0, "m_f": 0, "l_f": 0
    }
    st.rerun()

st.title("📊 Инвестиционен Калкулатор")

col_inputs, col_results = st.columns([1.2, 1], gap="medium")

with col_inputs:
    st.markdown("### 📝 Параметри")
    
    # Ред 1: Валута и Оборот
    c_top1, c_top2 = st.columns([1, 1.2])
    with c_top1:
        currency_mode = st.radio("Валута:", ["BGN", "EUR"], horizontal=True)
    with c_top2:
        raw_turnover = st.number_input("Прогнозен Оборот (без ДДС)", min_value=0.0, step=100.0, 
                                       value=st.session_state.form_data["turnover"], placeholder="Сума...")

    # Ред 2: Инвестиция
    st.markdown("**Инвестиция:**")
    inv_c1, inv_c2 = st.columns(2)
    with inv_c1:
        inv_net = st.number_input("Сума без ДДС", min_value=0.0, step=10.0, 
                                  value=st.session_state.form_data["inv_net"], placeholder="0.00")
    with inv_c2:
        inv_gross = st.number_input("Су_ма с ДДС", min_value=0.0, step=12.0, 
                                    value=st.session_state.form_data["inv_gross"], placeholder="0.00")

    # Ред 3: Отстъпка и Фризери (Компактно)
    c_mid1, c_mid2 = st.columns([1, 2])
    with c_mid1:
        discount_pct = st.number_input("Отстъпка (%)", min_value=0.0, max_value=100.0, step=0.1, value=st.session_state.form_data["discount"])
    with c_mid2:
        st.write("Брой фризери:")
        f1, f2, f3 = st.columns(3)
        with f1: s_freezer = st.number_input("< 1м", min_value=0, step=1, value=st.session_state.form_data["s_f"])
        with f2: m_freezer = st.number_input("= 1м", min_value=0, step=1, value=st.session_state.form_data["m_f"])
        with f3: l_freezer = st.number_input("> 1м", min_value=0, step=1, value=st.session_state.form_data["l_f"])

    if st.button("🗑️ ИЗЧИСТИ ВСИЧКО"):
        clear_form()

# --- ЛОГИКА ---
if inv_net:
    final_inv_net = inv_net
elif inv_gross:
    final_inv_net = inv_gross / VAT_RATE
else:
    final_inv_net = 0.0

turnover_val = raw_turnover if raw_turnover is not None else 0.0
if currency_mode == "BGN":
    turnover_eur = turnover_val / EUR_TO_BGN
    inv_eur_net = final_inv_net / EUR_TO_BGN
else:
    turnover_eur = turnover_val
    inv_eur_net = final_inv_net

turnover_bgn, inv_bgn_net = turnover_eur * EUR_TO_BGN, inv_eur_net * EUR_TO_BGN
total_freezers = s_freezer + m_freezer + l_freezer
min_req_turnover_eur = (s_freezer * 1023) + (m_freezer * 1534) + (l_freezer * 2556)

if total_freezers >= 3:
    allowed_max_pct = 19.0
else:
    allowed_max_pct = (s_freezer * 6.0) + (m_freezer * 8.0) + (l_freezer * 11.0)

base_expense_pct = (inv_eur_net / turnover_eur * 100) if turnover_eur > 0 else 0.0
final_result_pct = base_expense_pct + discount_pct

# --- РЕЗУЛТАТИ (Сбити) ---
with col_results:
    st.markdown("### 📈 Анализ")
    if turnover_val > 0:
        c_res1, c_res2 = st.columns(2)
        with c_res1:
            st.write("**💰 Оборот**")
            st.write(f"{turnover_eur:,.0f} € / {turnover_bgn:,.0f} лв.")
        with c_res2:
            st.write("**🏗️ Инв. (нет)**")
            st.write(f"{inv_eur_net:,.0f} € / {inv_bgn_net:,.0f} лв.")

        st.divider()

        is_ok = (final_result_pct <= allowed_max_pct) and (turnover_eur >= min_req_turnover_eur)
        color = "#28a745" if is_ok else "#dc3545"
        
        st.markdown(f"""
            <div style="background-color: {color}; padding: 15px; border-radius: 12px; text-align: center; color: white;">
                <span style="font-size: 36px; font-weight: bold; display: block;">{final_result_pct:.2f}%</span>
                <span style="font-size: 14px; opacity: 0.9;">Лимит по политика: {allowed_max_pct}%</span>
            </div>
        """, unsafe_allow_html=True)

        if not is_ok:
            st.write("")
            if turnover_eur < min_req_turnover_eur:
                st.error(f"Нужен мин. оборот: {min_req_turnover_eur:,.0f} €")
            if final_result_pct > allowed_max_pct:
                st.warning(f"Превишен лимит с {(final_result_pct - allowed_max_pct):.2f}%")
        else:
            st.success("✅ Сделката е одобрена!")

        with st.expander("Детайли за ДДС"):
            st.write(f"Инвестиция с ДДС: **{inv_eur_net*VAT_RATE:,.2f} €**")
            st.write(f"Инвестиция с ДДС: **{inv_bgn_net*VAT_RATE:,.2f} лв.**")
    else:
        st.info("💡 Въведете данни за анализ.")
