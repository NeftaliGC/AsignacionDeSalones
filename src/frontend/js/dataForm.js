import { setGlobalVariable, getGlobalVariable } from "./global.js";
import { fillDispDiaTable, fillGsDiaTable, fillDispHrTable } from "./contentab1.js";

document.getElementById('file').addEventListener('change', handleFile, false);

// dimensiones de DISP y GS
let n = 0;

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


        // Aplicar la lógica para obtener id, DISP, GS
        setGlobalVariable("data", getData(workbook))
        console.log(getGlobalVariable("data"));

        // Llamar a las funciones para llenar las tablas cuando los datos se carguen
        fillDispDiaTable();
        fillGsDiaTable();
        fillDispHrTable();
        
    };

    // Lee el archivo como array buffer
    reader.readAsArrayBuffer(file);
}

function getData(workbook) {

    let allData = null;
    
    // Iterar sobre cada hoja
    workbook.SheetNames.forEach(sheetName => {
        const sheetData = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName], { header: 1 });
        if (sheetName === "Datos Generales") {
            allData = getDataBySheetName(sheetName, sheetData);
        } else {
            allData["data"][sheetName] = getDataBySheetName(sheetName, sheetData);
        }
    });
    
    
    insertInfo("Datos cargados correctamente", "Los datos se han cargado correctamente. Puedes ver los detalles en las pestañas correspondientes.");
    toggleDetailsVisibility();
    setTimeout(hideCustomLoading, 3000); // Ocultar la pantalla de carga después de 3 segundos
    return allData;
}


function getDataBySheetName(sheetName, sheetData) {
    let dataDict;
    
    if (sheetName === "Datos Generales") {
        dataDict = processHoja1(sheetData);
    } else if (sheetName === "Disponibilidad Dias") {
        dataDict = processHoja2(sheetData);
    } else if (sheetName === "Disponibilidad Horario") {
        dataDict = processHoja3(sheetData);
    } else if (sheetName === "Disponibilidad Salones") {
        dataDict = processHoja4(sheetData);
    } else if (sheetName === "Informacion Grupos") {
        dataDict = processHoja5(sheetData);
    } else {
        console.warn(`No se ha definido un método para procesar la hoja: ${sheetName}`);
        dataDict = {};
    }

    return dataDict;
}

function processHoja1(sheetData) {
    // Lógica para procesar la hoja 1

    // Extraer el nombre desde la fila 1, columna 0
    const nombre = sheetData[1][0];

    // Extraer la dimensión de las matrices
    n = sheetData[4][0];

    const dataDict = {
        "nombre": nombre,
        "data": {

        }
    }

    return dataDict;

}

function processHoja2(sheetData) {
    // Lógica para procesar la hoja 2
    
    // Extraer DISP (desde la fila 1 hasta 1 + n, columnas 0 a 6)
    const DISP = sheetData.slice(2, 2 + n).map(row => row.slice(0, 6));
    
    // Extraer GS (desde la fila 1 + n + 3 hasta 1 + n + n + 3, columnas 0 a 3)
    const GS = sheetData.slice(2 + n + 3, 2 + n + n + 3).map(row => row.slice(0, 3));
    
    // Crear el objeto con los datos
    const dataDict =
        {
            "DISP": {
                "shape": [n, 6],
                "data": DISP
            },
            "GS": {
                "shape": [n, 3],
                "data": GS
            }
        }
    ;
    
    return dataDict;
    
}

function processHoja3(sheetData) {
    // Lógica para procesar la hoja 3

    const DISP = sheetData.slice(2, 2 + n).map(row => row.slice(0, 6));

    const dataDict = {
        "DISP": {
            "shape": [n, 6],
            "data": DISP
        }
    }

    return dataDict;
}

function processHoja4(sheetData) {
    // Lógica para procesar la hoja 4

    const dataDict = {

    }

    return dataDict;
}

function processHoja5(sheetData) {
    // Lógica para procesar la hoja 4

    const dataDict = {

    }

    return dataDict;
}