from flask import Flask, render_template, request, jsonify
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

    if isinstance(cena, str):
        return cena, 400  # komunikat błędu (np. "poza zakresem")

    if cena is None:
        return "Twoje okno jest za duże, skontaktuj się po indywidualną wycenę", 404

    return str(cena)

# === FUNKCJA WYCIĄGANIA CENY Z EXCELA Z WALIDACJĄ ZAKRESÓW ===
def get_price_from_sheet_ceil(file_path, sheet_name, width, height):
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=2)
    width_row = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1, nrows=1)
    width_values = width_row.values[0][3:-2]
    width_columns = df.columns[3:3 + len(width_values)]
    height_values = df.iloc[:, 2].dropna().unique()

    min_width = int(min(width_values))
    max_width = int(max(width_values))
    min_height = int(min(height_values))
    max_height = int(max(height_values))

    if not (min_width <= width <= max_width) or not (min_height <= height <= max_height):
        return f"Dla wybranego okna \"{sheet_name}\" dostępna szerokość to {min_width}–{max_width} mm, a wysokość {min_height}–{max_height} mm."

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

    if pd.isna(price) or price == "-" or price == "":
        return None

    return float(price)

# === API DO DODATKÓW (CHECKBOXY) ===
@app.route("/get-options", methods=["POST"])
def get_options():
    data = request.get_json()
    typ = data.get("typ")

    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=typ, engine="openpyxl", usecols="A:B", skiprows=29, nrows=4)
        df.columns = ["nazwa", "cena"]
        dodatki = df.to_dict(orient="records")
        return jsonify(dodatki)
    except Exception as e:
        print("Błąd dodatków:", e)
        return jsonify({"error": "Błąd przy pobieraniu dodatków"}), 500

# === URUCHOMIENIE APLIKACJI ===
if __name__ == "__main__":
   import os
   port = int(os.environ.get("PORT", 5000))
   app.run(host="0.0.0.0", port=port)
# === URUCHOM LOKALNIE ===
#if __name__ == "__main__":
#    app.run(debug=True)