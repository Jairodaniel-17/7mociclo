import streamlit as st
import sqlite3
import time

st.title("Enviar datos a las anotaciones del curso")
prompt = st.chat_input(placeholder="Markdown es compatible, escribe un mensaje... ")

cursos = [
    "Desarrollo de Aplicaciones para Móviles",
    "Análisis y Diseño de Sistemas",
    "SCRUM",
    "Gestión de Procesos de Negocios",
    "Sistemas Inteligentes",
    "Simulación de Sistemas",
    "Microprocesadores",
]


def semana():
    semanas = []
    for i in range(1, 17):
        semanas.append(f"Semana {i}")
    return semanas


with st.container():
    seleccione_una_semana = st.sidebar.selectbox("Selecciona una semana", (semana()))
    seleccione_un_curso = st.sidebar.selectbox("Selecciona un curso", (cursos))
    enviar_archivo = st.sidebar.file_uploader(
        "Sube un archivo, no te olvides de escoger el curso y semana",
    )
    if enviar_archivo:
        subir_archivo = st.sidebar.button("Subir archivo")
        if subir_archivo:
            conn = sqlite3.connect("data.db")
            c = conn.cursor()
            if enviar_archivo is not None:
                archivo_data = enviar_archivo.read()
                nombre_archivo = enviar_archivo.name
                c.execute(
                    "INSERT INTO archivos (semana, curso, nombre_archivo, archivo) VALUES (?, ?, ?, ?)",
                    (
                        seleccione_una_semana,
                        seleccione_un_curso,
                        nombre_archivo,
                        archivo_data,
                    ),
                )
                conn.commit()
                conn.close()
                temporal = st.sidebar.empty()
                temporal.success("Datos guardados exitosamente")
                time.sleep(3)
                temporal.empty()

query_insertar_mensaje = (
    "INSERT INTO mensajes (mensaje, semana, curso) VALUES (?, ?, ?)"
)


def mostrar_mensaje_por_el_bot(mensaje, semana, curso):
    with st.chat_message(name="assistant", avatar="😊"):
        st.write(f"*Se enviara al curso de {curso} en la {semana}*")
        st.write(mensaje)


def enviar_mensaje():
    mensaje = prompt
    if mensaje:
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute(
            query_insertar_mensaje,
            (mensaje, seleccione_una_semana, seleccione_un_curso),
        )
        conn.commit()
        conn.close()
    if mensaje:
        mostrar_mensaje_por_el_bot(mensaje, seleccione_una_semana, seleccione_un_curso)


def main():
    enviar_mensaje()


if __name__ == "__main__":
    main()
