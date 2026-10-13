import numpy as np 
import pandas as pd 
# Configuración de semilla para garantizar reproducibilidad en todas las ejecuciones 
np.random.seed(42) 
# Tamaño de la muestra (1000 hogares encuestados) 
n_registros = 1000 
# 1. Generación de variables demográficas y geográficas 
codusu_list = [f"HOG_EPH_2026_{i:04d}" for i in range(1, n_registros + 1)] 
# Regiones INDEC (1: GBA, 40: NOA, 41: NEA, 42: Cuyo, 43: Pampeana, 44: Patagonia) 
regiones = np.random.choice( 
[1, 40, 41, 42, 43, 44], 
size=n_registros, 
p=[0.35, 0.15, 0.15, 0.10, 0.15, 0.10], 
) 
# Integrantes totales en el hogar (distribución Poisson centrada en 3 personas) 
integrantes = np.random.poisson(lam=2.3, size=n_registros) + 1 
# 2. Generación de variables socioeconómicas y educativas 
# Nivel educativo del jefe/a de hogar (1: Primaria Inc, 2: Primaria Comp, 3: Secund Inc, 4: Secund Comp, 5: Sup/Univ Comp, 9: S/R) 
nivel_ed = np.random.choice( 
    [1, 2, 3, 4, 5, 9], 
    size=n_registros, 
    p=[0.08, 0.22, 0.30, 0.25, 0.13, 0.02], 
) 
 
# Ingreso Total Familiar (ITF): modelado log-normal condicionado por el nivel educativo 
ingreso_base = { 
    1: 280000, 
    2: 420000, 
    3: 580000, 
    4: 850000, 
    5: 1450000, 
    9: 500000, 
} 
itf_list = [] 
 
for ed in nivel_ed: 
    mu = ingreso_base[ed] 
    # Generar variación estocástica de ingresos 
    val = np.random.lognormal(mean=np.log(mu), sigma=0.45) 
    itf_list.append(round(val, 2)) 
 
itf_array = np.array(itf_list) 
 
# Decil de Ingreso Total Familiar (1 a 10) calculado empíricamente 
decif_array = pd.qcut(itf_array, q=10, labels=list(range(1, 11))) 
 
# 3. Generación de variables tecnológicas (Brecha Digital) 
# A mayor nivel socioeconómico/educativo, mayor probabilidad de poseer PC e Internet 
prob_pc = [] 
prob_inet = [] 
 
for ed, decil in zip(nivel_ed, decif_array): 
    # Probabilidad base según educación 
    p_pc = 0.25 + (ed * 0.11) if ed != 9 else 0.45 
    p_inet = 0.45 + (ed * 0.08) if ed != 9 else 0.65 
 
    # Ajuste por decil de ingreso 
    p_pc += (int(decil) - 5) * 0.03 
    p_inet += (int(decil) - 5) * 0.025 
 
    prob_pc.append(np.clip(p_pc, 0.10, 0.95)) 
    prob_inet.append(np.clip(p_inet, 0.25, 0.98)) 
 
# Generar tenencias (1: Sí, 2: No, 9: Sin Respuesta) 
iv12_3 = [ 
    np.random.choice([1, 2, 9], p=[p, 0.98 - p, 0.02]) for p in prob_pc 
] 
ii7 = [ 
    np.random.choice([1, 2, 9], p=[p, 0.98 - p, 0.02]) for p in prob_inet 
] 
 
# 4. Estructuración del DataFrame con nomenclatura oficial INDEC 
data = { 
"CODUSU": codusu_list, 
"REGION": regiones, 
"IX_TOT": integrantes, 
"NIVEL_ED": nivel_ed, 
"ITF": itf_array, 
"DECIFR": decif_array, 
"IV12_3": iv12_3,  # ¿Posee computadora/laptop? 
"II7": ii7,  # ¿Tiene conexión a internet fija? 
} 
df_eph = pd.DataFrame(data) 
# 5. Inducir deliberadamente valores faltantes (NaN) para la práctica de limpieza de la Clase 2 
mask_nulos_itf = np.random.choice( 
[True, False], size=n_registros, p=[0.06, 0.94] 
) 
mask_nulos_pc = np.random.choice( 
[True, False], size=n_registros, p=[0.03, 0.97] 
) 
df_eph.loc[mask_nulos_itf, "ITF"] = np.nan 
df_eph.loc[mask_nulos_pc, "IV12_3"] = np.nan 
# 6. Exportar archivo CSV 
nombre_archivo = "eph_tecnologia_microdatos.csv" 
df_eph.to_csv(nombre_archivo, index=False) 
print(f"Dataset generado exitosamente: '{nombre_archivo}' con {df_eph.shape[0]} registros y {df_eph.shape[1]} columnas.")
