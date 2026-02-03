import streamlit as st

# Константи
EUR_TO_BGN = 1.95583
VAT_RATE = 1.20 # 20% ДДС

st.set_page_config(page_title="Investment Calc Pro", layout="wide")

st.title("📊 Калкулатор: Инвестиции и Рентабилност")
st.markdown("---")

col_inputs, col_results = st.columns([1, 1], gap="large")

with col_inputs:
    st.subheader("📝 Основни параметри")
    
    currency_mode = st.radio("Въвеждай в:", ["BGN (Лева)", "EUR (Евро)"], horizontal=True)
    
    # --- ОБОРОТ ---
    raw_turnover = st.number_input("Прогнозен Оборот (без ДДС)", min_value=0.0, step=100.0, value=None, placeholder="Въведете сума...")

    # --- ИНВЕСТИЦИЯ С ДДС ЛОГИКА ---
    st.markdown("**Обща Инвестиция:**")
    inv_c1, inv_c2 = st.columns(2)
    
    with inv_c1:
        # Използваме session_state, за да можем да ги обвържем по-късно, 
        # но за простота тук ще ги оставим като независими входове с опция за избор
        inv_net = st.number_input("Сума без ДДС", min_value=0.0, step=10.0, value=None, placeholder="0.00")
    with inv_c2:
        inv_gross = st.number_input("Сума с ДДС", min_value=0.0, step=12.0, value=None, placeholder="0.00")

    # Автоматично приоритизиране: ако е въведено "без ДДС", ползваме него. 
    # Ако е въведено само "с ДДС", го пресмятаме обратно.
    if inv_net:
        final_inv_net = inv_net
    elif inv_gross:
        final_inv_net = inv_gross / VAT_RATE
    else:
        final_inv_net = 0.0

    discount_pct = st.number_input("Процент допълнителна отстъпка (%)", min_value=0.0, max_value=100.0, step=0.1, value=None, placeholder="0.0")

    st.subheader("🍦 Оборудване (Брой фризери)")
    f1, f2, f3 = st.columns(3)
    with f1: s_freezer = st.number_input("< 1м", min_value=0, step=1, value=0)
    with f2: m_freezer = st.number_input("1м", min_value=0, step=1, value=0)
    with f3: l_freezer = st.number_input("> 1м", min_value=0, step=1, value=0)

# --- ПРЕОБРАЗУВАНЕ НА ВАЛУТА ---
turnover_val = raw_turnover if raw_turnover is not None else 0.0
discount_val = discount_pct if discount_pct is not None else 0.0

if currency_mode == "BGN (Лева)":
    turnover_eur = turnover_val / EUR_TO_BGN
    inv_eur_net = final_inv_net / EUR_TO_BGN
else:
    turnover_eur = turnover_val
    inv_eur_net = final_inv_net

turnover_bgn = turnover_eur * EUR_TO_BGN
inv_bgn_net = inv_eur_net * EUR_TO_BGN

# --- ИЗЧИСЛЕНИЯ ПО ПОЛИТИКА ---
total_freezers = s_freezer + m_freezer + l_freezer
min_req_turnover_eur = (s_freezer * 1023) + (m_freezer * 1534) + (l_freezer * 2556)

if total_freezers >= 3:
    allowed_max_pct = 19.0
else:
    allowed_max_pct = (s_freezer * 6.0) + (m_freezer * 8.0) + (l_freezer * 11.0)

base_expense_pct = (inv_eur_net / turnover_eur * 100) if turnover_eur > 0 else 0.0
final_result_pct = base_expense_pct + discount_val

# --- РЕЗУЛТАТИ ---
with col_results:
    st.subheader("📈 Анализ")
    
    if turnover_val > 0:
        # Показване на ДДС разбивка в резултатите
        st.write(f"**Инвестиция (без ДДС):** {inv_eur_net:,.2f} € | {inv_bgn_net:,.2f} лв.")
        st.write(f"**Инвестиция (с ДДС):** {inv_eur_net*VAT_RATE:,.2f} € | {inv_bgn_net*VAT_RATE:,.2f} лв.")
        st.markdown("---")
        
        is_ok = (final_result_pct <= allowed_max_pct) and (turnover_eur >= min_req_turnover_eur)
        color = "#28a745" if is_ok else "#dc3545"
        
        st.markdown(f"""
            <div style="background-color: {color}; padding: 25px; border-radius: 15px; text-align: center; color: white;">
                <h1 style="margin:0; font-size: 45px;">{final_result_pct:.2f}%</h1>
                <p style="margin:0; font-size: 18px;">Общ разход спрямо политиката</p>
                <small>Лимит за избраните фризери: {allowed_max_pct}%</small>
            </div>
        """, unsafe_allow_html=True)
        
        if turnover_eur < min_req_turnover_eur:
            st.error(f"❌ Необходим мин. оборот: {min_req_turnover_eur:,.2f} €")
    else:
        st.info("💡 Въведете данни вляво, за да генерирате анализ.")

