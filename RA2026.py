import streamlit as st

# Константа за валутния курс
EUR_TO_BGN = 1.95583

st.set_page_config(page_title="Investment Calc Pro", layout="wide")

# --- СТИЛИЗИРАНЕ ЗА ПО-ДОБЪР UI ---
st.markdown("""
    <style>
    /* Правим полетата за въвеждане по-видими */
    .stNumberInput input {
        font-size: 1.2rem !important;
        padding: 10px !important;
    }
    /* Скриваме стрелките на числовите полета за по-чист вид */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Калкулатор: Инвестиции и Рентабилност")
st.markdown("---")

col_inputs, col_results = st.columns([1, 1], gap="large")

with col_inputs:
    st.subheader("📝 Основни параметри")
    
    currency_mode = st.radio("Въвеждай в:", ["BGN (Лева)", "EUR (Евро)"], horizontal=True)
    
    c1, c2 = st.columns(2)
    with c1:
        # Използваме value=None за празно поле и формат за избягване на застъпващи нули
        raw_turnover = st.number_input("Прогнозен Оборот", min_value=0.0, step=100.0, value=None, placeholder="Въведете сума...")
    with c2:
        raw_investment = st.number_input("Обща Инвестиция", min_value=0.0, step=10.0, value=None, placeholder="Въведете сума...")
    
    discount_pct = st.number_input("Процент допълнителна отстъпка (%)", min_value=0.0, max_value=100.0, step=0.1, value=None, placeholder="0.0")

    st.subheader("🍦 Оборудване (Брой фризери)")
    f1, f2, f3 = st.columns(3)
    with f1:
        s_freezer = st.number_input("< 1м", min_value=0, step=1, value=0) # Тук оставяме 0, защото е бройка
    with f2:
        m_freezer = st.number_input("1м", min_value=0, step=1, value=0)
    with f3:
        l_freezer = st.number_input("> 1м", min_value=0, step=1, value=0)

# --- ЛОГИКА ПРИ ПРАЗНИ ПОЛЕТА ---
# Ако потребителят още не е въвел нищо, задаваме 0 за изчисленията
turnover_val = raw_turnover if raw_turnover is not None else 0.0
investment_val = raw_investment if raw_investment is not None else 0.0
discount_val = discount_pct if discount_pct is not None else 0.0

# Преобразуване на валута
if currency_mode == "BGN (Лева)":
    turnover_eur = turnover_val / EUR_TO_BGN
    investment_eur = investment_val / EUR_TO_BGN
else:
    turnover_eur = turnover_val
    investment_eur = investment_val

turnover_bgn = turnover_eur * EUR_TO_BGN
investment_bgn = investment_eur * EUR_TO_BGN

# --- ИЗЧИСЛЕНИЯ ---
total_freezers = s_freezer + m_freezer + l_freezer
min_req_turnover_eur = (s_freezer * 1023) + (m_freezer * 1534) + (l_freezer * 2556)

if total_freezers >= 3:
    allowed_max_pct = 19.0
else:
    allowed_max_pct = (s_freezer * 6.0) + (m_freezer * 8.0) + (l_freezer * 11.0)

base_expense_pct = (investment_eur / turnover_eur * 100) if turnover_eur > 0 else 0.0
final_result_pct = base_expense_pct + discount_val

# --- РЕЗУЛТАТИ ---
with col_results:
    st.subheader("📈 Анализ")
    
    # Показваме резултати само ако има въведен оборот
    if turnover_val > 0:
        st.write(f"**Оборот:** {turnover_eur:,.2f} € | {turnover_bgn:,.2f} лв.")
        st.write(f"**Инвестиция:** {investment_eur:,.2f} € | {investment_bgn:,.2f} лв.")
        
        is_ok = (final_result_pct <= allowed_max_pct) and (turnover_eur >= min_req_turnover_eur)
        color = "#28a745" if is_ok else "#dc3545"
        
        st.markdown(f"""
            <div style="background-color: {color}; padding: 20px; border-radius: 15px; text-align: center; color: white;">
                <h1 style="margin:0;">{final_result_pct:.2f}%</h1>
                <p style="margin:0;">Общ разход (Лимит: {allowed_max_pct}%)</p>
            </div>
        """, unsafe_allow_html=True)
        
        if turnover_eur < min_req_turnover_eur:
            st.warning(f"⚠️ Нужен оборот: {min_req_turnover_eur:,.2f} €")
    else:
        st.info("💡 Моля, въведете оборот и изберете фризери, за да видите анализа.")

