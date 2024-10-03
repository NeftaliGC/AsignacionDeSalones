const form = document.getElementById('uploadfile');

form.addEventListener('submit', function(event) {
    event.preventDefault(); // Esto evita que el formulario se envíe de la manera tradicional
    event.stopPropagation(); // Esto evita que el evento se propague por el DOM
    console.log('evento detenido');
    // Aquí pondrías el código para enviar los datos del formulario mediante fetch API o XMLHttpRequest
    uploadFile(form);
});

function uploadFile(form) {
    const formData = new FormData(form);
    fetch('http://127.0.0.1:8000/uploadfile/', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(result => {
        console.log(result);
        alert('Archivo subido con éxito: ' + result.filename);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al subir el archivo: ' + error.message);
    });
}
