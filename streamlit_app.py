import streamlit as st
import pandas as pd

def filtrar_historial_por_accion(archivo, hoja_nombre, palabra_clave):
    """
    Lee un archivo Excel (puede ser un objeto cargado con streamlit.file_uploader),
    filtra los datos de la hoja especificada basándose en una palabra clave en la columna 'Acción'
    y devuelve un DataFrame con las filas filtradas.
    """
    try:
        # Leer la hoja especificada del archivo Excel.
        # Dado que "archivo" es un objeto tipo BytesIO, pd.read_excel lo procesa sin problemas.
        df = pd.read_excel(archivo, sheet_name=hoja_nombre, dtype=str)

        # Verificar si la columna 'Acción' existe.
        if 'Acción' not in df.columns:
            st.error(f"Error: La columna 'Acción' no se encontró en la hoja '{hoja_nombre}'.")
            return pd.DataFrame()

        # Rellenar valores NaN en la columna 'Acción' para evitar errores en la búsqueda.
        df['Acción'] = df['Acción'].fillna('')

        # Filtrar el DataFrame buscando la palabra clave sin distinguir mayúsculas/minúsculas.
        df_filtrado = df[df['Acción'].str.contains(palabra_clave, case=False, na=False)]
        return df_filtrado

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
        return pd.DataFrame()

def main():
    st.title("Filtrado de Historial por Acción")
    st.write("Esta aplicación carga un archivo Excel, filtra los registros de la hoja "
             "especificada según una palabra clave en la columna 'Acción', y muestra los resultados.")

    # Widget para cargar el archivo Excel.
    archivo_excel = st.file_uploader("Selecciona un archivo Excel", type=["xlsx", "xls"])

    if archivo_excel is not None:
        # Entrada para el nombre de la hoja con un valor por defecto.
        hoja_nombre = st.text_input("Ingresa el nombre de la hoja", value="Historial")
        # Entrada para la palabra clave a buscar.
        palabra_clave = st.text_input("Ingresa la palabra clave para filtrar en la columna 'Acción'")

        # Botón para ejecutar el filtrado.
        if st.button("Filtrar"):
            if not palabra_clave:
                st.warning("Por favor, ingresa una palabra clave para buscar.")
            else:
                df_filtrado = filtrar_historial_por_accion(archivo_excel, hoja_nombre, palabra_clave)
                
                if df_filtrado.empty:
                    st.info(f"No se encontraron registros que contengan '{palabra_clave}' en la columna 'Acción'.")
                else:
                    st.subheader("Registros Encontrados")
                    st.dataframe(df_filtrado)

if __name__ == "__main__":
    main()
