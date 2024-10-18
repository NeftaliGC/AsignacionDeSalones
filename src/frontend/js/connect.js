import { setGlobalVariable, getGlobalVariable } from './global.js';

let inactivityTimer = null; // Variable para almacenar el temporizador

window.addEventListener('load', function() {
    startSession();
    activateListeners();
    startInactivityTimer();
});

// Iniciar el temporizador de inactividad
function startInactivityTimer() {
    inactivityTimer = setTimeout(() => {
        endSession();
    }, 1 * 60 * 1000); // Temporizador de 2 minutos de inactividad
}

function startSession() {
    fetch(`${getGlobalVariable("api_uri")}/start-session/`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Respuesta:', data);
        setGlobalVariable("session_id", data.session_id);
    })
    .catch((error) => {
        console.error('Error:', error);
        console.log('Error al iniciar la sesión');
    });
}

function endSession() {
    fetch(`${getGlobalVariable("api_uri")}/end-session/`, {
        method: 'GET',
        headers: {
            'token': `${getGlobalVariable("session_id")}`,
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('Sesión cerrada automáticamente por inactividad:', data)
        desactivateListeners();
        showCustomAlert("Sesion Terminada", "La sesión ha sido cerrada por inactividad, recargue la pagina para iniciar una sesion nueva")
    })
    .catch(error => console.error('Error al cerrar la sesión:', error));
}

function resetTimer() {
    console.log("timer")
    clearTimeout(inactivityTimer); // Cancela el temporizador anterior
    startInactivityTimer(); // Inicia un nuevo temporizador
}

function desactivateListeners() {
    document.removeEventListener('mousemove', resetTimer)
    document.removeEventListener('keydown', resetTimer)
}

function activateListeners() {
    console.log("listeners activados")
    document.addEventListener('mousemove', resetTimer);
    document.addEventListener('keydown', resetTimer);
}
