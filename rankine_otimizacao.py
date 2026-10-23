import streamlit as st
import matplotlib.pyplot as plt

from rankine_otimizacao import ciclo_rankine

st.title("Otimização do Ciclo Rankine Regenerativo")

# Entradas
pH = st.sidebar.number_input(
    "Pressão máxima (MPa)",
    value=10.0
)

TH = st.sidebar.number_input(
    "Temperatura máxima (°C)",
    value=500.0
)

pL = st.sidebar.number_input(
    "Pressão mínima (MPa)",
    value=0.01
)

eta_t = st.sidebar.number_input(
    "Eficiência da turbina",
    value=0.80,
    step=0.01
)

n = st.sidebar.slider(
    "Número de pontos",
    min_value=20,
    max_value=500,
    value=100
)

if st.button("Executar Otimização"):

    try:

        # CHAMADA CORRIGIDA
        df, otimo = ciclo_rankine(
            pH,
            TH,
            pL,
            eta_t,
            100000,
            n
        )

        st.success("Cálculo concluído")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Pressão ótima (MPa)",
                f"{otimo['pi_MPa']:.4f}"
            )

            st.metric(
                "Rendimento (%)",
                f"{otimo['eta']*100:.2f}"
            )

        with col2:
            st.metric(
                "Fração extraída",
                f"{otimo['y']:.4f}"
            )

            st.metric(
                "Vazão (kg/s)",
                f"{otimo['mdot']:.2f}"
            )

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(
            df["pi_MPa"],
            df["eta"] * 100,
            linewidth=2
        )

        ax.scatter(
            otimo["pi_MPa"],
            otimo["eta"] * 100,
            color="red",
            s=80,
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
            "Otimização da Pressão Intermediária"
        )

        ax.grid(True)
        ax.legend()

        st.pyplot(fig)

        st.subheader("Tabela Completa")

        st.dataframe(df)

        csv = df.to_csv(index=False)

        st.download_button(
            "Baixar CSV",
            csv,
            "rankine.csv",
            "text/csv"
        )

    except Exception as erro:

        st.error(f"Erro: {erro}")
