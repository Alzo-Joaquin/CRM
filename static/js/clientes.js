const formCliente = document.getElementById("form-cliente");
const mensaje = document.getElementById("mensaje");
const tablaBody = document.querySelector("#tabla-clientes tbody");
const btnRecargar = document.getElementById("btn-recargar");

async function cargarClientes() {
  try {
    const response = await fetch("/clientes");
    const clientes = await response.json();

    tablaBody.innerHTML = "";

    clientes.forEach(cliente => {
      const fila = document.createElement("tr");

      fila.innerHTML = `
        <td>${cliente.id}</td>
        <td>${cliente.nombre}</td>
        <td>${cliente.apellido}</td>
        <td>${cliente.email}</td>
        <td>${cliente.telefono ?? ""}</td>
        <td>${cliente.direccion ?? ""}</td>
        <td>${cliente.activo ? "Sí" : "No"}</td>
      `;

      tablaBody.appendChild(fila);
    });
  } catch (error) {
    mensaje.textContent = "Error al cargar clientes.";
    mensaje.style.color = "red";
  }
}

formCliente.addEventListener("submit", async (event) => {
  event.preventDefault();

  const nuevoCliente = {
    nombre: document.getElementById("nombre").value,
    apellido: document.getElementById("apellido").value,
    email: document.getElementById("email").value,
    telefono: document.getElementById("telefono").value,
    direccion: document.getElementById("direccion").value
  };

  try {
    const response = await fetch("/clientes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(nuevoCliente)
    });

    const data = await response.json();

    if (!response.ok) {
      mensaje.textContent = data.error || "Error al crear cliente.";
      mensaje.style.color = "red";
      return;
    }

    mensaje.textContent = "Cliente creado correctamente.";
    mensaje.style.color = "green";

    formCliente.reset();
    cargarClientes();
  } catch (error) {
    mensaje.textContent = "Error de conexión con el servidor.";
    mensaje.style.color = "red";
  }
});

btnRecargar.addEventListener("click", cargarClientes);

cargarClientes();