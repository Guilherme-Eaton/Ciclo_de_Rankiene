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

    pressao = np.logspace(
        np.log10(P_LOW),
        np.log10(P_HIGH),
        N
    )

    resultado = []

    for pi in pressao:

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

            if y <= 0 or y >= 1:
                continue

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

            qin = h5 - h4

            eta = wliq / qin

            mdot = POTENCIA_LIQ / wliq

            resultado.append(
                {
                    "pi_MPa": pi,
                    "eta": eta,
                    "y": y,
                    "wt": wt,
                    "wb": wb,
                    "wliq": wliq,
                    "qin": qin,
                    "mdot": mdot,
                }
            )

        except Exception:
            pass

    df = pd.DataFrame(resultado)

    if len(df) == 0:
        raise ValueError(
            "Nenhum ponto válido foi calculado."
        )

    indice = df["eta"].idxmax()

    otimo = df.loc[indice]

    return df, otimo
    
