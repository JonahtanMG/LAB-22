const modal = document.getElementById("modal");       
const salida = document.getElementById("salida");     
const cerrarModal = document.getElementById("cerrar-modal");

// Listar equipo
document.getElementById("btn-listar").addEventListener("click", async () => {
    const res = await fetch("/equipos");
    const data = await res.json();
    // Mostrar datos en la página
    salida.textContent = JSON.stringify(data, null, 2);
});

// Agragar equipo
document.getElementById("btn-agregar").addEventListener("click", () => {
    modal.style.display = "block";
});

// Cerrar el modal
cerrarModal.addEventListener("click", () => {
    modal.style.display = "none";
});

// Enviar el form
document.getElementById("form-equipo").addEventListener("submit", async (e) => {
    e.preventDefault(); 
    const equipo = {
        nombre: document.getElementById("nombre").value,
        ciudad: document.getElementById("ciudad").value,
        nivelAtaque: parseInt(document.getElementById("ataque").value),
        nivelDefensa: parseInt(document.getElementById("defensa").value)
    };
    
    // Enviar datos al servidor con POST
    const res = await fetch("/equipos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(equipo)
    });
    
    // Obtener respuesta del servidor
    const data = await res.json();
    
    // Mostrar resultado y cerrar 
    salida.textContent = "Equipo agregado:" + JSON.stringify(data, null, 2);
    modal.style.display = "none";
});

// Buscar por id
document.getElementById("btn-buscar").addEventListener("click", async () => {
    const id = document.getElementById("buscar-id").value;
    if (!id) {
        alert("Ingrese un ID valido");
        return;
    }
    const res = await fetch(`/equipos/${id}`);
    // Si es 404 mostrar error, sino mostrar datos
    if (res.status === 404) {
        salida.textContent = "Equipo no encontrado";
    } else {
        const data = await res.json();
        salida.textContent = JSON.stringify(data, null, 2);
    }
});