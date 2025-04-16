from fpdf import FPDF
from datetime import datetime
import os

FONT_PATH_REGULAR = "DejaVuSans.ttf"
FONT_PATH_BOLD = "DejaVuSans-Bold.ttf"
LOGO_PATH = "static/img/ALUKO.jpg"

class PDF(FPDF):
    def header(self):
        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, x=160, y=10, w=40)
        self.set_font("DejaVu", 'B', 14)
        self.cell(0, 10, "OFERTA - ALUKO SC", ln=True, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.cell(0, 10, f"Strona {self.page_no()}", 0, 0, "C")

def generate_offer_pdf(data, output_path=None):
    pdf = PDF()

    pdf.add_font("DejaVu", "", FONT_PATH_REGULAR, uni=True)
    pdf.add_font("DejaVu", "B", FONT_PATH_BOLD, uni=True)
    pdf.add_page()
    pdf.set_font("DejaVu", size=12)

    pdf.ln(5)
    pdf.set_font("DejaVu", size=10)
    pdf.cell(0, 10, f"Data oferty: {datetime.today().strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(0, 10, f"Oferta dla: {data['imie']} {data['nazwisko']}", ln=True)
    pdf.cell(0, 10, f"Email: {data['email']}", ln=True)
    pdf.ln(10)

    total_width = pdf.w - 2 * pdf.l_margin
    col_widths = {
        "#": 7,
        "typ": 84,
        "szer": 16,
        "wys": 16,
        "ilosc": 13,
        "cena_jedn": 26,
        "cena_laczna": total_width - (7 + 78 + 16 + 16 + 13 + 26)
    }

    pdf.set_font("DejaVu", "B", 11)
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(col_widths["#"], 10, "#", 1, 0, 'C', True)
    pdf.cell(col_widths["typ"], 10, "Typ", 1, 0, 'C', True)
    pdf.cell(col_widths["szer"], 10, "Szer.", 1, 0, 'C', True)
    pdf.cell(col_widths["wys"], 10, "Wys.", 1, 0, 'C', True)
    pdf.cell(col_widths["ilosc"], 10, "Ilość", 1, 0, 'C', True)
    pdf.cell(col_widths["cena_jedn"], 10, "Cena jedn.", 1, 0, 'C', True)
    pdf.cell(col_widths["cena_laczna"], 10, "Cena łączna", 1, 1, 'C', True)

    pdf.set_font("DejaVu", size=10)

    for idx, poz in enumerate(data['pozycje'], 1):
        row_height = 11
        pdf.cell(col_widths["#"], row_height, str(idx), border=1, ln=0, align='C')
        pdf.cell(col_widths["typ"], row_height, poz['typ'], border=1, ln=0, align='L')
        pdf.cell(col_widths["szer"], row_height, poz['szerokosc'], border=1, ln=0, align='C')
        pdf.cell(col_widths["wys"], row_height, poz['wysokosc'], border=1, ln=0, align='C')
        pdf.cell(col_widths["ilosc"], row_height, str(poz['ilosc']), border=1, ln=0, align='C')
        pdf.cell(col_widths["cena_jedn"], row_height, f"{poz['cenaJednostkowa']:.2f} zł", border=1, ln=0, align='R')
        pdf.cell(col_widths["cena_laczna"], row_height, f"{poz['cenaLaczna']:.2f} zł", border=1, ln=1, align='R')


        for d in poz['dodatki']:
            pdf.cell(col_widths["#"], row_height, "", border=1, ln=0, align='C')
            pdf.cell(col_widths["typ"], row_height, f"{d['nazwa']}", border=1, ln=0, align='L')
            pdf.cell(col_widths["szer"], row_height, "", border=1, ln=0, align='C')
            pdf.cell(col_widths["wys"], row_height, "", border=1, ln=0, align='C')
            pdf.cell(col_widths["ilosc"], row_height, str(poz['ilosc']), border=1, ln=0, align='C')
            pdf.cell(col_widths["cena_jedn"], row_height, f"{d['cenaJednostkowa']:.2f} zł", border=1, ln=0, align='R')
            pdf.cell(col_widths["cena_laczna"], row_height, f"{d['cenaLaczna']:.2f} zł", border=1, ln=1, align='R')

    pdf.ln(5)
    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(0, 10, "Podsumowanie:", ln=True)
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 10, data['podsumowanie'])

    if output_path is None:
        filename = f"oferta_{data['imie'].lower()}_{datetime.today().strftime('%Y%m%d')}.pdf"
        output_path = os.path.join(os.getcwd(), filename)

    pdf.output(output_path)
    return output_path
