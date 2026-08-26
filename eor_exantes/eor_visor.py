
import streamlit as st
st.set_page_config(page_title="EOR Exantes",layout="wide")
st.title("EOR Exantes")
st.info("Use el menú lateral para acceder al módulo Exantes")

import streamlit as st
import oracledb
from streamlit_calendar import calendar
from datetime import date

st.set_page_config(
    page_title="EOR Exantes",
    layout="wide"
)

st.title("Disponibilidad de Exantes")

tabla = 'PUB004PEXANTE'

def conn():
    return oracledb.connect(
        user="USR3_27_2CC32",
        password="08EOR_Ingreso*",
        host="201.247.249.154",
        port=1521,
        service_name="BDRSQL"
    )

fecha_ref = st.date_input(
    "Mes a consultar",
    value=date.today()
)

mes = fecha_ref.month
anio = fecha_ref.year

try:

    c = conn()
    cur = c.cursor()

    sql = f"""
    SELECT DISTINCT TRUNC(FECHA_PUBLICACION)
    FROM {tabla}
    WHERE EXTRACT(MONTH FROM FECHA_PUBLICACION)=:1
      AND EXTRACT(YEAR FROM FECHA_PUBLICACION)=:2
    ORDER BY 1
    """

    cur.execute(sql, [mes, anio])

    fechas = [r[0] for r in cur.fetchall()]

    eventos = [
        {
            "title": "Información Disp",
            "start": d.strftime("%Y-%m-%d"),
            "color": "#2E7D32"
        }
        for d in fechas
    ]

    calendar(
        events=eventos,
        options={
            "initialView": "dayGridMonth",
            "locale": "es"
        }
    )

    st.success(
        f"{len(fechas)} días encontrados para {tabla}"
    )

except Exception as e:
    st.error(str(e))
