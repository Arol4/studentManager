document.addEventListener('DOMContentLoaded', function() {
    const types_modification = document.getElementById('types_modification');
    const modification_par_choix = document.getElementById('modification_par_choix');
    // Sauvegarder le HTML initial IMMÉDIATEMENT
    const modification_par_choix_html_initial = modification_par_choix.innerHTML;
    let types_evaluation, liste_des_matieres_enseignees, notes_de_la_matiere_selectionnee;
    let valeur_type_evaluation, valeur_matiere;
    let valeur_type_evaluation_par_etudiants, valeur_etudiant_id;

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
            modification_par_choix.innerHTML = "";
            const studentArray = Object.entries(window.notesData.etudiants);
            if (studentArray.length == 0) {
                modification_par_choix.textContent = "Aucun étudiant n'est enregistré.";
            } else {
                const listeDesEtudiants = document.createElement('select');
                const  labelListeDesEtudiants = document.createElement('label');
                labelListeDesEtudiants.textContent = "Nom de l'étudiant: ";
                modification_par_choix.appendChild(labelListeDesEtudiants);
                listeDesEtudiants.id = "listeDesEtudiants";
                if (studentArray.length == 1) {
                    studentArray.forEach(([etudiant_id, etudiant]) =>{
                        const optionSurEtudiant = document.createElement('option');
                        optionSurEtudiant.textContent = etudiant.nom;
                        optionSurEtudiant.value = etudiant_id;
                        optionSurEtudiant.selected = true;
                        listeDesEtudiants.appendChild(optionSurEtudiant);
                    });
                }else{
                    const enteteSelection = document.createElement('option');
                    enteteSelection.textContent = "Selectionnez un étudiant";
                    enteteSelection.selected = true;
                    enteteSelection.value = "";
                    enteteSelection.disabled = true;
                    listeDesEtudiants.appendChild(enteteSelection);
                    studentArray.forEach(([etudiant_id, etudiant]) =>{
                        const optionSurEtudiant = document.createElement('option');
                        optionSurEtudiant.textContent = etudiant.nom;
                        optionSurEtudiant.value = etudiant_id;
                        listeDesEtudiants.appendChild(optionSurEtudiant);
                    });                    
                }
                modification_par_choix.appendChild(listeDesEtudiants);
                const returnLine1 = document.createElement('br');
                modification_par_choix.appendChild(returnLine1);
                const labelTypeEvaluation = document.createElement('label');
                labelTypeEvaluation.textContent = "Type d'évaluation :";
                modification_par_choix.appendChild(labelTypeEvaluation);
                const listeTypesEvaluation = document.createElement('select');

                const optionSurCC = document.createElement('option');
                optionSurCC.value = "CC";
                optionSurCC.textContent = "Contrôle Continu (CC)";
                if (window.notesData.role == "enseignant") {
                    listeTypesEvaluation.disabled = true;
                    optionSurCC.selected = true;
                    listeTypesEvaluation.appendChild(optionSurCC);
                }else{
                    const enteteSelectionTypeEvaluation = document.createElement('option');
                    enteteSelectionTypeEvaluation.textContent = "Selectionnez un type d'évaluation";
                    enteteSelectionTypeEvaluation.selected = true;
                    enteteSelectionTypeEvaluation.value = "";
                    enteteSelectionTypeEvaluation.disabled = true;
                    const optionSurSN = document.createElement('option');
                    optionSurSN.value = "SN";
                    optionSurSN.textContent = "Session Normale (SN)";
                    listeTypesEvaluation.appendChild(enteteSelectionTypeEvaluation);
                    listeTypesEvaluation.appendChild(optionSurCC);
                    listeTypesEvaluation.appendChild(optionSurSN);
                }
                modification_par_choix.appendChild(listeTypesEvaluation);
                const notesParEtudiants = document.createElement('div');
                modification_par_choix.appendChild(notesParEtudiants);
                listeDesEtudiants.addEventListener('change', afficherNotesParEtudiants);
                listeTypesEvaluation.addEventListener('change', afficherNotesParEtudiants);
                if (valeur_type_evaluation_par_etudiants) {
                    listeDesEtudiants.value = valeur_etudiant_id;
                }
                if (valeur_etudiant_id) {
                    listeTypesEvaluation.value = valeur_type_evaluation_par_etudiants;
                }
                afficherNotesParEtudiants();
                function afficherNotesParEtudiants(){
                    const etudiant_id = listeDesEtudiants.value;
                    const type_evaluation = listeTypesEvaluation.value;
                    if (etudiant_id && type_evaluation) {
                        const table = creerLeTableauEtudiant(etudiant_id, type_evaluation);
                        notesParEtudiants.innerHTML = "";
                        notesParEtudiants.appendChild(table);
                        const saveButton = document.createElement("button");
                        saveButton.textContent = "Enregistrer les notes";
                        saveButton.addEventListener('click', enregistrerNotesEtudiant);
                        notesParEtudiants.appendChild(saveButton);
                    } else {
                        notesParEtudiants.textContent = "Sélectionnez un étudiant et un type d'évaluation pour afficher ses notes.";
                    }
                    valeur_etudiant_id = etudiant_id;
                    valeur_type_evaluation_par_etudiants = type_evaluation; 
                }
                function enregistrerNotesEtudiant(){
                    const rows = notesParEtudiants.querySelectorAll("tbody tr");
                    notes = {};
                    rows.forEach(row => {
                        const matiere_id = row.getAttribute("matiere-id");
                        const input = row.querySelector("input");
                        const noteValue = parseFloat(input.value);
                        const note = isNaN(noteValue) ? null : noteValue;
                        notes[matiere_id] = note;
                    });
                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                    fetch(window.notesData.urls.enregistrer_notes_etudiant, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({
                            etudiant_id: valeur_etudiant_id,
                            type_evaluation: valeur_type_evaluation_par_etudiants,
                            notes: notes
                        })
                    }).then(response => {
                        if (!response.ok){
                            throw new Error('Erreur réseau');
                        }
                        return response.json();
                    }).then(data => {
                        if (data.message){ 
                            alert(data.message);
                            Object.entries(notes).forEach(([matiere_id, note]) => {
                                ((window.notesData.tableaux[matiere_id][valeur_type_evaluation_par_etudiants]).rows)[valeur_etudiant_id].note = note;
                            });
                        }else{
                            alert("Erreur inconnue");
                        }
                    }).catch(error => {
                        console.error('Erreur:', error);
                        alert('Erreur réseau: '+ error.message);
                    });
                }
            }
        }
    }
    function creerLeTableauEtudiant(etudiant_id, type_evaluation){
        tableauDesMatieres = Object.entries(window.notesData.liste_des_matieres);
        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        const headers = ['Matiere', 'Note'];
        headers.forEach(header => {
            const th = document.createElement('th');
            th.scope = "col";
            th.textContent = header;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
        const tbody = document.createElement("tbody");
        tableauDesMatieres.forEach(([matiere_id, matiere]) =>{
            const tr = document.createElement('tr');
            const th = document.createElement('th');
            const note = (((((window.notesData.tableaux)[matiere_id])[type_evaluation]).rows)[etudiant_id]).note; 
            th.scope = "row";
            tr.setAttribute("matiere-id", parseInt(matiere_id, 10));
            th.textContent = matiere.libelle;
            tr.appendChild(th);
            const td = document.createElement("td");
            const input = document.createElement("input");
            input.type = "number";
            input.value = note !== null ? note:'';
            input.max = 20;
            input.min = 0;
            input.step = 0.5;
            td.appendChild(input);
            tr.appendChild(td);
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);
        return table;
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
            
            const thNom = document.createElement('th');
            thNom.scope = "row";
            thNom.textContent = rowData.nom;
            row.appendChild(thNom);
        
            const tdNote = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.value = rowData.note !== null ? rowData.note : '';
            input.min = 0;
            input.max = 20;
            input.step = 0.5;
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
        .then(async response => {
            const data = await response.json();
            if (!response.ok) {
                const errorMessage = data.error || 'Erreur réseau';
                throw new Error(errorMessage);
            }
            return data;
        })
        .then(data => {
            alert(data.message);
            Object.entries(notes).forEach(([id, note]) =>
            {
                ((((window.notesData).tableaux[matiere_selectionnee][type_evaluation]).rows)[id]).note = note; 
            });
        })
        .catch(error => {
            console.error("Détails de l'erreur :", error);
            alert('Erreur : ' + error.message);
        });
    }
});