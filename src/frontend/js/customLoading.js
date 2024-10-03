function showCustomLoading() {
    document.getElementById('customLoading').style.display = 'flex';
}

function hideCustomLoading() {
    document.getElementById('customLoading').style.display = 'none';
}

setTimeout(function() {
    // Ocultar la pantalla de carga después de 3 segundos
    hideCustomLoading();
    return true;
}, 3000);