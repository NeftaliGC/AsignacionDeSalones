import { setGlobalVariable, getGlobalVariable } from './global.js';

const submitButton = document.getElementById("submitButton");

submitButton.addEventListener("click", function() {
    if (getGlobalVariable("data") === null) {
        showCustomAlert("Error", "No se han cargado un excel con los datos");
        return;
    }

    const data = getGlobalVariable("data");
    console.log(data);

    if (getGlobalVariable("session_id") === null) {
        console.log("No se ha iniciado la sesión");
        return;
    }

    sendData(data);

});

function sendData(data) {
    // Enviar los datos al servidor
    fetch(`${getGlobalVariable("api_uri")}/add-data/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'token': `${getGlobalVariable("session_id")}`
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
        console.log('Error al enviar los datos');
    });

}