import streamlit as st

st.title("Diagnóstico")

st.write("O app carregou")

try:
    from rankine_otimizacao import ciclo_rankine
    st.success("Importação OK")
except Exception as e:
    st.error(f"Erro na importação: {e}")

if st.button("Teste"):

    try:

        st.write("Entrou no botão")

        resultado = ciclo_rankine()

        st.write("Função executou")

        st.write(type(resultado))

        st.write(resultado)

    except Exception as e:

        st.error(f"Erro na execução: {e}")
