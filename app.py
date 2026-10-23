import streamlit as st
import matplotlib.pyplot as plt

from rankine_otimizacao import otimizar_rankine

st.set_page_config(
    page_title="Ciclo Rankine Regenerativo",
    layout="wide"
)

st.title("Otimização do Ciclo Rankine Regenerativo")

st.write(
    "Clique no botão para calcular 100 pressões intermediárias "
    "e encontrar a pressão ótima."
)

if st.button("Executar Otimização"):

    try:

        df, otimo = otimizar_rankine()

        st.success("Cálculo concluído!")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Pressão Ótima (MPa)",
                f"{otimo['pi']:.4f}"
            )

            st.metric(
                "Rendimento (%)",
                f"{otimo['eta'] * 100:.2f}"
            )

        with col2:
            st.metric(
                "Fração Extraída",
                f"{otimo['y']:.4f}"
            )

            st.metric(
                "Vazão (kg/s)",
                f"{otimo['mdot']:.2f}"
            )

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(
            df["pi"],
            df["eta"] * 100,
            linewidth=2
        )

        ax.scatter(
            otimo["pi"],
            otimo["eta"] * 100,
            color="red",
            s=100,
            label="Ótimo"
        )

        ax.set_xscale("log")

        ax.set_xlabel(
            "Pressão Intermediária (MPa)"
        )

        ax.set_ylabel(
            "Rendimento (%)"
        )

        ax.set_title(
            "Rendimento × Pressão Intermediária"
        )

        ax.grid(True)

        ax.legend()

        st.pyplot(fig)

        st.subheader("Tabela Completa")

        st.dataframe(df)

    except Exception as erro:

        st.error(
            f"Erro: {erro}"
        )
