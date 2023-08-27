import streamlit as st
import os
import base64
import sqlite3
import time

st.set_page_config(
    page_title="Jairo Untels",
    page_icon="🙃",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.linkedin.com/in/jairo-mendoza-torres/",
        "About": "Hice esta app para hacer algunas anotaciones de mi 7mo ciclo de la universidad 🤓",
    },
)


st.markdown(
    """<style>
/* Ocultar el elemento flotante */
Footer {
    display: none !important;
}
</style>
""",
    unsafe_allow_html=True,
)


st.title("Anotaciones de mi 7mo Ciclo")


class Mensaje:
    def __init__(self, semana, curso, mensaje):
        self.semana = semana
        self.curso = curso
        self.mensaje = mensaje


class Archivo:
    def __init__(self, semana, curso, nombre_archivo, archivo):
        self.semana = semana
        self.curso = curso
        self.nombre_archivo = nombre_archivo
        self.archivo = archivo


lista_2_cursos = [
    "Desarrollo de Aplicaciones para Móviles",
    "Análisis y Diseño de Sistemas",
    "SCRUM",
    "Gestión de Procesos de Negocios",
    "Sistemas Inteligentes",
    "Simulación de Sistemas",
    "Microprocesadores",
]


lista_de_cursos = st.tabs(lista_2_cursos)


def semana():
    semanas = []
    for i in range(1, 17):
        semanas.append(f"Semana {i}")
    return semanas


def traer_datos(curso, semana):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT semana, curso, mensaje FROM mensajes where curso = ? and semana = ?",
        (curso, semana),
    )
    records = cursor.fetchall()
    conn.close()
    lista_de_mensajes = []
    for record in records:
        semana, curso, mensaje = record
        msg = Mensaje(semana, curso, mensaje)
        lista_de_mensajes.append(msg)
    return lista_de_mensajes


def traer_archivos(curso, semana):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT semana, curso, nombre_archivo, archivo FROM archivos WHERE curso = ? AND semana = ?",
        (curso, semana),
    )
    records = cursor.fetchall()
    conn.close()
    lista_de_archivos = []
    for record in records:
        semana, curso, nombre_archivo, archivo_bytes = record
        archivo = Archivo(semana, curso, nombre_archivo, archivo_bytes)
        lista_de_archivos.append(archivo)
    return lista_de_archivos


def listar_anotaciones_con_archivos():
    semanas = semana()
    numero_de_cursos = range(0, 7)
    for numero_de_curso in numero_de_cursos:
        with lista_de_cursos[numero_de_curso]:
            for semana_actual in semanas:
                with st.expander(semana_actual):
                    lista_de_mensajes = traer_datos(
                        lista_2_cursos[numero_de_curso], semana_actual
                    )
                    for msg in lista_de_mensajes:
                        st.write(msg.mensaje)

                    archivos_adjuntos = traer_archivos(
                        lista_2_cursos[numero_de_curso], semana_actual
                    )

                    archivos_disponibles = [
                        archivo.nombre_archivo for archivo in archivos_adjuntos
                    ]
                    selected_file = st.selectbox(
                        "Selecciona un archivo para descargar:",
                        archivos_disponibles,
                        key=f"select_{numero_de_curso}_{semana_actual}",
                    )

                    archivo_elegido = next(
                        (
                            archivo
                            for archivo in archivos_adjuntos
                            if archivo.nombre_archivo == selected_file
                        ),
                        None,
                    )

                    if archivo_elegido:
                        download_key = f"download_{numero_de_curso}_{semana_actual}_{archivo_elegido.nombre_archivo}"
                        st.download_button(
                            label="Descargar",
                            data=archivo_elegido.archivo,
                            file_name=archivo_elegido.nombre_archivo,
                            mime="application/octet-stream",
                            key=download_key,
                        )


if __name__ == "__main__":
    listar_anotaciones_con_archivos()
