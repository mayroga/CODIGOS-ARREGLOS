document.getElementById('btnCrear').addEventListener('click', () => lanzarProceso('/crear_app'));
document.getElementById('btnRevisar').addEventListener('click', () => lanzarProceso('/revisar_app'));
document.getElementById('btnCorregir').addEventListener('click', () => lanzarProceso('/corregir_app'));

// BOTÓN DE DESTRUCCIÓN DE DATOS LOCAL
document.getElementById('btnBorrarTodo').addEventListener('click', () => {
    document.getElementById('appDescripcion').value = "";
    document.getElementById('sugerenciasPanel').innerText = "Las guías maestras y las explicaciones completas de tus códigos empaquetados aparecerán aquí...";
    for (let i = 1; i <= 5; i++) {
        document.getElementById(`code${i}`).value = "";
    }
    window.gc && window.gc(); // Forzar recolección de basura si el dispositivo lo admite
});

async function lanzarProceso(endpoint) {
    const desc = document.getElementById('appDescripcion').value;
    const btnCrear = document.getElementById('btnCrear');
    const btnRevisar = document.getElementById('btnRevisar');
    const btnCorregir = document.getElementById('btnCorregir');

    if (!desc.trim() && endpoint === '/crear_app') {
        return alert("Por favor, introduce la descripción técnica del sistema que deseas crear.");
    }

    [btnCrear, btnRevisar, btnCorregir].forEach(b => b.disabled = true);
    document.getElementById('sugerenciasPanel').innerText = "Abriendo hilos de procesamiento síncrono. Sincronizando dependencias cruzadas...";

    try {
        // Recopilamos nombres y contenidos dinámicos del formulario
        const payload = { descripcion: desc };
        for (let i = 1; i <= 5; i++) {
            payload[`nombre${i}`] = document.getElementById(`name${i}`).value;
            payload[`codigo${i}`] = document.getElementById(`code${i}`).value;
        }

        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let streamAcumulado = "";

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            streamAcumulado += decoder.decode(value, { stream: true });
            procesarStreamMultiArchivo(streamAcumulado);
        }
    } catch (error) {
        alert("La conexión con el motor de procesamiento local se vio interrumpida.");
    } finally {
        [btnCrear, btnRevisar, btnCorregir].forEach(b => b.disabled = false);
    }
}

// Algoritmo de extracción estricta basado en bloques abiertos :::INICIO::: y :::FIN:::
function procesarStreamMultiArchivo(texto) {
    // 1. Procesar Sugerencias / Explicación del Maestro
    const inicioSuj = texto.indexOf(":::INICIO_SUGERENCIAS:::");
    const finSuj = texto.indexOf(":::FIN_SUGERENCIAS:::");
    if (inicioSuj !== -1) {
        const corteFin = (finSuj !== -1) ? finSuj : texto.length;
        document.getElementById('sugerenciasPanel').innerText = texto.substring(inicioSuj + 24, corteFin).trim();
    }

    // 2. Procesar los hasta 5 archivos dinámicos de forma secuencial
    let posicionActual = 0;
    let contadorPaneles = 1;

    while (texto.indexOf(":::INICIO_ARCHIVO:::", posicionActual) !== -1 && contadorPaneles <= 5) {
        const inicioM = texto.indexOf(":::INICIO_ARCHIVO:::", posicionActual);
        const saltoLinea = texto.indexOf("\n", inicioM);
        const finM = texto.indexOf(":::FIN_ARCHIVO:::", inicioM);

        if (saltoLinea !== -1 && saltoLinea > inicioM) {
            // Extraer el nombre que propuso la IA para contrastarlo o inyectarlo
            const encabezado = texto.substring(inicioM + 20, saltoLinea).trim();
            const finBloque = (finM !== -1) ? finM : texto.length;
            const codigoLimpio = texto.substring(saltoLinea + 1, finBloque).trim();

            const inputNombre = document.getElementById(`name${contadorPaneles}`);
            const areaCodigo = document.getElementById(`code${contadorPaneles}`);

            if (areaCodigo) {
                if (encabezado && inputNombre.value.trim() === "") {
                    inputNombre.value = encabezado; // Si el panel estaba vacío, le asignamos el nombre sugerido
                }
                areaCodigo.value = codigoLimpio;
            }
        }
        
        posicionActual = (finM !== -1) ? finM + 17 : texto.length;
        contadorPaneles++;
    }
}
