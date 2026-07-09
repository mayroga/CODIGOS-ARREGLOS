// Asignación de eventos a los botones guiados
document.getElementById('btnCrear').addEventListener('click', () => procesarOperacion('/crear_app'));
document.getElementById('btnRevisar').addEventListener('click', () => procesarOperacion('/revisar_app'));
document.getElementById('btnCorregir').addEventListener('click', () => procesarOperacion('/corregir_app'));

// BOTÓN DE BORRADO ABSOLUTO (Limpia toda la RAM local al instante)
document.getElementById('btnBorrarTodo').addEventListener('click', () => {
    document.getElementById('appDescripcion').value = "";
    document.getElementById('code1').value = "";
    document.getElementById('code2').value = "";
    document.getElementById('code3').value = "";
    document.getElementById('sugerenciasPanel').innerText = "El Maestro de Codificación te guiará aquí paso a paso...";
    // Sugerimos al navegador liberar los hilos de memoria asignados
    window.gc && window.gc();
});

// Función unificada que maneja el Streaming en tiempo real para evitar congelamientos
async function procesarOperacion(endpoint) {
    const desc = document.getElementById('appDescripcion').value;
    const btnCrear = document.getElementById('btnCrear');
    const btnRevisar = document.getElementById('btnRevisar');
    const btnCorregir = document.getElementById('btnCorregir');

    if (!desc.trim() && endpoint === '/crear_app') {
        return alert("Por favor, describe la aplicación que deseas crear en la caja superior.");
    }

    // Bloqueamos los botones durante la ejecución para proteger el canal de datos
    [btnCrear, btnRevisar, btnCorregir].forEach(b => b.disabled = true);
    document.getElementById('sugerenciasPanel').innerText = "Estableciendo conexión segura con el motor de IA en tiempo real...";

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                descripcion: desc,
                codigo1: document.getElementById('code1').value,
                codigo2: document.getElementById('code2').value,
                codigo3: document.getElementById('code3').value
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let acumuladorText = "";

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            acumuladorText += decoder.decode(value, { stream: true });
            
            // Procesa y distribuye dinámicamente el texto en las cajas correspondientes
            inyectarTextoEnPanelesStrict(acumuladorText);
        }
    } catch (error) {
        alert("La transmisión se interrumpió. Verifica tu conexión a internet.");
    } finally {
        // Desbloqueamos los botones al terminar
        [btnCrear, btnRevisar, btnCorregir].forEach(b => b.disabled = false);
    }
}

// Algoritmo de separación estricto para evitar cortes de cable visuales
function inyectarTextoEnPanelesStrict(texto) {
    const marcas = {
        '===ARCHIVO1===': 'code1',
        '===ARCHIVO2===': 'code2',
        '===ARCHIVO3===': 'code3',
        '===SUGERENCIAS===': 'sugerenciasPanel'
    };

    const llaves = Object.keys(marcas);
    
    for (let i = 0; i < llaves.length; i++) {
        const marcaActual = llaves[i];
        const idElemento = marcas[marcaActual];
        const indexInicio = texto.indexOf(marcaActual);
        
        if (indexInicio !== -1) {
            let indexFin = texto.length;
            
            for (let j = 0; j < llaves.length; j++) {
                const otraMarca = llaves[j];
                const indexOtra = texto.indexOf(otraMarca);
                if (indexOtra !== -1 && indexOtra > indexInicio && indexOtra < indexFin) {
                    indexFin = indexOtra;
                }
            }
            
            const contenidoLimpio = texto.substring(indexInicio + marcaActual.length, indexFin).trim();
            const elemento = document.getElementById(idElemento);
            
            if (elemento) {
                if (idElemento === 'sugerenciasPanel') {
                    elemento.innerText = contenidoLimpio;
                } else {
                    elemento.value = contenidoLimpio;
                }
            }
        }
    }
}
