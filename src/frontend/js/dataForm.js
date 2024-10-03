document.getElementById('file').addEventListener('change', handleFile, false);

function handleFile(event) {
    console.log('Evento de cambio de archivo');
    const file = event.target.files[0];  // Obtén el archivo seleccionado
    if (!file) {
        console.log('No se seleccionó ningún archivo');
        return;
    }
    console.log('Archivo seleccionado:', file);
    showCustomLoading();
    const reader = new FileReader();

    reader.onload = function (e) {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });

        // primera hoja del Excel
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];

        // Convertimos la hoja de Excel a una matriz de datos
        const sheetData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 });

        // Aplicar la lógica para obtener id, DISP, GS
        const dataDict = getData(sheetData);

        // Mostrar el JSON en la consola
        console.log(dataDict);
    };

    // Lee el archivo como array buffer
    reader.readAsArrayBuffer(file);
}

function getData(sheetData) {
    // Asumiendo que el archivo tiene el mismo formato que en el script Python
    const POSITION = 8;

    // Extraer el id desde la fila 1, columna 0
    const id = sheetData[1][0];

    // Extraer las dimensiones de DISP y GS desde la fila 4, columna 0
    const n = sheetData[4][0];

    // Extraer DISP (desde la fila 8 hasta 8 + n, columnas 0 a 6)
    const DISP = sheetData.slice(POSITION, POSITION + n).map(row => row.slice(0, 6));

    // Extraer GS (desde la fila 8 + n + 3 hasta 8 + n + n + 3, columnas 0 a 3)
    const GS = sheetData.slice(POSITION + n + 3, POSITION + n + n + 3).map(row => row.slice(0, 3));

    // Crear el objeto con los datos
    const dataDict = {
        "id": id,
        "DISP": {
            "shape": [n, 6],
            "data": DISP
        },
        "GS": {
            "shape": [n, 3],
            "data": GS
        }
    };

    
    insertInfo('Datos extraídos correctamente', JSON.stringify(dataDict, null, 2));
    toggleDetailsVisibility();
    setTimeout(hideCustomLoading, 3000); // Ocultar la pantalla de carga después de 3 segundos
    return dataDict;
}
