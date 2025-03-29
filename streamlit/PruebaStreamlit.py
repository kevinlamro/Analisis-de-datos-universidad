import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import requests
import os

# URLs de los archivos en GitHub (RAW)
url_preferidos = "https://raw.githubusercontent.com/kevinlamro/Analisis-de-datos-universidad/main/streamlit/lugares_preferidos.xlsx"
url_completos = "https://raw.githubusercontent.com/kevinlamro/Analisis-de-datos-universidad/main/streamlit/lugares_completos.xlsx"

# Nombres de los archivos locales
archivo_preferidos = "lugares_preferidos.xlsx"
archivo_completos = "lugares_completos.xlsx"

# Función para descargar archivos si no existen
def descargar_archivo(url, archivo):
    if not os.path.exists(archivo):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(archivo, "wb") as file:
                    file.write(response.content)
                st.success(f"Archivo '{archivo}' descargado correctamente.")
            else:
                st.error(f"Error al descargar '{archivo}': {response.status_code}")
                st.stop()
        except Exception as e:
            st.error(f"Error al descargar '{archivo}': {e}")
            st.stop()

# Descargar ambos archivos si no existen
descargar_archivo(url_preferidos, archivo_preferidos)
descargar_archivo(url_completos, archivo_completos)

# Cargar los datos
try:
    df = pd.read_excel(archivo_completos)
except Exception as e:
    st.error(f"Error al cargar el archivo '{archivo_completos}': {e}")
    st.stop()

# 📌 Análisis de datos
moda = df["sitios"].mode()[0]
conteo_sitios = df["sitios"].value_counts()
porcentaje_sitios = (conteo_sitios / len(df)) * 100

niveles_satisfaccion = df[df["sitios"] == moda]["nivel de satisfaccion"]
media_satisfaccion = niveles_satisfaccion.mean()
mediana_satisfaccion = niveles_satisfaccion.median()
desviacion_satisfaccion = niveles_satisfaccion.std()

# 📌 Mostrar resultados en Streamlit
st.title("Análisis de Lugares Preferidos")

st.subheader("Sitio más elegido (Moda):")
st.write(moda)

st.subheader("Cantidad de personas por sitio:")
st.write(conteo_sitios)

st.subheader("Porcentaje de elección de cada sitio:")
st.write(porcentaje_sitios)

st.subheader("Estadísticas del sitio más elegido:")
st.write(f"Media: {media_satisfaccion:.2f}")
st.write(f"Mediana: {mediana_satisfaccion:.2f}")
st.write(f"Desviación estándar: {desviacion_satisfaccion:.2f}")

# 📊 Gráfica de Barras
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(conteo_sitios.index, conteo_sitios.values, color='skyblue', edgecolor='black')
ax1.set_xlabel('Sitios')
ax1.set_ylabel('Cantidad de personas')
ax1.set_title('Cantidad de personas por sitio preferido')
ax1.set_xticklabels(conteo_sitios.index, rotation=45, ha='right')
ax1.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig1)

# 📊 Gráfica de Pastel
fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.pie(conteo_sitios.values, labels=conteo_sitios.index, autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=140)
ax2.set_title('Distribución de sitios preferidos')
st.pyplot(fig2)

# 📊 Gráfica de Dispersión
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.scatter(df["sitios"], df["nivel de satisfaccion"], color='red', alpha=0.5)
ax3.set_xlabel("Sitios")
ax3.set_ylabel("Nivel de Satisfacción")
ax3.set_title("Relación entre Sitios y Nivel de Satisfacción")
ax3.set_xticklabels(df["sitios"].unique(), rotation=45, ha='right')
st.pyplot(fig3)

# 📊 Histograma de Niveles de Satisfacción
fig4, ax4 = plt.subplots(figsize=(10, 6))
ax4.hist(df["nivel de satisfaccion"], bins=5, color='green', edgecolor='black', alpha=0.7)
ax4.set_xlabel("Nivel de Satisfacción")
ax4.set_ylabel("Frecuencia")
ax4.set_title("Distribución de Niveles de Satisfacción")
ax4.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig4)

# 📊 Gráfica de Caja
fig5, ax5 = plt.subplots(figsize=(10, 6))
df.boxplot(column=["nivel de satisfaccion"], by="sitios", grid=False, ax=ax5, patch_artist=True, boxprops=dict(facecolor="lightblue"))
ax5.set_xlabel("Sitios")
ax5.set_ylabel("Nivel de Satisfacción")
ax5.set_title("Distribución del Nivel de Satisfacción por Sitio")
st.pyplot(fig5)

# 📌 Tabla de hallazgos
st.subheader("Hallazgos")
hallazgos = pd.DataFrame({
    "Métrica": ["Sitio más elegido", "Media Satisfacción", "Mediana Satisfacción", "Desviación Satisfacción"],
    "Valor": [moda, f"{media_satisfaccion:.2f}", f"{mediana_satisfaccion:.2f}", f"{desviacion_satisfaccion:.2f}"]
})
st.table(hallazgos)
