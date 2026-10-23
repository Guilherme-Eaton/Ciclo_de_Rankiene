import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from iapws import IAPWS97

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

def otimizar_rankine():

    pressoes = np.logspace(
        np.log10(P_LOW),
        np.log10(P_HIGH),
        100
    )

    resultados = []

    for pi in pressoes:

        r = ciclo_rankine(pi)

        if r is not None:
            resultados.append(r)

    df = pd.DataFrame(resultados)

    indice = df["eta"].idxmax()

    otimo = df.loc[indice]

    return df, otimo

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
