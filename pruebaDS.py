import pdfplumber
import pandas as pd
import os

pdf_dir = "pdfs"
csv_dir = "csvs"
os.makedirs(csv_dir, exist_ok=True)

def hacer_encabezados_unicos(columnas):
    contador = {}
    nuevas = []
    for col in columnas:
        if col in contador:
            contador[col] += 1
            nuevas.append(f"{col}_{contador[col]}")
        else:
            contador[col] = 0
            nuevas.append(col)
    return nuevas

for file in os.listdir(pdf_dir):
    if file.endswith(".pdf"):
        nombre = file.replace(".pdf", "")
        pdf_path = os.path.join(pdf_dir, file)
        print(f"Extrayendo datos de {file}...")

        tablas = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    encabezado = hacer_encabezados_unicos(table[0])  # ← aquí arreglamos duplicados
                    df = pd.DataFrame(table[1:], columns=encabezado)
                    df["departamento"] = nombre
                    tablas.append(df)

        if tablas:
            df_total = pd.concat(tablas, ignore_index=True)
            df_total.to_csv(os.path.join(csv_dir, f"{nombre}.csv"), index=False)
