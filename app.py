import streamlit as st
from rankine_otimizacao import ciclo_rankine

st.title("Diagnóstico Rankine")

if st.button("Executar"):

    try:

        st.write("Antes da função")

        df, otimo = ciclo_rankine()

        st.write("Função executada")

        st.write(df.head())

        st.write(otimo)

    except Exception as e:

        st.error(str(e))
        
