# 🛒 Retail Sales Dashboard — Versión 2 (Actualización Automática)

Este proyecto es la **versión 2** de mi *Retail Sales Dashboard*, ahora con un **flujo de actualización automática del dataset** mediante un script en **Python** y **Windows Task Scheduler**, sumado a un **modelo en estrella en Power BI** totalmente reprocesado para soportar actualizaciones sin intervención manual.

---

## 🎯 Objetivo del proyecto

Construir un dashboard profesional de ventas minoristas que:

- Centralice datos crudos de transacciones.
- Realice un proceso ETL automático con Python (limpieza + transformación).
- Se actualice de forma programada mediante Windows Task Scheduler.
- Utilice un **modelo en estrella** para análisis eficientes.
- Presente indicadores clave (KPI) en Power BI listos para negocio.

---

## ⚙️ ETL Automatizado (Python)

El archivo `update_dataset.py` realiza:

### ✔ Limpieza de datos
- Normalización de fechas (con `dayfirst=True`)
- Limpieza de valores faltantes
- Conversión de tipos numéricos
- Eliminación de filas inválidas

### ✔ Transformaciones generadas automáticamente
- `Total Amount` = Quantity × Price per Unit  
- `Year`, `Month`, `MonthName`
- `Age Band`
- Estandarización de `Product Category`, `Gender`, `Age`

### ✔ Exportación final
El script genera automáticamente:
- data/processed/retail_sales_clean.csv
que es la fuente principal del modelo Power BI.

---

## 🔄 Flujo automático (Python → BAT → Task Scheduler → Power BI)

### 1️⃣ El usuario o un proceso actualiza el archivo crudo:
- data/raw/retail_sales_dataset.csv

### 2️⃣ El archivo `.bat` ejecuta el script Python:
- actualizar_retail_sales.bat

### 3️⃣ Windows Task Scheduler ejecuta ese `.bat` **de forma programada**  
(en este caso, diariamente a las 11:30).

### 4️⃣ Power BI toma automáticamente el archivo limpio:
- data/processed/retail_sales_clean.csv

y con un clic en **Actualizar**, el dashboard refresca todas las métricas.

---

## 📈 Visualizaciones destacadas

- **Ventas por categoría** (gráfico de barras)
- **Ventas por mes y año** (gráfico de líneas)
- **Distribución por género** (gráfico donut)
- **Análisis por banda etaria** (barras)
- **KPI principales**:
  - Ventas totales
  - Unidades vendidas
  - Ticket promedio
- **Segmentadores dinámicos**:
  - Categoría
  - Edad
  - Género
  - Año
  - Mes

---

## 👤 Sobre mí

Soy **Javier Reitano**, Contador Público Nacional (título Universitario) y en desarrollo en el **análisis de datos, automatización y Business Intelligence**.

Trabajo con:

- **Python** (Pandas, ETL, automatizaciones)
- **Power BI** (DAX, modelado en estrella, visualizaciones)
- **GitHub** (versionado profesional y portfolio)

Mi objetivo es crear dashboards claros, dinámicos y totalmente automatizados para la toma de decisiones.

🔗 **LinkedIn:** https://www.linkedin.com/in/javier-alejandro-reitano-ab4952243/






  


