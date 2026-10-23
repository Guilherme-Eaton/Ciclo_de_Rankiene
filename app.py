import streamlit as st
import matplotlib.pyplot as plt

from rankine_otimizacao import otimizar_rankine

st.set_page_config(
    page_title="Ciclo Rankine Regenerativo",
    layout="wide"
)

st.title("Otimização do Ciclo Rankine Regenerativo")

# ===================================
# SIDEBAR
# ===================================

st.sidebar.header("Parâmetros")

mostrar_tabela = st.sidebar.checkbox(
    "Mostrar tabela completa",
    value=True
)

mostrar_grafico = st.sidebar.checkbox(
    "Mostrar gráfico",
    value=True
)

# ===================================
# BOTÃO
# ===================================

if st.button("Executar Otimização"):

    with st.spinner("Calculando..."):

        df, otimo = otimizar_rankine()

    st.success("Cálculo concluído!")

    # ===================================
    # RESULTADOS
    # ===================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Pressão ótima (MPa)",
            f"{otimo['pi']:.4f}"
        )

    with col2:
        st.metric(
            "Rendimento (%)",
            f"{otimo['eta'] * 100:.2f}"
        )

    with col3:
        st.metric(
            "Fração extraída",
            f"{otimo['y']:.4f}"
        )

    with col4:
        st.metric(
            "Vazão (kg/s)",
            f"{otimo['mdot']:.2f}"
        )

    # ===================================
    # GRÁFICO
    # ===================================

    if mostrar_grafico:

        st.subheader("Curva de Otimização")

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

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

        ax.grid(True)

        ax.legend()

        st.pyplot(fig)

    # ===================================
    # TABELA
    # ===================================

    if mostrar_tabela:

        st.subheader("Resultados Calculados")

        st.dataframe(
            df,
            use_container_width=True
        )

    # ===================================
    # DOWNLOAD CSV
    # ===================================

    csv = df.to_csv(index=False)

    st.download_button(
        label="📥 Baixar CSV",
        data=csv,
        file_name="rankine_resultados.csv",
        mime="text/csv"
    )
