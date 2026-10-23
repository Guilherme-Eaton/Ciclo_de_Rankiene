import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from iapws import IAPWS97
import streamlit as st
st.title("Teste streamlit")
st.sucess("Funcionando!")

# =====================================================
# DADOS DO PROBLEMA
# =====================================================

P_HIGH = 10.0      # MPa
T_HIGH = 500.0     # °C
P_LOW = 0.01       # MPa (10 kPa)
ETA_T = 0.80
POTENCIA_LIQ = 100000.0  # kW

# =====================================================
# ESTADO 1
# =====================================================

estado1 = IAPWS97(P=P_LOW, x=0)

h1 = estado1.h
s1 = estado1.s
v1 = estado1.v

# =====================================================
# ESTADO 5
# =====================================================

estado5 = IAPWS97(
    P=P_HIGH,
    T=T_HIGH + 273.15
)

h5 = estado5.h
s5 = estado5.s

# =====================================================
# FUNÇÃO DO CICLO
# =====================================================

def ciclo_rankine(pi):
    try:
        # -------------------------
        # Estado 2
        # -------------------------
      
        wb1 = v1 * ((pi - P_LOW) * 1000)
        h2 = h1 + wb1
      
        # -------------------------
        # Estado 3
        # -------------------------

        estado3 = IAPWS97(P=pi, x=0)

        h3 = estado3.h
        v3 = estado3.v

        # -------------------------
        # Estado 4
        # -------------------------

        wb2 = v3 * ((P_HIGH - pi) * 1000)
        h4 = h3 + wb2

        # -------------------------
        # Estado 6s
        # -------------------------

        estado6s = IAPWS97(
            P=pi,
            s=s5
        )

        h6s = estado6s.h
        h6 = h5 - ETA_T * (h5 - h6s)
        estado6 = IAPWS97(
            P=pi,
            h=h6
        )

        s6 = estado6.s

        # -------------------------
        # Estado 7s
        # -------------------------

        estado7s = IAPWS97(
            P=P_LOW,
            s=s6
        )

        h7s = estado7s.h

        h7 = h6 - ETA_T * (h6 - h7s)

        # -------------------------
        # Fração extraída
        # -------------------------

        y = (h3 - h2) / (h6 - h2)

        if y <= 0 or y >= 1:
            return None

        # -------------------------
        # Turbina
        # -------------------------

        wt = (
            (h5 - h6)
            +
            (1 - y) * (h6 - h7)
        )

        # -------------------------
        # Bombas
        # -------------------------

        wb = (
            (1 - y) * (h2 - h1)
            +
            (h4 - h3)
        )

        # -------------------------
        # Trabalho líquido
        # -------------------------

        wliq = wt - wb

        # -------------------------
        # Calor fornecido
        # -------------------------

        qin = h5 - h4

        # -------------------------
        # Rendimento
        # -------------------------

        eta = wliq / qin

        # -------------------------
        # Vazão mássica
        # -------------------------

        mdot = POTENCIA_LIQ / wliq

        return {

            "pi": pi,
            "h2": h2,
            "h3": h3,
            "h4": h4,
            "h6": h6,
            "h7": h7,
            "y": y,
            "wt": wt,
            "wb": wb,
            "wliq": wliq,
            "qin": qin,
            "eta": eta,
            "mdot": mdot
        }

    except:
        return None

# =====================================================
# 100 PONTOS
# =====================================================

pressao = np.logspace(
    np.log10(P_LOW),
    np.log10(P_HIGH),
    100
)

resultado = []

for pi in pressao:
    r = ciclo_rankine(pi)
    if r is not None:
        resultado.append(r)

df = pd.DataFrame(resultado)

# =====================================================
# ÓTIMO
# =====================================================

indice = df["eta"].idxmax()

otimo = df.loc[indice]

# =====================================================
# EXCEL
# =====================================================

with pd.ExcelWriter(
    "rankine_otimizado.xlsx",
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Varredura",
        index=False
    )

    resumo = pd.DataFrame({

        "Parametro": [

            "Pressao otima MPa",
            "Rendimento maximo",
            "Vazao kg/s",
            "Fracao extraida"

        ],

        "Valor": [

            otimo["pi"],
            otimo["eta"],
            otimo["mdot"],
            otimo["y"]

        ]

    })

    resumo.to_excel(
        writer,
        sheet_name="Resumo",
        index=False
    )

# =====================================================
# GRAFICO
# =====================================================

plt.figure(figsize=(10,6))

plt.plot(
    df["pi"],
    df["eta"]*100,
    marker="o"
)

plt.xscale("log")

plt.xlabel("Pressao intermediaria (MPa)")
plt.ylabel("Rendimento (%)")

plt.title(
    "Otimizacao da pressao intermediaria"
)

plt.grid(True)

plt.savefig(
    "grafico_rankine.png",
    dpi=300
)

plt.show()

# =====================================================
# CSV
# =====================================================

df.to_csv(
    "rankine_otimizado.csv",
    index=False
)

# =====================================================
# RESULTADO FINAL
# =====================================================

print("\n===================================")

print(
    f"PRESSAO OTIMA = {otimo['pi']:.4f} MPa"
)

print(
    f"RENDIMENTO = {otimo['eta']*100:.4f} %"
)

print(
    f"Y = {otimo['y']:.4f}"
)

print(
    f"VAZAO = {otimo['mdot']:.4f} kg/s"
)

print("===================================")
