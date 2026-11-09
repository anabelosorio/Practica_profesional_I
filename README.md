# Practica_profesional_I

Soy Anabel Osorio  con experiencia en recolección, limpieza, análisis y visualización de datos para resolver preguntas concretas de negocio. 
Trabajo desde la pregunta hacia el dato: antes de armar un gráfico, defino qué decisión necesita tomar el cliente y qué información la respalda.

Mi objetivo no es entregar tablas, sino respuestas: qué está pasando, por qué pasa y qué conviene hacer.

Lo que me diferencia

Enfoque en el negocio: cada análisis parte de una pregunta clara y termina en una recomendación accionable.

Datos confiables: valido, limpio y documento los datos antes de analizarlos, para que las conclusiones se sostengan.

Comunicación clara: presento resultados con visualizaciones simples y explicaciones sin jerga técnica.

Ética y privacidad: trato los datos según principios de confidencialidad, minimización y transparencia, en línea con la Ley 25.326 de Protección de los Datos Personales.

Stack

Datos: SQL · Python (Pandas, NumPy) · Excel 
Visualización: Power BI/Tableau 
Buenas prácticas: limpieza y validación de datos · documentación · ética y protección de datos personales

# Brecha Digital en Argentina - EPH (INDEC)

Proyecto de la materia **Práctica Profesional I** (Técnico Superior en Ciencia de Datos e IA).

El objetivo es analizar cómo el ingreso, el nivel educativo y la región influyen en que un hogar tenga conexión a Internet y computadora, 
usando datos de la Encuesta Permanente de Hogares (EPH - INDEC).

## Estructura

```
DATA/         -> datos originales y dataset limpio (df_clean.csv)
notebooks/    -> notebook con el análisis paso a paso
graficos/     -> gráficos generados
informe/      -> informe técnico en PDF
main.py       -> script que hace todo el proceso
```

## Cómo ejecutarlo

```
pip install -r requirements.txt
python main.py
```

## Variables usadas

- `REGION`: región del país
- `NIVEL_ED`: nivel educativo del jefe/a de hogar
- `ITF`: ingreso total familiar
- `IX_TOT`: cantidad de personas en el hogar
- `IPCF`: ingreso per cápita (lo calculamos como ITF / IX_TOT)
- `II7`: tiene conexión a Internet (1 = sí, 2 = no)
- `IV12_3`: tiene computadora (1 = sí, 2 = no)

## Resultados principales

- El 73,7% de los hogares tiene Internet y el 64,1% tiene computadora.
- En los hogares más pobres (Q1) solo el 48% tiene computadora, contra el 83% en los más ricos (Q5).
- Cuando el jefe/a de hogar no terminó la primaria, solo el 43% de los hogares tiene Internet. Con estudios superiores llega al 98%.
- No encontramos diferencias importantes entre regiones.
