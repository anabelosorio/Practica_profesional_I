# Proyecto: Brecha Digital en Argentina (EPH - INDEC)
# Práctica Profesional I
#
# Este script hace todo el proceso:
# 1. Carga los datos
# 2. Los limpia y genera df_clean.csv
# 3. Calcula estadísticas y tablas
# 4. Hace los gráficos

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# ---------------------------------------------------------------
# 1. CARGA DE DATOS
# ---------------------------------------------------------------
df = pd.read_csv("DATA/eph_tecnologia_microdatos2.csv", sep=";")

print("Cantidad de hogares:", len(df))
print(df.head())
print("\nValores nulos por columna:")
print(df.isnull().sum())

# ---------------------------------------------------------------
# 2. LIMPIEZA
# ---------------------------------------------------------------
# El código 9 significa "no sabe / no responde", lo pasamos a nulo
for col in ["NIVEL_ED", "II7", "IV12_3"]:
    df[col] = df[col].replace(9, None)

# Sacamos los hogares que no tienen ingreso informado
df = df.dropna(subset=["ITF"])

# Calculamos el ingreso per cápita familiar (IPCF)
df["IPCF"] = df["ITF"] / df["IX_TOT"]

# Pasamos los códigos a nombres para que se entienda
regiones = {1: "GBA", 40: "NOA", 41: "NEA", 42: "Cuyo", 43: "Pampeana", 44: "Patagonia"}
niveles = {1: "Primario incompleto", 2: "Primario completo", 3: "Secundario incompleto",
           4: "Secundario completo", 5: "Superior"}
si_no = {1: "Sí", 2: "No"}

df["REGION_NOMBRE"] = df["REGION"].map(regiones)
df["NIVEL_EDUCATIVO"] = df["NIVEL_ED"].map(niveles)
df["INTERNET"] = df["II7"].map(si_no)
df["COMPUTADORA"] = df["IV12_3"].map(si_no)

# Armamos quintiles de ingreso per cápita (Q1 = más pobres, Q5 = más ricos)
df["QUINTIL"] = pd.qcut(df["IPCF"], 5, labels=["Q1", "Q2", "Q3", "Q4", "Q5"])

df.to_csv("DATA/df_clean.csv", index=False)
print("\nDataset limpio guardado. Hogares:", len(df))

# ---------------------------------------------------------------
# 3. ANÁLISIS
# ---------------------------------------------------------------
print("\n--- Estadísticas del ingreso per cápita (IPCF) ---")
print(df["IPCF"].describe())

print("\n--- Hogares con Internet (%) ---")
print(df["INTERNET"].value_counts(normalize=True) * 100)

print("\n--- Hogares con computadora (%) ---")
print(df["COMPUTADORA"].value_counts(normalize=True) * 100)

orden_educ = list(niveles.values())


def tabla_y_chi2(variable, tecnologia):
    """Muestra la tabla cruzada en % y el resultado del test chi-cuadrado."""
    tabla = pd.crosstab(df[variable], df[tecnologia], normalize="index") * 100
    chi2, p, gl, esperado = chi2_contingency(pd.crosstab(df[variable], df[tecnologia]))
    print(f"\n--- {variable} vs {tecnologia} (%) ---")
    print(tabla.round(1))
    print(f"Chi-cuadrado = {chi2:.2f}  p-valor = {p:.4f}")
    if p < 0.05:
        print("=> Hay relación significativa")
    else:
        print("=> No hay relación significativa")


# H1: ingreso
print("\n--- Media y mediana del IPCF según acceso a Internet ---")
print(df.groupby("INTERNET")["IPCF"].agg(["mean", "median", "count"]).round(0))
print("\n--- Media y mediana del IPCF según tenencia de computadora ---")
print(df.groupby("COMPUTADORA")["IPCF"].agg(["mean", "median", "count"]).round(0))

tabla_y_chi2("QUINTIL", "INTERNET")
tabla_y_chi2("QUINTIL", "COMPUTADORA")
# H2: educación
tabla_y_chi2("NIVEL_EDUCATIVO", "INTERNET")
tabla_y_chi2("NIVEL_EDUCATIVO", "COMPUTADORA")
# H3: región
tabla_y_chi2("REGION_NOMBRE", "INTERNET")
tabla_y_chi2("REGION_NOMBRE", "COMPUTADORA")

# ---------------------------------------------------------------
# 4. GRÁFICOS
# ---------------------------------------------------------------
sns.set_theme(style="whitegrid")

# Para graficar usamos 100 = tiene, 0 = no tiene (así el promedio da el %)
df["tiene_internet"] = df["INTERNET"].map({"Sí": 100, "No": 0})
df["tiene_pc"] = df["COMPUTADORA"].map({"Sí": 100, "No": 0})

# Gráfico 1: distribución del ingreso per cápita
plt.figure(figsize=(8, 4))
sns.histplot(df["IPCF"], bins=40)
plt.axvline(df["IPCF"].median(), color="red", linestyle="--", label="Mediana")
plt.title("Distribución del ingreso per cápita familiar")
plt.xlabel("IPCF ($)")
plt.ylabel("Cantidad de hogares")
plt.legend()
plt.savefig("graficos/1_distribucion_ipcf.png", bbox_inches="tight")
plt.close()


def grafico_barras(variable, archivo, titulo, orden=None):
    datos = df.groupby(variable, observed=True)[["tiene_internet", "tiene_pc"]].mean()
    if orden:
        datos = datos.reindex(orden)
    datos.columns = ["Internet", "Computadora"]
    datos.plot(kind="bar", figsize=(8, 4), color=["steelblue", "orange"])
    plt.title(titulo)
    plt.ylabel("% de hogares")
    plt.xlabel("")
    plt.xticks(rotation=20)
    plt.ylim(0, 100)
    plt.savefig("graficos/" + archivo, bbox_inches="tight")
    plt.close()


# Gráfico 2: acceso según quintil de ingreso
grafico_barras("QUINTIL", "2_acceso_por_quintil.png", "Acceso según quintil de ingreso")
# Gráfico 3: acceso según nivel educativo
grafico_barras("NIVEL_EDUCATIVO", "3_acceso_por_educacion.png",
               "Acceso según nivel educativo del jefe/a de hogar", orden_educ)
# Gráfico 4: acceso según región
grafico_barras("REGION_NOMBRE", "4_acceso_por_region.png", "Acceso según región")

# Gráfico 5: tortas comparando el quintil más pobre (Q1) con el más rico (Q5)
fig, ejes = plt.subplots(1, 2, figsize=(9, 4))
for eje, quintil, titulo in zip(ejes, ["Q1", "Q5"], ["Q1 (20% más pobre)", "Q5 (20% más rico)"]):
    datos = df[df["QUINTIL"] == quintil]["COMPUTADORA"].value_counts()
    datos = datos.reindex(["Sí", "No"])
    eje.pie(datos, labels=["Tiene computadora", "No tiene"], autopct="%1.1f%%",
            colors=["orange", "lightgrey"], startangle=90)
    eje.set_title(titulo)
plt.suptitle("Tenencia de computadora: hogares más pobres vs. más ricos", y=1.04)
plt.savefig("graficos/5_computadora_q1_vs_q5.png", bbox_inches="tight")
plt.close()

print("\nGráficos guardados en la carpeta 'graficos'")
