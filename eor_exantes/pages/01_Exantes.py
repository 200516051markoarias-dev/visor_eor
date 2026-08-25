
import streamlit as st
import pandas as pd
import oracledb
from streamlit_calendar import calendar
from io import BytesIO

NODOS={
'Guatemala':['1124','1126','1710'],
'El Salvador':['27131','27211','27301'],
'Honduras':['3183','3211','3300','3301'],
'Nicaragua':['4402','4403','4406'],
'Costa Rica':['50000','50050','50100','50200'],
'Panamá':['6003','6005','6014','6018']
}

def conn():
    return oracledb.connect(user='USR3_27_2CC32',password='08EOR_Ingreso*',host='201.247.249.154',port=1521,service_name='BDRSQL')

st.title('Consulta Exantes')
tabla=st.selectbox('Tabla',['PUB004PEXANTE'])

pais=st.multiselect('Países',list(NODOS.keys()),default=['Guatemala'])
sel=[]
for p in pais: sel.extend(NODOS[p])
nodos=st.multiselect('Nodos',sel,default=sel[:1])
fi=st.date_input('Fecha inicial')
ff=st.date_input('Fecha final')

mes=fi.month
anio=fi.year

try:
    c = conn()
    cur = c.cursor()

    # q = f"""
    # SELECT DISTINCT TRUNC(FECHA_PUBLICACION)
    # FROM {tabla}
    # WHERE EXTRACT(MONTH FROM FECHA_PUBLICACION) = :1
    #   AND EXTRACT(YEAR FROM FECHA_PUBLICACION) = :2
    # """

    # cur.execute(q, [mes, anio])

    # fechas = [r[0] for r in cur.fetchall()]

    # events = [
    #     {
    #         "title": "Disponible",
    #         "start": d.strftime("%Y-%m-%d"),
    #         "color": "green"
    #     }
    #     for d in fechas
    # ]

    # calendar(
    #     events=events,
    #     options={
    #         "initialView": "dayGridMonth",
    #         "locale": "es"
    #     }
    # )

    if st.button("Exportar Excel") and nodos:

        nodos_sql = ",".join([f"'{n}'" for n in nodos])

        # q = f"""
        # SELECT *
        # FROM {tabla}
        # WHERE FECHA_PUBLICACION BETWEEN :1 AND :2
        #   AND NODO IN ({nodos_sql})
        # ORDER BY FECHA_PUBLICACION, PERIODO
        # """

        q = f"""
        SELECT nodo, fecha_publicacion, periodo, precioexante 
        FROM {tabla}
        WHERE FECHA_PUBLICACION BETWEEN :1 AND :2
          AND NODO IN ({nodos_sql})
        ORDER BY FECHA_PUBLICACION, PERIODO
        """

        cur.execute(q, [fi, ff])

        cols = [d[0] for d in cur.description]

        df = pd.DataFrame(
            cur.fetchall(),
            columns=cols
        )

        out = BytesIO()

        with pd.ExcelWriter(
            out,
            engine="openpyxl"
        ) as writer:

            df.to_excel(
                writer,
                sheet_name="Exantes",
                index=False
            )

        st.download_button(
            "Descargar XLSX",
            out.getvalue(),
            "Exantes.xlsx"
        )

except Exception as e:
    st.error(str(e))