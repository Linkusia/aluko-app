document.addEventListener("DOMContentLoaded", () => {
    const typSelect = document.getElementById("typ");
    const previewImg = document.getElementById("oknoPreview");
    const dodajBtn = document.getElementById("dodajBtn");
    const tabelaBody = document.querySelector("#zestawienie tbody");
    const sumaDiv = document.getElementById("sumaWyceny");

    let suma = 0;
    let grupaCounter = 0;

    function aktualizujSume() {
        const vat = suma * 0.23;
        const sumaZVat = suma + vat;

        sumaDiv.innerHTML = `
            <div>Netto: ${suma.toFixed(2)} zł</div>
            <div>VAT 23%: ${vat.toFixed(2)} zł</div>
            <div><strong>Brutto: ${sumaZVat.toFixed(2)} zł</strong></div>
        `;
    }

    function przeliczNumeracje() {
        const wiersze = document.querySelectorAll(".okno-wiersz");
        wiersze.forEach((tr, index) => {
            tr.querySelector("td").textContent = `${index + 1}.`;
        });
    }

    typSelect.addEventListener("change", async () => {
        const selected = typSelect.value;
        const dodatkiBox = document.getElementById("dodatkiBox");

        previewImg.src = `/static/img/${selected}.png`;
        dodatkiBox.innerHTML = "Ładowanie dodatków...";

        const response = await fetch("/get-options", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ typ: selected })
        });

        if (!response.ok) {
            dodatkiBox.innerHTML = "Brak dodatków dla pola stałego.";
            return;
        }

        const dodatki = await response.json();
        dodatkiBox.innerHTML = "";
        dodatki.forEach(d => {
            const label = document.createElement("label");
            label.innerHTML = `
                <input type="checkbox" class="dodatek" data-cena="${d.cena}" value="${d.nazwa}">
                <span class="dodatek-text">${d.nazwa} (${d.cena} zł)</span>
            `;
            dodatkiBox.appendChild(label);
        });
    });

    dodajBtn.addEventListener("click", async () => {
        const typ = typSelect.value;
        const szerokosc = parseInt(document.getElementById("szerokosc").value);
        const wysokosc = parseInt(document.getElementById("wysokosc").value);
        const ilosc = parseInt(document.getElementById("ilosc").value);

        if (!typ || !szerokosc || !wysokosc || !ilosc || ilosc <= 0) {
            alert("Proszę wypełnić wszystkie pola poprawnie.");
            return;
        }

        const response = await fetch("/get-price", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ typ, szerokosc, wysokosc })
        });

        if (!response.ok) {
            const error = await response.text();
            alert(error);
            return;
        }

        const cenaJednostkowa = parseFloat(await response.text());
        const cenaLaczna = cenaJednostkowa * ilosc;

        const kolorTla = grupaCounter % 2 === 0 ? "#ffffff" : "#bfbfbf";
        const grupaId = `grupa-${grupaCounter}`;
        grupaCounter++;

        const numerPorzadkowy = document.querySelectorAll(".okno-wiersz").length + 1;

        const tr = document.createElement("tr");
        tr.classList.add("okno-wiersz");
        tr.innerHTML = `
            <td>${numerPorzadkowy}.</td>
            <td>${typ}</td>
            <td>${szerokosc}</td>
            <td>${wysokosc}</td>
            <td>${ilosc}</td>
            <td>${cenaJednostkowa.toFixed(2)}</td>
            <td>${cenaLaczna.toFixed(2)}</td>
            <td><img src="/static/img/${typ}.png" alt="${typ}" style="height:50px;"></td>
            <td><button class="usunBtn">Usuń</button></td> 
        `;

        tr.dataset.grupa = grupaId;
        tr.style.backgroundColor = kolorTla;
        tr.style.borderBottom = "1px solid #ccc";

        tabelaBody.appendChild(tr);
        suma += cenaLaczna;

        const dodatkiZaznaczone = document.querySelectorAll(".dodatek:checked");

        dodatkiZaznaczone.forEach(d => {
            const cenaJedn = parseFloat(d.dataset.cena);
            const cenaDodatekTotal = cenaJedn * ilosc;

            const dodatekTr = document.createElement("tr");
            dodatekTr.innerHTML = `
                <td></td>
                <td>➕ ${d.value}</td>
                <td>-</td>
                <td>-</td>
                <td>${ilosc}</td>
                <td>${cenaJedn.toFixed(2)}</td>
                <td>${cenaDodatekTotal.toFixed(2)}</td>
                <td colspan="2">Dodatek</td>
            `;
            dodatekTr.style.backgroundColor = kolorTla;
            dodatekTr.dataset.grupa = grupaId;
            tabelaBody.appendChild(dodatekTr);

            suma += cenaDodatekTotal;
        });

        tr.querySelector(".usunBtn").addEventListener("click", () => {
            const rows = tabelaBody.querySelectorAll(`tr[data-grupa='${grupaId}']`);
            let sumaDoOdjecia = cenaLaczna;

            dodatkiZaznaczone.forEach(d => {
                sumaDoOdjecia += parseFloat(d.dataset.cena) * ilosc;
            });

            suma -= sumaDoOdjecia;
            rows.forEach(row => row.remove());
            aktualizujSume();
            przeliczNumeracje();

            const pozostaleWiersze = document.querySelectorAll(".okno-wiersz");
            pozostaleWiersze.forEach((tr, index) => {
                const kolor = index % 2 === 0 ? "#ffffff" : "#bfbfbf";
                tr.style.backgroundColor = kolor;
                const grupa = tr.dataset.grupa;
                const dodatki = document.querySelectorAll(`tr[data-grupa='${grupa}']:not(.okno-wiersz)`);
                dodatki.forEach(d => d.style.backgroundColor = kolor);
            });
        });

        aktualizujSume();
    });

    typSelect.dispatchEvent(new Event("change"));
});
document.getElementById("wyslijOferteBtn").addEventListener("click", async () => {
    const imie = document.getElementById("imie").value;
    const nazwisko = document.getElementById("nazwisko").value;
    const email = document.getElementById("email").value;
    const typ = document.getElementById("typ").value;

    const szerokosc = document.getElementById("szerokosc").value;
    const wysokosc = document.getElementById("wysokosc").value;

    const dodatki = [];
    document.querySelectorAll(".dodatek-checkbox:checked").forEach(el => {
        const label = el.closest("label");
        const cena = label.dataset.cena;
        dodatki.push({ nazwa: el.value, cena });
    });

    const podsumowanie = document.getElementById("sumaWyceny").innerText;
    const rows = document.querySelectorAll("#zestawienie tbody tr");
    const pozycje = [];
    let currentPozycja = null;
    
    rows.forEach(row => {
        const cells = row.querySelectorAll("td");
        const isDodatek = cells[1].textContent.includes("➕");
    
        if (!isDodatek) {
            // nowa główna pozycja
            currentPozycja = {
                typ: cells[1].textContent.trim(),
                szerokosc: cells[2].textContent.trim(),
                wysokosc: cells[3].textContent.trim(),
                ilosc: parseInt(cells[4].textContent.trim()),
                cenaJednostkowa: parseFloat(cells[5].textContent.trim()),
                cenaLaczna: parseFloat(cells[6].textContent.trim()),
                dodatki: []
            };
            pozycje.push(currentPozycja);
        } else if (currentPozycja) {
            // dodatek podpięty do ostatniej pozycji
            currentPozycja.dodatki.push({
                nazwa: cells[1].textContent.replace("➕", "").trim(),
                cenaJednostkowa: parseFloat(cells[5].textContent.trim()),
                cenaLaczna: parseFloat(cells[6].textContent.trim())
            });
        }
    });
    const response = await fetch("/send-offer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            imie, nazwisko, email,
            pozycje,
            podsumowanie,
        })
    });
    const mailStatus = document.getElementById("mailStatus");

    if (response.ok) {
        mailStatus.textContent = "📨 Oferta została wysłana!";
    } else {
        const error = await response.text();
        mailStatus.textContent = "❌ Błąd: " + error;
    }
});