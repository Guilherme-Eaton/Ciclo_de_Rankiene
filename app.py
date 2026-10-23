import streamlit as st
import inspect

from rankine_otimizacao import ciclo_rankine

st.write(inspect.signature(ciclo_rankine))
