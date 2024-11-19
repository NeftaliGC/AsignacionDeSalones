import { getGlobalVariable } from "./global.js";


// Seleccionar las tablas en el documento HTML
const dispDia = document.getElementById("disp-dia");
const gsDia = document.getElementById("gs-dia");
const dispHr = document.getElementById("disp-hr");
const nomod = document.getElementById("nomod");
const nomgru = document.getElementById("nomgru");

// Función para llenar la tabla de Disponibilidad por Día
export function fillDispDiaTable() {

    let data = getGlobalVariable("data");

    nomod.innerHTML += data["nombre"];
    nomgru.innerHTML += data["data"]["Disponibilidad Dias"]["DISP"]["shape"][0];
    
    const dispData = data["data"]["Disponibilidad Dias"]["DISP"].data;
    
    // Limpiar el contenido de la tabla antes de llenarla
    dispDia.querySelector("tbody").innerHTML = "";
    
    // Iterar sobre los datos y crear filas
    dispData.forEach((row, rowIndex) => {
        const newRow = document.createElement("tr");
        
        // Crear la primera celda de la fila (Grupo) y agregarla
        const groupCell = document.createElement("td");
        groupCell.textContent = `Grupo ${rowIndex + 1}`;
        newRow.appendChild(groupCell);
        
        // Llenar las celdas con los valores de cada día
        row.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            newRow.appendChild(cell);
        });
        
        // Agregar la nueva fila a la tabla
        dispDia.querySelector("tbody").appendChild(newRow);
    });
}

// Función para llenar la tabla de Disponibilidad GS
export function fillGsDiaTable() {
    let data = getGlobalVariable("data");
    const gsData = data["data"]["Disponibilidad Dias"]["GS"].data;
    
    // Limpiar el contenido de la tabla antes de llenarla
    gsDia.querySelector("tbody").innerHTML = "";
    
    // Iterar sobre los datos y crear filas
    gsData.forEach((row, rowIndex) => {
        const newRow = document.createElement("tr");
        
        // Crear la primera celda de la fila (Grupo/Sesión) y agregarla
        const groupCell = document.createElement("td");
        groupCell.textContent = `Grupo ${rowIndex + 1}`;
        newRow.appendChild(groupCell);
        
        // Llenar las celdas con los valores de cada clase por semana
        row.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            newRow.appendChild(cell);
        });
        
        // Agregar la nueva fila a la tabla
        gsDia.querySelector("tbody").appendChild(newRow);
    });
}

// Función para llenar la tabla de Disponibilidad por Horario
export function fillDispHrTable() {
    let data = getGlobalVariable("data");
    const dispHrData = data["data"]["Disponibilidad Horario"]["DISP"].data;
    
    // Limpiar el contenido de la tabla antes de llenarla
    dispHr.querySelector("tbody").innerHTML = "";
    
    // Iterar sobre los datos y crear filas
    dispHrData.forEach((row, rowIndex) => {
        const newRow = document.createElement("tr");
        
        // Crear la primera celda de la fila (Grupo) y agregarla
        const groupCell = document.createElement("td");
        groupCell.textContent = `Grupo ${rowIndex + 1}`;
        newRow.appendChild(groupCell);
        
        // Llenar las celdas con los valores de cada horario
        row.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            newRow.appendChild(cell);
        });
        
        // Agregar la nueva fila a la tabla
        dispHr.querySelector("tbody").appendChild(newRow);
    });
}

export function fillTitles() {
    let data = getGlobalVariable("data");

    // Llenar los títulos de las tablas
    
}