function showCustomAlert(titulo, mensaje) {
    document.getElementById('customAlert').style.display = 'block';
    setMessage(titulo, mensaje);
    document.getElementById('alertOverlay').style.display = 'block';
}

function closeCustomAlert() {
    document.getElementById('customAlert').style.display = 'none';
    document.getElementById('alertOverlay').style.display = 'none';
}

function setMessage(t, m) {
    titulo = document.getElementById('titulo-alert');
    mensaje = document.getElementById('mensaje-alert');

    titulo.innerHTML = t;
    mensaje.innerHTML = m;
}