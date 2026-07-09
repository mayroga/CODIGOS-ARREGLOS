// Control de Pestañas
document.getElementById('tabExpress').addEventListener('click', () => cambiarPestana('tabExpress', 'moduloExpress'));
document.getElementById('tabAutonomo').addEventListener('click', () => cambiarPestana('tabAutonomo', 'moduloAutonomo'));

function cambiarPestana(tabId, moduloId) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.modulo').forEach(m => m.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    document.getElementById(moduloId).classList.add('active');
}

// BOTONES DE BORRADO SEGURO (Evitan la sobrecarga de datos en la pantalla)
document.getElementById('btnBorrarExpress').addEventListener('click', () => {
    document.getElementById('codigoSucio').value = "";
    document.getElementById('codigoLimpio').value = "";
});

document.getElementById('btnBorrarAutonomo').addEventListener('click', () => {
    document.getElementById('appDescripcion').value = "";
    document.getElementById('code1').value = "";
    document.getElementById('code2').value = "";
    document.getElementById('code3').value = "";
    document.getElementById('sugerenciasPanel').innerText = "Las sugerencias aparecerán aquí tras procesar...";
});

// Lógica de Ejecución Express
document.getElementById('btnCorregir').addEventListener('click', async () => {
    const btn = document.getElementById('btnCorregir');
    const input = document.getElementById('codigoSucio').value;
    if (!input.trim()) return alert("Por favor, ingresa código primero.");
    
    btn.innerText = "Corrigiendo..."; btn.disabled = true;
    try {
        const response = await fetch('/corregir', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ codigo: input })
        });
        const data = await response.json();
        document.getElementById('codigoLimpio').value = data.codigoCorregido || data.error;
    } catch(e) { 
        alert("Error de red al conectar con el servidor."); 
    } finally {
        btn.innerText = "Corregir Código"; btn.disabled = false;
    }
});

// Lógica de Ingeniería Avanzada (Procesamiento por Fragmentos / Streaming)
document.getElementById('btnConstruir').addEventListener('click', async () => {
    const btn = document.getElementById('btnConstruir');
    const desc = document.getElementById('appDescripcion').value;
    
    btn.innerText = "Sincronizando Archivos..."; btn.disabled = true;
    document.getElementById('sugerenciasPanel').innerText = "Abriendo canal de flujo continuo...";

    try {
        const response = await fetch('/generar_sistema', {
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
            
            // Va dividiendo el texto y rellenando los paneles en tiempo real mientras descarga
            inyectarTextoEnPaneles(acumuladorText);
        }
    } catch (error) {
        alert("La transmisión de códigos se interrumpió.");
    } finally {
        btn.innerText = "Vincular y Rectificar Sistema"; btn.disabled = false;
    }
});

// Parsea el bloque completo buscando los divisores e inyecta el contenido dinámicamente
function inyectarTextoEnPaneles(texto) {
    const marca1 = texto.indexOf("===ARCHIVO1===");
    const marca2 = texto.indexOf("===ARCHIVO2===");
    const marca3 = texto.indexOf("===ARCHIVO3===");
    const marcaS = texto.indexOf("===SUGERENCIAS===");

    if (marca1 !== -1) {
        let fin = (marca2 !== -1) ? marca2 : texto.length;
        document.getElementById('code1').value = texto.substring(marca1 + 14, fin).trim();
    }
    if (marca2 !== -1) {
        let fin = (marca3 !== -1) ? marca3 : texto.length;
        document.getElementById('code2').value = texto.substring(marca2 + 14, fin).trim();
    }
    if (marca3 !== -1) {
        let fin = (marcaS !== -1) ? marcaS : texto.length;
        document.getElementById('code3').value = texto.substring(marca3 + 14, fin).trim();
    }
    if (marcaS !== -1) {
        document.getElementById('sugerenciasPanel').innerText = texto.substring(marcaS + 17).trim();
    }
}
