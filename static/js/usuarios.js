const formUsuario = document.getElementById("form-usuario");
const tablaUsuarios = document.getElementById("tabla-usuarios");
const mensajeUsuario = document.getElementById("mensaje-usuario");
const btnRecargarUsuarios = document.getElementById("btn-recargar-usuarios");

async function cargarUsuarios() {
  try {
    const response = await fetch("/usuarios");
    const usuarios = await response.json();

    tablaUsuarios.innerHTML = "";

    usuarios.forEach(usuario => {
      const fila = document.createElement("tr");

      fila.innerHTML = `
        <td>${usuario.id}</td>
        <td>${usuario.nombre}</td>
        <td>${usuario.email}</td>
        <td>${usuario.rol}</td>
        <td>${usuario.activo ? "Sí" : "No"}</td>
      `;

      tablaUsuarios.appendChild(fila);
    });
  } catch (error) {
    mensajeUsuario.textContent = "Error al cargar usuarios.";
    mensajeUsuario.style.color = "red";
  }
}

formUsuario.addEventListener("submit", async (event) => {
  event.preventDefault();

  const nuevoUsuario = {
    nombre: document.getElementById("nombre").value,
    email: document.getElementById("email").value,
    rol: document.getElementById("rol").value,
    password: document.getElementById("password").value
  };

  try {
    const response = await fetch("/usuarios", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(nuevoUsuario)
    });

    const data = await response.json();

    if (!response.ok) {
      mensajeUsuario.textContent = data.error || "Error al crear usuario.";
      mensajeUsuario.style.color = "red";
      return;
    }

    mensajeUsuario.textContent = "Usuario creado correctamente.";
    mensajeUsuario.style.color = "green";

    formUsuario.reset();
    await cargarUsuarios();
  } catch (error) {
    mensajeUsuario.textContent = "Error de conexión con el servidor.";
    mensajeUsuario.style.color = "red";
  }
});

btnRecargarUsuarios.addEventListener("click", cargarUsuarios);

cargarUsuarios();