const formSolicitud = document.getElementById("form-solicitud-stock");
const selectProducto = document.getElementById("producto_id");
const inputCantidad = document.getElementById("cantidad");
const inputObservaciones = document.getElementById("observaciones");
const mensajeSolicitud = document.getElementById("mensaje-solicitud-stock");
const tablaSolicitudes = document.getElementById("tabla-solicitudes-stock");
const btnRecargarSolicitudes = document.getElementById("btn-recargar-solicitudes");

async function cargarProductos() {
  const response = await fetch("/productos?activo=true");
  const productos = await response.json();

  selectProducto.innerHTML = `<option value="">Seleccionar producto</option>`;

  productos.forEach(producto => {
    const option = document.createElement("option");
    option.value = producto.id;
    option.textContent = `${producto.nombre} (stock actual: ${producto.stock_actual})`;
    selectProducto.appendChild(option);
  });
}

async function cargarSolicitudes() {
  const response = await fetch("/solicitudes-stock");
  const solicitudes = await response.json();

  tablaSolicitudes.innerHTML = "";

  solicitudes.forEach(solicitud => {
    const fila = document.createElement("tr");

    fila.innerHTML = `
      <td>${solicitud.id}</td>
      <td>${solicitud.producto ?? ""}</td>
      <td>${solicitud.cantidad}</td>
      <td>${solicitud.estado}</td>
      <td>${solicitud.observaciones ?? ""}</td>
      <td>${solicitud.fecha_creacion ?? ""}</td>
    `;

    tablaSolicitudes.appendChild(fila);
  });
}

formSolicitud.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    producto_id: Number(selectProducto.value),
    cantidad: Number(inputCantidad.value),
    observaciones: inputObservaciones.value.trim()
  };

  try {
    const response = await fetch("/solicitudes-stock", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      mensajeSolicitud.textContent = data.error || "Error al crear la solicitud.";
      mensajeSolicitud.style.color = "red";
      return;
    }

    mensajeSolicitud.textContent = "Solicitud enviada correctamente.";
    mensajeSolicitud.style.color = "green";

    formSolicitud.reset();
    await cargarSolicitudes();
    await cargarProductos();
  } catch (error) {
    mensajeSolicitud.textContent = "Error de conexión con el servidor.";
    mensajeSolicitud.style.color = "red";
  }
});

btnRecargarSolicitudes.addEventListener("click", cargarSolicitudes);

async function inicializarSolicitudStock() {
  await cargarProductos();
  await cargarSolicitudes();
}

inicializarSolicitudStock();