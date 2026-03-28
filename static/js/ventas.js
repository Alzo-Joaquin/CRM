const selectCliente = document.getElementById("cliente");
const selectUsuario = document.getElementById("usuario");
const selectProducto = document.getElementById("producto");
const inputCantidad = document.getElementById("cantidad");
const formVenta = document.getElementById("form-venta");
const mensajeVenta = document.getElementById("mensaje-venta");
const tablaVentas = document.getElementById("tabla-ventas");
const btnRecargarVentas = document.getElementById("btn-recargar-ventas");
const btnAnterior = document.getElementById("btn-anterior");
const btnSiguiente = document.getElementById("btn-siguiente");
const infoPagina = document.getElementById("info-pagina");
const inputEmailCliente = document.getElementById("email_cliente");

let paginaActual = 1;
const limitePorPagina = 5;
let totalPaginas = 1;

async function cargarClientes() {
  const response = await fetch("/clientes?activo=true");
  const clientes = await response.json();

  selectCliente.innerHTML = `<option value="">Seleccionar cliente</option>`;

  clientes.forEach(cliente => {
    const option = document.createElement("option");
    option.value = cliente.id;
    option.textContent = `${cliente.id} - ${cliente.nombre} ${cliente.apellido}`;
    selectCliente.appendChild(option);
  });
}

async function cargarUsuarios() {
  if (!selectUsuario || selectUsuario.tagName !== "SELECT") {
    return;
  }

  const response = await fetch("/usuarios?activo=true");
  const usuarios = await response.json();

  selectUsuario.innerHTML = `<option value="">Seleccionar usuario</option>`;

  usuarios.forEach(usuario => {
    const option = document.createElement("option");
    option.value = usuario.id;
    option.textContent = `${usuario.id} - ${usuario.nombre} (${usuario.rol})`;
    selectUsuario.appendChild(option);
  });
}

async function cargarProductos() {
  const response = await fetch("/productos?activo=true");
  const productos = await response.json();

  selectProducto.innerHTML = `<option value="">Seleccionar producto</option>`;

  productos.forEach(producto => {
    const option = document.createElement("option");
    option.value = producto.id;
    option.textContent = `${producto.id} - ${producto.nombre} | Stock: ${producto.stock_actual} | Precio: ${producto.precio}`;
    selectProducto.appendChild(option);
  });
}

async function cargarVentas() {
  const response = await fetch(`/ventas?page=${paginaActual}&limit=${limitePorPagina}`);
  const data = await response.json();

  const ventas = data.results;
  totalPaginas = data.pages;

  tablaVentas.innerHTML = "";

  for (const venta of ventas) {
    const fila = document.createElement("tr");

    const resumenProductos = venta.items
      .map(item => `${item.producto} x${item.cantidad}`)
      .join(", ");

    fila.innerHTML = `
      <td>${venta.id}</td>
      <td>${venta.cliente}</td>
      <td>${venta.usuario}</td>
      <td>${resumenProductos}</td>
      <td>${venta.total}</td>
      <td>${venta.estado}</td>
      <td>${venta.fecha ?? ""}</td>
    `;

    tablaVentas.appendChild(fila);
  }

  infoPagina.textContent = `Página ${data.page} de ${data.pages}`;
  btnAnterior.disabled = paginaActual <= 1;
  btnSiguiente.disabled = paginaActual >= totalPaginas;
}

formVenta.addEventListener("submit", async (event) => {
  event.preventDefault();

  const clienteId = Number(selectCliente.value);
  const usuarioId = Number(selectUsuario.value);
  const productoId = Number(selectProducto.value);
  const cantidad = Number(inputCantidad.value);
  const emailCliente = inputEmailCliente.value.trim();

  const venta = {
    cliente_id: clienteId,
    usuario_id: usuarioId,
    email: emailCliente,
    items: [
      {
        producto_id: productoId,
        cantidad: cantidad
      }
    ]
  };

  try {
    const response = await fetch("/ventas", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(venta)
    });

    const data = await response.json();

    if (!response.ok) {
      mensajeVenta.textContent = data.error || "Error al registrar la venta.";
      mensajeVenta.style.color = "red";
      return;
    }

    mensajeVenta.textContent = `Venta registrada correctamente. ID venta: ${data.id}`;
    mensajeVenta.style.color = "green";

    formVenta.reset();

    await cargarVentas();
    await cargarProductos();
  } catch (error) {
    mensajeVenta.textContent = "Error de conexión con el servidor.";
    mensajeVenta.style.color = "red";
  }
});

btnRecargarVentas.addEventListener("click", async () => {
  paginaActual = 1;
  await cargarVentas();
  await cargarProductos();
});

btnAnterior.addEventListener("click", async () => {
  if (paginaActual > 1) {
    paginaActual--;
    await cargarVentas();
  }
});

btnSiguiente.addEventListener("click", async () => {
  if (paginaActual < totalPaginas) {
    paginaActual++;
    await cargarVentas();
  }
});

async function inicializarPantallaVentas() {
  await cargarClientes();
  await cargarUsuarios();
  await cargarProductos();
  await cargarVentas();
}

inicializarPantallaVentas();