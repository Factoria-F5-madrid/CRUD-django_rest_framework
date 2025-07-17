import streamlit as st
import requests

st.sidebar.title('Menú')
st.sidebar.write('Bienvenidxs a mi librería')

st.title('Bienvenidxs a mi librería')
st.write('Estos son mis libros desde mi API:')

response = requests.get('http://127.0.0.1:8000/v1/libros')
if response.status_code == 200:
    libros = response.json()
    for libro in libros:
        st.write(f"Titulo: {libro['titulo']}")
        if st.button(f"Ver detalle {libro['id']}"):
            st.write(libro)
        if st.button(f"Borrar {libro['id']}"):
            delete_response = requests.delete(f"http://127.0.0.1:8000/v1/libros/{libro['id']}")
            if delete_response.status_code == 204:
                st.write(f"Libro {libro['id']} borrado")
            else:
                st.write(f"No se pudo borrar el libro {libro['id']}")
else:
    st.write('No se encontraron libros')