document.addEventListener('DOMContentLoaded', () => {
    const note_elements = document.querySelectorAll('.note');
    note_elements.forEach((note_element) => {
        let content = note_element.textContent.trim();
        let note = (content === "")? NaN:Number(content);
        if (Number.isNaN(note)){
            if(content === "VA"){
                note_element.classList.add("bonne_note");
            }else{
                if(content === "NV"){
                    note_element.classList.add("mauvaise_note");
                }else{
                    note_element.classList.add("aucune_note");
                }
            }
        }else{
            if (note >= 10) {
                note_element.classList.add("bonne_note");
            } else {
                note_element.classList.add("mauvaise_note");
            }
        }
    });
})