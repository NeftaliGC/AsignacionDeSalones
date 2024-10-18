const globalState = {
    data: { value: null, type: "object"},
    session_id: { value: null, type: "string" },
    api_uri: { value: "http://127.0.0.1:8000", type: "string"}
};


/**
 * Establece el valor de una variable global en el diccionario de variables globales
 * @param {String} variable - Nombre de la variable global a acceder
 * @param {*} valor - Valor nuevo para la variable global
 */
export function setGlobalVariable(variable, valor) {

    if (variable in globalState) {
        if (typeof valor === globalState[variable].type) {
            globalState[variable].value = valor
        } else {
            throw new Error(`Tipo incorrecto para la variable "${nombre}". Esperado: ${globalState[nombre].type}`)
        }
    } else {
        throw new Error(`La variable "${nombre}" no existe.`);
    }

}


/**
 * Obtiene el valor de una variable global en el diccionario de variables globales
 * @param {String} variable - Nombre de la variable global a acceder
 * @returns 
 */
export function getGlobalVariable(variable) {

    if (variable in globalState) {
        return globalState[variable].value;
    } else {
        throw new Error(`La variable "${variable}" no existe.`);
    }

}