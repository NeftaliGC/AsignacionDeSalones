import { getGlobalVariable } from './global.js';

const save = document.getElementById('saveButton');

save.addEventListener('click', function(event) {

    event.preventDefault();
    event.stopPropagation();

    if (getGlobalVariable("data") === null) {
        showCustomAlert("Alerta" , "No se ha cargado ningún archivo");
        return;
    }

    saveData();
    return;

});

function saveData() {
    
    fetch(`${getGlobalVariable("api_uri")}/save-data/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'token': `${getGlobalVariable("session_id")}`
        },
        body: JSON.stringify({ data: " "})
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta:', data);
        showCustomAlert("Información", "La información ha sido guardada")
    })
    .catch((error) => {
        console.error('Error:', error);
        console.log('Error al enviar los datos');
    });

}