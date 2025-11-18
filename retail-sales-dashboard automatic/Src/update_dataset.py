import pandas as pd
from pathlib import Path
from datetime import datetime


# ==== RUTAS BASE ====
BASE_DIR = Path(__file__).resolve().parent.parent  # carpeta raíz del repo
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

RAW_FILE = RAW_DIR / "retail_sales_dataset.csv"
OUTPUT_FILE = PROCESSED_DIR / "retail_sales_clean.csv"


def load_raw_data() -> pd.DataFrame:
    """Lee el dataset crudo desde CSV."""
    print(f"[{datetime.now()}] Leyendo datos crudos de: {RAW_FILE}")

    # Si te da error de encoding, probá con encoding='latin-1' o 'cp1252'
    df = pd.read_csv(RAW_FILE)
    return df


def clean_numeric_column(series: pd.Series) -> pd.Series:
    """
    Limpia una columna numérica que puede venir como texto,
    con comas de miles o como separador decimal.
    """
    s = series.astype(str).str.strip()

    # Elimina espacios
    s = s.str.replace(" ", "", regex=False)

    # Reemplaza comas por puntos (por si son decimales tipo '12,5')
    s = s.str.replace(",", ".", regex=False)

    # Convierte a número
    return pd.to_numeric(s, errors="coerce")


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica las transformaciones necesarias al dataset."""

    print(f"[{datetime.now()}] Transformando datos...")

    # ==== 1) Normalizar nombres de columnas (por seguridad) ====
    df.columns = [c.strip() for c in df.columns]

    # Esperamos estas columnas:
    expected_cols = [
        "Transaction ID",
        "Date",
        "Customer ID",
        "Gender",
        "Age",
        "Product Category",
        "Quantity",
        "Price per Unit",
        "Total Amount",
    ]

    missing = [c for c in expected_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas esperadas en el CSV crudo: {missing}")

    # ==== 2) Convertir fecha ====
    # Intento flexible: dd/mm/yyyy y yyyy-mm-dd
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce",
        dayfirst=True,          # importante por formatos europeos
        infer_datetime_format=True
    )

    # Eliminar filas sin fecha válida
    before_rows = len(df)
    df = df.dropna(subset=["Date"])
    after_rows = len(df)
    print(f"Filas eliminadas por fecha inválida: {before_rows - after_rows}")

    # ==== 3) Convertir columnas numéricas ====
    df["Quantity"] = clean_numeric_column(df["Quantity"]).fillna(0).astype("int64")
    df["Price per Unit"] = clean_numeric_column(df["Price per Unit"])

    # Total Amount: lo recalculamos para asegurar coherencia
    df["Total Amount"] = df["Quantity"] * df["Price per Unit"]

    # ==== 4) Crear columnas de calendario ====
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.month_name()

    # ==== 5) Crear Age Band (segmentos de edad) ====
    df["Age"] = clean_numeric_column(df["Age"])

    bins = [0, 18, 25, 35, 50, 65, 120]
    labels = ["<18", "18-24", "25-34", "35-49", "50-64", "65+"]

    df["Age Band"] = pd.cut(
        df["Age"],
        bins=bins,
        labels=labels,
        right=False,       # intervalo [x, y)
        include_lowest=True
    )

    # ==== 6) Ordenar columnas (opcional, para prolijidad) ====
    ordered_cols = [
        "Transaction ID",
        "Date",
        "Year",
        "Month",
        "MonthName",
        "Customer ID",
        "Gender",
        "Age",
        "Age Band",
        "Product Category",
        "Quantity",
        "Price per Unit",
        "Total Amount",
    ]

    # Nos aseguramos de no perder columnas extra si las hubiera
    other_cols = [c for c in df.columns if c not in ordered_cols]
    df = df[ordered_cols + other_cols]

    # ==== 7) Ordenar por fecha y Transaction ID (opcional) ====
    df = df.sort_values(["Date", "Transaction ID"]).reset_index(drop=True)

    print(f"[{datetime.now()}] Transformación completada. Filas finales: {len(df)}")
    return df


def save_processed_data(df: pd.DataFrame) -> None:
    """Guarda el dataset procesado en CSV para que lo use Power BI."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"[{datetime.now()}] Dataset limpio guardado en: {OUTPUT_FILE}")


def main():
    print(f"[{datetime.now()}] Iniciando actualización automática de Retail Sales...")
    df_raw = load_raw_data()
    df_clean = transform_data(df_raw)
    save_processed_data(df_clean)
    print(f"[{datetime.now()}] Proceso completado correctamente.")


if __name__ == "__main__":
    main()
