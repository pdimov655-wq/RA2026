import streamlit as st

# ... (запазваме началната част на кода и логиката за изчисления) ...

# --- РЕЗУЛТАТИ (Дясна колона) ---
with col_results:
    st.subheader("📈 Анализ на рентабилността")
    
    if turnover_val > 0:
        # 1. Секция ОБОРОТ
        st.markdown("### 💰 Оборот по договор")
        st.write(f"**Евро:** {turnover_eur:,.2f} €")
        st.write(f"**Лева:** {turnover_bgn:,.2f} лв.")
        
        st.markdown("---")
        
        # 2. Секция ИНВЕСТИЦИЯ
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
        
        # 3. ВИЗУАЛЕН СТАТУС (Процент разход)
        is_ok = (final_result_pct <= allowed_max_pct) and (turnover_eur >= min_req_turnover_eur)
        color = "#28a745" if is_ok else "#dc3545"
        
        st.markdown(f"""
            <div style="background-color: {color}; padding: 25px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h1 style="margin:0; font-size: 50px;">{final_result_pct:.2f}%</h1>
                <p style="margin:0; font-size: 18px; font-weight: bold;">ОБЩ РАЗХОД ПО ПОЛИТИКА</p>
                <p style="margin:5px 0 0 0; opacity: 0.9;">Лимит: {allowed_max_pct}%</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 4. ПРЕДУПРЕЖДЕНИЯ
        st.write("")
        if turnover_eur < min_req_turnover_eur:
            st.error(f"❌ **Недостатъчен оборот!** Минимумът е {min_req_turnover_eur:,.2f} € ({min_req_turnover_eur*EUR_TO_BGN:,.2f} лв.)")
        
        if final_result_pct > allowed_max_pct:
            st.warning(f"⚠️ **Превишен лимит!** Инвестицията е твърде висока за този тип клиент.")
            
        if is_ok:
            st.success("✅ **Сделката е одобрена!** Всички параметри са в норма.")
            
    else:
        st.info("💡 Моля, въведете прогнозен оборот в секция 'Основни параметри', за да стартирате анализа.")
