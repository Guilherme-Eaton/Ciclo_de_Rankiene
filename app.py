import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO

from rankine_otimizacao import otimizar_rankine



st.set_page_config(
    page_title="Ciclo Rankine Regenerativo",
    layout="wide"
)

st.title("Otimização do Ciclo Rankine Regenerativo")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Parâmetros do Problema")

pH = st.sidebar.number_input(
    "Pressão máxima (MPa)",
    min_value=1.0,
    max_value=30.0,
    value=10.0,
    step=0.5
)

TH = st.sidebar.number_input(
    "Temperatura máxima (°C)",
    min_value=100,
    max_value=700,
    value=500
)

pL = st.sidebar.number_input(
    "Pressão mínima (MPa)",
    min_value=0.001,
    max_value=1.0,
    value=0.01,
    format="%.3f"
)

eta_t = st.sidebar.slider(
    "Eficiência da Turbina",
    min_value=0.50,
    max_value=1.00,
    value=0.80,
    step=0.01
)

potencia = st.sidebar.number_input(
    "Potência Líquida (MW)",
    min_value=1.0,
    max_value=1000.0,
    value=100.0
)

n_pontos = st.sidebar.slider(
    "Número de Pontos",
    min_value=50,
    max_value=500,
    value=100,
    step=50
)

mostrar_tabela = st.sidebar.checkbox(
    "Mostrar Tabela Completa",
    value=True
)

mostrar_grafico = st.sidebar.checkbox(
    "Mostrar Gráfico",
    value=True
)

# ==================================================
# BOTÃO
# ==================================================

if st.button("Executar Otimização"):

    with st.spinner("Calculando..."):

        df, otimo = otimizar_rankine(
            P_HIGH=pH,
            T_HIGH=TH,
            P_LOW=pL,
            ETA_T=eta_t,
            POTENCIA_LIQ=potencia * 1000,
            N=n_pontos
        )

    st.success("Cálculo concluído!")

    # ==================================================
    # RESULTADOS
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Pressão Ótima (MPa)",
            f"{otimo['pi']:.4f}"
        )

    with col2:
        st.metric(
            "Rendimento Máximo (%)",
            f"{otimo['eta']*100:.2f}"
        )

    with col3:
        st.metric(
            "Fração Extraída",
            f"{otimo['y']:.4f}"
        )

    with col4:
        st.metric(
            "Vazão Mássica (kg/s)",
            f"{otimo['mdot']:.2f}"
        )

    # ==================================================
    # GRÁFICO
    # ==================================================

    if mostrar_grafico:

        st.subheader("Curva η × Pressão Intermediária")

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        ax.plot(
            df["pi"],
            df["eta"] * 100,
            color="blue",
            linewidth=2
        )

        ax.scatter(
            otimo["pi"],
            otimo["eta"] * 100,
            color="red",
            s=120,
            label="Ponto Ótimo"
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

    # ==================================================
    # TABELA
    # ==================================================

    if mostrar_tabela:

        st.subheader("Tabela Completa de Resultados")

        st.dataframe(
            df,
            use_container_width=True
        )

    # ==================================================
    # DOWNLOAD CSV
    # ==================================================

    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name="rankine_resultados.csv",
        mime="text/csv"
    )
