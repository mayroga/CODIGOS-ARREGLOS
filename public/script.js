document.getElementById('btnCorregir').addEventListener('click', async () => {
    const codigoInput = document.getElementById('codigoSucio').value;
    const btnText = document.getElementById('btnCorregir');
    
    if (!codigoInput.trim()) {
        return alert("Por favor, ingresa algún código primero.");
    }

    btnText.innerText = "Corrigiendo...";
    btnText.disabled = true;

    try {
        const response = await fetch('/corregir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ codigo: codigoInput })
        });
        
        const data = await response.json();
        if (data.error) throw new Error(data.error);
        
        document.getElementById('codigoLimpio').value = data.codigoCorregido;
    } catch (error) {
        alert("Hubo un problema al reparar el código. Verifica la conexión.");
    } finally {
        btnText.innerText = "Corregir Código";
        btnText.disabled = false;
    }
});

// El botón que limpia de inmediato el área para seguir trabajando de forma ágil
document.getElementById('btnBorrar').addEventListener('click', () => {
    document.getElementById('codigoSucio').value = "";
    document.getElementById('codigoLimpio').value = "";
});
