from flask import Flask, render_template, request
from fpdf import FPDF
from datetime import datetime
import smtplib
from email.message import EmailMessage
import pandas as pd
import os

app = Flask(__name__)

# === KONFIGURACJA ===
EXCEL_PATH = "WYCENY.xlsx"
FONT_PATH_REGULAR = "DejaVuSans.ttf"
FONT_PATH_BOLD = "DejaVuSans-Bold.ttf"
SMTP_EMAIL = "testlinkusiatest@gmail.com"
SMTP_HASLO = "fwimegwfcxksoaou"
MAIL_WLASCICIELA = "paulina.mrozinska90@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FIRMA_NAZWA = "ALUKO SC"
FIRMA_ADRES = "ul. Fabryczna 10\nWrocław"

# === STRONY ===
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/wycena")
def kalkulator():
    return render_template("index.html")

# === API DO CENY ===
@app.route("/get-price", methods=["POST"])
def get_price():
    data = request.get_json()
    typ = data.get("typ")
    szerokosc = int(data.get("szerokosc"))
    wysokosc = int(data.get("wysokosc"))

    cena = get_price_from_sheet_ceil(EXCEL_PATH, typ, szerokosc, wysokosc)
    if cena is None:
        return "Brak danych do wyceny", 404

    return str(cena)

# === FUNKCJE ===
def get_price_from_sheet_ceil(file_path, sheet_name, width, height):
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)
    width_row = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1, nrows=1)
    width_values = width_row.values[0][3:-2]
    width_columns = df.columns[3:3 + len(width_values)]
    height_values = df.iloc[:, 2].dropna().unique()

    width_candidates = width_values[width_values >= width]
    height_candidates = height_values[height_values >= height]

    if len(width_candidates) == 0 or len(height_candidates) == 0:
        return None

    chosen_width = width_candidates[0]
    chosen_height = height_candidates[0]
    column_idx = list(width_values).index(chosen_width)
    column_name = width_columns[column_idx]

    row = df[df.iloc[:, 2] == chosen_height]
    price = row[column_name].values[0]
    return None if pd.isna(price) else float(price)

# === URUCHOM LOKALNIE ===
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)