// script.js
function openTab(evt, tabName) {
    // Ocultar todo el contenido de las pestañas
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remover la clase "active" de todos los enlaces de pestañas
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Mostrar el contenido de la pestaña actual y añadir la clase "active"
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Por defecto, abrir la primera pestaña
document.getElementsByClassName("tablink")[0].click();
