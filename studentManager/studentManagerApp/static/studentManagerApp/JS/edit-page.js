document.addEventListener('DOMContentLoaded', function() {
    const types_modification = document.getElementById('types_modification');
    const modification_par_choix = document.getElementById('modification_par_choix');
    // Sauvegarder le HTML initial IMMÉDIATEMENT
    const modification_par_choix_html_initial = modification_par_choix.innerHTML;
    let types_evaluation, liste_des_matieres_enseignees, notes_de_la_matiere_selectionnee;
    let valeur_type_evaluation, valeur_matiere;

    // Fonction pour réinitialiser les références aux éléments
    function initialiserReferences() {
        types_evaluation = document.getElementById('types_evaluation');
        liste_des_matieres_enseignees = document.getElementById('liste_des_matieres_enseignees');
        notes_de_la_matiere_selectionnee = document.getElementById('notes_de_la_matiere_selectionnee');
        
        // Réattacher les écouteurs d'événements
        if (liste_des_matieres_enseignees) {
            liste_des_matieres_enseignees.addEventListener('change', afficherNotes);
        }
        if (types_evaluation) {
            types_evaluation.addEventListener('change', afficherNotes);
        }

        if (valeur_matiere){
            liste_des_matieres_enseignees.value = valeur_matiere;
        }
        if (valeur_type_evaluation) {
            types_evaluation.value = valeur_type_evaluation;
        }
    }

    // Initialiser les références au chargement
    initialiserReferences();
    afficherNotes();

    types_modification.addEventListener('change', afficherModifications);

    function afficherModifications() {
        const type_modification = types_modification.value;
        if (type_modification == "par_matiere") {
            // Restaurer le HTML initial
            modification_par_choix.innerHTML = modification_par_choix_html_initial;
            // Réinitialiser les références aux nouveaux éléments
            initialiserReferences();
            // Réafficher les notes
            afficherNotes();
        } else if (type_modification == "par_etudiant") {
            modification_par_choix.innerHTML = "Le menu de la modification par étudiant doit s'afficher ici.";
        }
    }

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
        Object.entries(data.rows).forEach(([id, rowData]) => {
            const row = document.createElement('tr');
            row.setAttribute('data-id', parseInt(id, 10));
            
            const tdNom = document.createElement('td');
            tdNom.textContent = rowData.nom;
            row.appendChild(tdNom);
        
            const tdNote = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.value = rowData.note !== null ? rowData.note : '';
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
        
        if (matiere_selectionnee && type_evaluation && window.notesData.tableaux[matiere_selectionnee] && window.notesData.tableaux[matiere_selectionnee][type_evaluation]) {
            const tableau = creerTableauHTML(window.notesData.tableaux[matiere_selectionnee][type_evaluation]);
            notes_de_la_matiere_selectionnee.appendChild(tableau);
            const saveButton = document.createElement('button');
            saveButton.textContent = 'Enregistrer les notes';
            saveButton.addEventListener('click', enregistrerNotes);
            notes_de_la_matiere_selectionnee.appendChild(saveButton);
        } else {
            notes_de_la_matiere_selectionnee.textContent = "Sélectionnez une matière et un type d'évaluation pour afficher les notes des étudiants";
        }
        valeur_type_evaluation = type_evaluation;
        valeur_matiere = matiere_selectionnee;
    }
    function enregistrerNotes() {
        const matiere_selectionnee = liste_des_matieres_enseignees.value;
        const type_evaluation = types_evaluation.value;
        const rows = notes_de_la_matiere_selectionnee.querySelectorAll('tbody tr');
        
        const notes = {};
        rows.forEach(row => {
            const id = row.getAttribute('data-id');
            const input = row.querySelector('input');
            const noteValue = input.value.trim();
            const note = noteValue === '' ? null : parseFloat(noteValue);
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
                Object.entries(notes).forEach(([id, note]) =>
                {
                    ((((window.notesData).tableaux[matiere_selectionnee][type_evaluation]).rows)[id]).note = note; 
                });
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