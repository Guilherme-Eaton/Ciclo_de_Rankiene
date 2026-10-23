import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Otimização do Ciclo Rankine")

# Dados de exemplo
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Cria o gráfico
fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(x, y, color="blue")
ax.set_title("Gráfico de Teste")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(True)

# Mostra no Streamlit
st.pyplot(fig)
