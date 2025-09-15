document.addEventListener('DOMContentLoaded', function() {
    const types_evaluation = document.getElementById('types_evaluation');
    const liste_des_matieres_enseignees = document.getElementById('liste_des_matieres_enseignees');
    const notes_de_la_matiere_selectionnee = document.getElementById('notes_de_la_matiere_selectionnee');
    afficherNotes();   
    liste_des_matieres_enseignees.addEventListener('change', afficherNotes);
    types_evaluation.addEventListener('change', afficherNotes);

    function creerTableauHTML(data) {
        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        
        data.headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            headerRow.appendChild(th);
        });
        
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        const tbody = document.createElement('tbody');
        data.rows.forEach(rowData => {
            const row = document.createElement('tr');
            row.setAttribute('data-id', rowData.id);
            
            const tdNom = document.createElement('td');
            tdNom.textContent = rowData.nom;
            row.appendChild(tdNom);
        
            const tdNote = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.value = rowData.note;
            input.min = 0;
            input.max = 20;
            input.step = 0.5;
            input.style.width = '50px';
            tdNote.appendChild(input);
            row.appendChild(tdNote);
            
            tbody.appendChild(row);
        });
        
        table.appendChild(tbody);
        return table;
    }
    function afficherNotes(){
        const type_evaluation = types_evaluation.value;
        const matiere_selectionnee = liste_des_matieres_enseignees.value;
        notes_de_la_matiere_selectionnee.innerHTML = '';
        if (matiere_selectionnee && type_evaluation && (window.notesData.tableaux[matiere_selectionnee])[type_evaluation]) {
            const tableau = creerTableauHTML((window.notesData.tableaux[matiere_selectionnee])[type_evaluation]);
            notes_de_la_matiere_selectionnee.appendChild(tableau);
            const saveButton = document.createElement('button');
            saveButton.textContent = 'Enregistrer les notes';
            saveButton.addEventListener('click', enregistrerNotes);
            notes_de_la_matiere_selectionnee.appendChild(saveButton);
        }else{
            notes_de_la_matiere_selectionnee.textContent="Sélectionnez une matière et un type d'évaluation pour afficher les notes des étudiants";

        }     
    }
    function enregistrerNotes() {
        const matiere_selectionnee = liste_des_matieres_enseignees.value;
        const type_evaluation = types_evaluation.value;
        const rows = notes_de_la_matiere_selectionnee.querySelectorAll('tbody tr');
        
        const notes = {};
        rows.forEach(row => {
            const id = row.getAttribute('data-id');
            const input = row.querySelector('input');
            const note = parseFloat(input.value);
            notes[id] = isNaN(note) ? null : note;
        });
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch(window.notesData.urls.enregistrer_notes, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                matiere_id: matiere_selectionnee,
                type_evaluation: type_evaluation,
                notes: notes 
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur réseau');
            }
            return response.json();
        })
        .then(data => {
            if (data.message) {
                alert(data.message);
            } else {
                alert('Erreur inconnue');
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur réseau : ' + error.message);
        });
    }
});