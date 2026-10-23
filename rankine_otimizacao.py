import numpy as np
import pandas as pd
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
# FUNÇÃO DE CÁLCULO DE UM PONTO
# =====================================================

def ciclo_rankine(pi):

    try:

        wb1 = v1 * ((pi - P_LOW) * 1000)
        h2 = h1 + wb1

        estado3 = IAPWS97(
            P=pi,
            x=0
        )

        h3 = estado3.h
        v3 = estado3.v

        wb2 = v3 * ((P_HIGH - pi) * 1000)
        h4 = h3 + wb2

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

        estado7s = IAPWS97(
            P=P_LOW,
            s=s6
        )

        h7s = estado7s.h

        h7 = h6 - ETA_T * (h6 - h7s)

        y = (h3 - h2) / (h6 - h2)

        if not (0 < y < 1):
            return None

        wt = (
            (h5 - h6)
            +
            (1 - y) * (h6 - h7)
        )

        wb = (
            (1 - y) * (h2 - h1)
            +
            (h4 - h3)
        )

        wliq = wt - wb

        if wliq <= 0:
            return None

        qin = h5 - h4

        eta = wliq / qin

        mdot = POTENCIA_LIQ / wliq

        return {
            "pi": pi,
            "y": y,
            "wt": wt,
            "wb": wb,
            "wliq": wliq,
            "qin": qin,
            "eta": eta,
            "mdot": mdot
        }

    except Exception:
        return None


# =====================================================
# FUNÇÃO DE OTIMIZAÇÃO (100 PONTOS)
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

    if len(resultados) == 0:
        raise Exception(
            "Nenhum ponto válido foi calculado."
        )

    df = pd.DataFrame(resultados)

    indice = df["eta"].idxmax()

    otimo = df.loc[indice]

    return df, otimo
