import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import os

# Nombre del archivo con los datos completos
archivo_completo = "lugares_completos.xlsx"

# Verificar si ya existen los datos completos
if os.path.exists(archivo_completo):
    df = pd.read_excel(archivo_completo)
else:
    try:
        df = pd.read_excel("lugares_preferidos.xlsx")
    except FileNotFoundError:
        st.error("Archivo 'lugares_preferidos.xlsx' no encontrado.")
        st.stop()
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        st.stop()

    total_datos = 300
    datos_reales = len(df)
    datos_faltantes = total_datos - datos_reales

    if datos_faltantes > 0:
        conteo_sitios = df["sitios"].value_counts()
        nuevos_sitios = np.random.choice(conteo_sitios.index, size=datos_faltantes, p=conteo_sitios.values / conteo_sitios.sum())
        nuevos_niveles_satisfaccion = np.random.randint(1, 6, size=datos_faltantes)
        carreras_existentes = df["carreras"].unique()
        nuevas_carreras = np.random.choice(carreras_existentes, size=datos_faltantes)

        nombres = ["Juan", "Santiago", "Mateo", "Valentina", "Sofía", "Andrés", "Camila", "Sebastián"]
        apellidos = ["Gómez", "Rodríguez", "López", "Martínez", "González", "Hernández"]
        nuevos_nombres = [f"{np.random.choice(nombres)} {np.random.choice(apellidos)}" for _ in range(datos_faltantes)]

        df_nuevos = pd.DataFrame({
            "nombres": nuevos_nombres,
            "sitios": nuevos_sitios,
            "nivel de satisfaccion": nuevos_niveles_satisfaccion,
            "carreras": nuevas_carreras
        })

        df = pd.concat([df, df_nuevos], ignore_index=True)
        df.to_excel(archivo_completo, index=False)

# Análisis de datos
moda = df["sitios"].mode()[0]
conteo_sitios = df["sitios"].value_counts()
porcentaje_sitios = (conteo_sitios / len(df)) * 100

niveles_satisfaccion = df[df["sitios"] == moda]["nivel de satisfaccion"]
media_satisfaccion = niveles_satisfaccion.mean()
mediana_satisfaccion = niveles_satisfaccion.median()
desviacion_satisfaccion = niveles_satisfaccion.std()

# Mostrar resultados en Streamlit
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

# Gráfica de Barras
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.bar(conteo_sitios.index, conteo_sitios.values, color='skyblue', edgecolor='black')
ax1.set_xlabel('Sitios')
ax1.set_ylabel('Cantidad de personas')
ax1.set_title('Cantidad de personas por sitio preferido')
ax1.set_xticklabels(conteo_sitios.index, rotation=45, ha='right')
ax1.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig1)

# Gráfica de Pastel
fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.pie(conteo_sitios.values, labels=conteo_sitios.index, autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=140)
ax2.set_title('Distribución de sitios preferidos')
st.pyplot(fig2)

# Gráfica de Dispersión
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.scatter(df["sitios"], df["nivel de satisfaccion"], color='red', alpha=0.5)
ax3.set_xlabel("Sitios")
ax3.set_ylabel("Nivel de Satisfacción")
ax3.set_title("Relación entre Sitios y Nivel de Satisfacción")
ax3.set_xticklabels(df["sitios"].unique(), rotation=45, ha='right')
st.pyplot(fig3)

# Histograma de Niveles de Satisfacción
fig4, ax4 = plt.subplots(figsize=(10, 6))
ax4.hist(df["nivel de satisfaccion"], bins=5, color='green', edgecolor='black', alpha=0.7)
ax4.set_xlabel("Nivel de Satisfacción")
ax4.set_ylabel("Frecuencia")
ax4.set_title("Distribución de Niveles de Satisfacción")
ax4.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig4)

# Gráfica de Caja
fig5, ax5 = plt.subplots(figsize=(10, 6))
df.boxplot(column=["nivel de satisfaccion"], by="sitios", grid=False, ax=ax5, patch_artist=True, boxprops=dict(facecolor="lightblue"))
ax5.set_xlabel("Sitios")
ax5.set_ylabel("Nivel de Satisfacción")
ax5.set_title("Distribución del Nivel de Satisfacción por Sitio")
st.pyplot(fig5)


# Tabla de hallazgos
st.subheader("Hallazgos")
hallazgos = pd.DataFrame({
    "Métrica": ["Sitio más elegido", "Media Satisfacción", "Mediana Satisfacción", "Desviación Satisfacción"],
    "Valor": [moda, f"{media_satisfaccion:.2f}", f"{mediana_satisfaccion:.2f}", f"{desviacion_satisfaccion:.2f}"]
})
st.table(hallazgos)

