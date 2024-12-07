async function fetchCompteur() {
    const response = await fetch('/api/compteur');
    const data = await response.json();
    document.getElementById('compteur').innerText = `Montant actuel : ${data.compteur} €`;
}

async function ajouterDepense() {
    const montant = document.getElementById('montant').value;
    const libelle = document.getElementById('libelle').value;
    await fetch('/api/ajouter_depense', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ montant, libelle })
    });
    reload();
}

async function recupererDernieresDepenses(nbDepenses) {
    const response = await fetch('/api/depenses?limit=' + nbDepenses, {
        method: 'GET'
    });
    const data = await response.json();
    const table = document.getElementById('depenses').getElementsByTagName('tbody')[0];

    table.innerHTML = '';

    data.depenses.forEach(depense => {
        const row = document.createElement("tr");
        table.insertBefore(row, table.firstChild);
        const montant = row.insertCell(0);
        const libelle = row.insertCell(1);
        montant.innerHTML = depense[1];
        libelle.innerHTML = depense[2];
    })
}

async function definirMontant() {
    const montant = document.getElementById('montant_def').value;
    await fetch('/api/definir_montant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ montant })
    });
    reload();
}

reload();

function reload() {
    fetchCompteur();
    recupererDernieresDepenses(5);
}
