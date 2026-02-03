import streamlit as st

# Константа за валутния курс
EUR_TO_BGN = 1.95583

st.set_page_config(page_title="Investment Calc Pro", layout="wide")

st.title("📊 Калкулатор: Инвестиции и Рентабилност")
st.markdown("---")

# --- СЕКЦИЯ 1: ВЪВЕЖДАНЕ НА ДАННИ ---
col_inputs, col_results = st.columns([1, 1], gap="large")

with col_inputs:
    st.subheader("📝 Основни параметри")
    
    # Избор на валута за въвеждане
    currency_mode = st.radio("Въвеждай в:", ["BGN (Лева)", "EUR (Евро)"], horizontal=True)
    
    c1, c2 = st.columns(2)
    with c1:
        raw_turnover = st.number_input("Прогнозен Оборот", min_value=0.0, format="%.2f")
    with c2:
        raw_investment = st.number_input("Обща Инвестиция", min_value=0.0, format="%.2f")
    
    # Преобразуване според избраната валута
    if currency_mode == "BGN (Лева)":
        turnover_eur = raw_turnover / EUR_TO_BGN
        investment_eur = raw_investment / EUR_TO_BGN
        turnover_bgn = raw_turnover
        investment_bgn = raw_investment
    else:
        turnover_eur = raw_turnover
        investment_eur = raw_investment
        turnover_bgn = raw_turnover * EUR_TO_BGN
        investment_bgn = raw_investment * EUR_TO_BGN

    discount_pct = st.number_input("Процент допълнителна отстъпка (%)", min_value=0.0, max_value=100.0, step=0.1)

    st.subheader("🍦 Оборудване (Брой фризери)")
    f1, f2, f3 = st.columns(3)
    with f1:
        s_freezer = st.number_input("< 1м", min_value=0, step=1, value=0)
    with f2:
        m_freezer = st.number_input("1м", min_value=0, step=1, value=0)
    with f3:
        l_freezer = st.number_input("> 1м", min_value=0, step=1, value=0)

# --- ИЗЧИСЛЕНИЯ ПО ТЪРГОВСКА ПОЛИТИКА ---
total_freezers = s_freezer + m_freezer + l_freezer

# Минимален оборот (в евро по условие)
min_req_turnover_eur = (s_freezer * 1023) + (m_freezer * 1534) + (l_freezer * 2556)
min_req_turnover_bgn = min_req_turnover_eur * EUR_TO_BGN

# Максимален процент инвестиция
if total_freezers >= 3:
    allowed_max_pct = 19.0
else:
    allowed_max_pct = (s_freezer * 6.0) + (m_freezer * 8.0) + (l_freezer * 11.0)

# Краен резултат (Инвестиция/Оборот + Отстъпка)
base_expense_pct = (investment_eur / turnover_eur * 100) if turnover_eur > 0 else 0.0
final_result_pct = base_expense_pct + discount_pct

# --- СЕКЦИЯ 2: РЕЗУЛТАТИ ---
with col_results:
    st.subheader("📈 Анализ на рентабилността")
    
    # Показване на валутите
    st.write(f"**Оборот:** {turnover_eur:,.2f} € | {turnover_bgn:,.2f} лв.")
    st.write(f"**Инвестиция:** {investment_eur:,.2f} € | {investment_bgn:,.2f} лв.")
    st.markdown("---")

    # Основен статус
    is_ok = (final_result_pct <= allowed_max_pct) and (turnover_eur >= min_req_turnover_eur) and (total_freezers > 0)
    
    color = "#28a745" if is_ok else "#dc3545" # Зелено или Червено
    
    st.markdown(f"""
        <div style="background-color: {color}; padding: 25px; border-radius: 15px; text-align: center; color: white;">
            <h1 style="margin:0; font-size: 40px;">{final_result_pct:.2f}%</h1>
            <p style="margin:0; font-size: 18px;">Общ разход (Макс: {allowed_max_pct}%)</p>
        </div>
    """, unsafe_allow_html=True)

    # Проверки
    st.write("")
    if total_freezers == 0:
        st.info("ℹ️ Моля, добавете поне един фризер за калкулация.")
    else:
        if turnover_eur < min_req_turnover_eur:
            st.error(f"❌ Недостатъчен оборот! Минимум: {min_req_turnover_eur:,.2f} € ({min_req_turnover_bgn:,.2f} лв.)")
        else:
            st.success(f"✅ Оборотът е над изискуемия минимум ({min_req_turnover_eur:,.2f} €)")

        if final_result_pct > allowed_max_pct:
            st.error(f"❌ Разходът превишава лимита от {allowed_max_pct}%")
        elif is_ok:
            st.balloons()
            st.success("✅ Сделката отговаря на търговската политика!")

st.markdown("---")
st.caption("© 2026 Търговски калкулатор | Валутен курс: 1 EUR = 1.95583 BGN")
