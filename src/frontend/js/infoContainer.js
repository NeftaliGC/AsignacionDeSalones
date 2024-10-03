function insertInfo(message, detailsContent) {
    // Mostrar el contenedor de información
    document.getElementById('info').style.display = 'block';

    // Insertar el mensaje de información
    document.getElementById('message-info').textContent = message;

    // Insertar los detalles
    document.getElementById('details').innerHTML = detailsContent;

    // Asegurar que el icono esté en su posición inicial
    document.getElementById('toggleDetails').classList.remove('rotated');
}

function toggleDetailsVisibility() {
    const details = document.getElementById('details');
    const icon = document.getElementById('toggleDetails');

    if (details.classList.contains('details-expanded')) {
        // Ocultar los detalles
        details.classList.remove('details-expanded');
        details.classList.add('details-collapsed');
        icon.classList.remove('rotated');
    } else {
        // Mostrar los detalles
        details.classList.remove('details-collapsed');
        details.classList.add('details-expanded');
        icon.classList.add('rotated');
    }
}
