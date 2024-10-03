const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('file');
const fileNameDisplay = document.getElementById('file-name');
const allowedExtension = '.xlsx'; // Extensión permitida

// Prevenir el comportamiento por defecto para arrastrar y soltar
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Estilos cuando se arrastra el archivo sobre la zona
['dragenter', 'dragover'].forEach(eventName => {
    uploadZone.classList.add('dragging');
});

['dragleave', 'drop'].forEach(eventName => {
    uploadZone.classList.remove('dragging');
});

// Manejar la subida del archivo arrastrado
uploadZone.addEventListener('drop', handleDrop);

function handleDrop(e) {
    const files = e.dataTransfer.files;
    if (files.length) {
        const file = files[0];
        if (validateFileExtension(file)) {
            // Asignar los archivos al input
            fileInput.files = files;

            // Forzar el evento 'change' para que se ejecute el mismo código que al seleccionar manualmente
            const event = new Event('change');
            fileInput.dispatchEvent(event);

        } else {
            let titulo = "¡Operación Invalida!";
            let mensaje = "Solo se aceptan archivos .xlsx";
            showCustomAlert(titulo, mensaje);
        }
    }
}

// Si se selecciona el archivo manualmente
fileInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        if (validateFileExtension(file)) {
            updateFileNameDisplay(file); // Mostrar el nombre del archivo
        } else {
            let titulo = "¡Operación Invalida!";
            let mensaje = "Solo se aceptan archivos .xlsx";
            showCustomAlert(titulo, mensaje);
            fileInput.value = ''; // Limpiar el input si el archivo no es válido
        }
    }
});

// Función para validar la extensión del archivo
function validateFileExtension(file) {
    const fileName = file.name;
    return fileName.endsWith(allowedExtension); // Verifica si el archivo tiene la extensión .xlsx
}

// Función para actualizar el nombre del archivo en la interfaz
function updateFileNameDisplay(file) {
    fileNameDisplay.textContent = `Archivo seleccionado: ${file.name}`;
}
