document.addEventListener("DOMContentLoaded", () => {
    const typSelect = document.getElementById("typ");
    const previewImg = document.getElementById("oknoPreview");
    const dodajBtn = document.getElementById("dodajBtn");
    const tabelaBody = document.querySelector("#zestawienie tbody");
    const sumaDiv = document.getElementById("sumaWyceny");

    let suma = 0;

    typSelect.addEventListener("change", () => {
        const selected = typSelect.value;
        previewImg.src = `/static/img/${selected}.png`;
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
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ typ, szerokosc, wysokosc })
        });

        if (!response.ok) {
            const error = await response.text();
            alert(error);
            return;
        }

        const cenaJednostkowa = parseFloat(await response.text());
        const cenaLaczna = cenaJednostkowa * ilosc;

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${typ}</td>
            <td>${szerokosc}</td>
            <td>${wysokosc}</td>
            <td>${ilosc}</td>
            <td>${cenaJednostkowa.toFixed(2)}</td>
            <td>${cenaLaczna.toFixed(2)}</td>
            <td><img src="/static/img/${typ}.png" alt="${typ}" style="height:50px;"></td>
            <td><button class="usunBtn">Usuń</button></td>
        `;
        tr.style.borderBottom = "1px solid #ccc";
        tr.style.backgroundColor = tabelaBody.children.length % 2 === 0 ? "#f9f9f9" : "#ffffff";

        tr.querySelector(".usunBtn").addEventListener("click", () => {
            suma -= cenaLaczna;
            sumaDiv.innerText = `SUMA: ${suma.toFixed(2)} zł`;
            tr.remove();
        });

        tabelaBody.appendChild(tr);
        suma += cenaLaczna;
        sumaDiv.innerText = `SUMA: ${suma.toFixed(2)} zł`;
    });
});
