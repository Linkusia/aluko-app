from flask import Flask, render_template, request, jsonify
from fpdf import FPDF
from datetime import datetime
import smtplib
from email.message import EmailMessage
import pandas as pd
import os
from pdf_generator import generate_offer_pdf

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
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/en')
def home_en():
    return render_template('home_en.html')

@app.route('/de')
def home_de():
    return render_template('home_de.html')

@app.route('/wycena')
def kalkulator():
    return render_template('index.html')

# === API DO CENY ===
@app.route("/get-price", methods=["POST"])
def get_price():
    data = request.get_json()
    typ = data.get("typ")
    szerokosc = int(data.get("szerokosc"))
    wysokosc = int(data.get("wysokosc"))

    cena = get_price_from_sheet_ceil(EXCEL_PATH, typ, szerokosc, wysokosc)

    if isinstance(cena, str):
        return cena, 400

    if cena is None:
        return "Twoje okno jest za duże, skontaktuj się po indywidualną wycenę", 404

    return str(cena)

# === API DO DODATKÓW ===
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
# === API DO WYSYŁKI PDF ===
@app.route("/send-offer", methods=["POST"])
def send_offer():
    data = request.get_json()

    try:
        pdf_path = generate_offer_pdf(data, output_path="oferta_temp.pdf")

        # przygotuj maila
        msg = EmailMessage()
        msg["Subject"] = "Twoja oferta od ALUKO SC"
        msg["From"] = SMTP_EMAIL
        msg["To"] = data['email']
        msg.set_content(f"Cześć {data['imie']},\n\nW załączeniu znajdziesz ofertę przygotowaną na podstawie Twoich danych.\n\nPozdrawiamy!\nZespół ALUKO SC")

        with open(pdf_path, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename="Oferta_ALUKO.pdf")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_HASLO)
            server.send_message(msg)

        return "Oferta wysłana!", 200

    except Exception as e:
        print("Błąd przy wysyłce oferty:", e)
        return "Błąd przy wysyłce oferty.", 500
# === FUNKCJA CENOWA ===
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
        return "Grześ powiedział, że złe proporcje."

    return float(price)

# === URUCHOMIENIE APLIKACJI ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)