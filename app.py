import streamlit as st
import matplotlib.pyplot as plt

from rankine_otimizacao import ciclo_rankine

st.title("Otimização do Ciclo Rankine Regenerativo")

if st.button("Executar Otimização"):

    try:

        df, otimo = ciclo_rankine()

        st.success("Cálculo executado com sucesso!")

        st.write("Pressão ótima (MPa):", otimo["pi_MPa"])
        st.write("Rendimento (%):", otimo["eta"] * 100)

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(
            df["pi_MPa"],
            df["eta"] * 100
        )

        ax.set_xscale("log")

        ax.set_xlabel(
            "Pressão Intermediária (MPa)"
        )

        ax.set_ylabel(
            "Rendimento (%)"
        )

        ax.grid(True)

        st.pyplot(fig)

        st.dataframe(df)

    except Exception as e:

        st.error(f"Erro: {e}")
