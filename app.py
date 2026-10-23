import numpy as np
import pandas as pd
from iapws import IAPWS97


def ciclo_rankine(
    P_HIGH=10.0,
    T_HIGH=500.0,
    P_LOW=0.01,
    ETA_T=0.80,
    POTENCIA_LIQ=100000,
    N=100
):

    estado1 = IAPWS97(P=P_LOW, x=0)

    h1 = estado1.h
    v1 = estado1.v

    estado5 = IAPWS97(
        P=P_HIGH,
        T=T_HIGH + 273.15
    )

    h5 = estado5.h
    s5 = estado5.s

    pressoes = np.logspace(
        np.log10(P_LOW),
        np.log10(P_HIGH),
        N
    )

    resultados = []

    for pi in pressoes:

        try:

            # Estado 2
            wb1 = v1 * ((pi - P_LOW) * 1000)
            h2 = h1 + wb1

            # Estado 3
            estado3 = IAPWS97(P=pi, x=0)

            h3 = estado3.h
            v3 = estado3.v

            # Estado 4
            wb2 = v3 * ((P_HIGH - pi) * 1000)

            h4 = h3 + wb2

            # Estado 6s
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

            # Estado 7s
            estado7s = IAPWS97(
                P=P_LOW,
                s=s6
            )

            h7s = estado7s.h

            h7 = h6 - ETA_T * (h6 - h7s)

            # Fração de extração
            y = (h3 - h2) / (h6 - h2)

            if y <= 0 or y >= 1:
                continue

            # Turbina
            wt = (
                (h5 - h6)
                +
                (1 - y) * (h6 - h7)
            )

            # Bombas
            wb = (
                (1 - y) * (h2 - h1)
                +
                (h4 - h3)
            )

            # Trabalho líquido
            wliq = wt - wb

            if wliq <= 0:
                continue

            # Calor fornecido
            qin = h5 - h4

            # Rendimento
            eta = wliq / qin

            # Vazão
            mdot = POTENCIA_LIQ / wliq

            resultados.append(
                {
                    "pi_MPa": pi,
                    "eta": eta,
                    "y": y,
                    "wt": wt,
                    "wb": wb,
                    "wliq": wliq,
                    "qin": qin,
                    "mdot": mdot
                }
            )

        except Exception:
            continue

    df = pd.DataFrame(resultados)

    if len(df) == 0:
        raise ValueError(
            "Nenhum ponto válido foi calculado."
        )

    indice = df["eta"].idxmax()

    otimo = df.loc[indice]

    return df, otimo
    
