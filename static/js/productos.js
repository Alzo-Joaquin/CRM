const form = document.getElementById("form-producto");
const tabla = document.getElementById("tabla-productos");
const mensaje = document.getElementById("mensaje");
const btn = document.getElementById("recargar");
const selectCategoria = document.getElementById("categoria_id");

async function cargarProductos() {
  const res = await fetch("/productos");
  const data = await res.json();

  tabla.innerHTML = "";

  data.forEach(p => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${p.id}</td>
      <td>${p.nombre}</td>
      <td>${p.descripcion ?? ""}</td>
      <td>${p.precio}</td>
      <td>${p.costo}</td>
      <td>${p.stock_actual}</td>
      <td>${p.stock_minimo}</td>
      <td>${p.categoria ?? ""}</td>
      <td>${p.activo ? "Sí" : "No"}</td>
    `;

    tabla.appendChild(row);
  });
}

async function cargarCategorias() {
  try {
    const res = await fetch("/categorias");
    const categorias = await res.json();

    selectCategoria.innerHTML = `<option value="">Seleccionar categoría</option>`;

    categorias.forEach(categoria => {
      const option = document.createElement("option");
      option.value = categoria.id;
      option.textContent = `${categoria.id} - ${categoria.nombre}`;
      selectCategoria.appendChild(option);
    });
  } catch (error) {
    mensaje.innerText = "Error al cargar categorías.";
    mensaje.style.color = "red";
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const producto = {
    nombre: document.getElementById("nombre").value,
    descripcion: document.getElementById("descripcion").value,
    precio: Number(document.getElementById("precio").value),
    costo: Number(document.getElementById("costo").value),
    stock_actual: Number(document.getElementById("stock_actual").value),
    stock_minimo: Number(document.getElementById("stock_minimo").value),
    categoria_id: Number(selectCategoria.value),
  };

  const res = await fetch("/productos", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(producto)
  });

  const data = await res.json();

  if (!res.ok) {
    mensaje.innerText = data.error;
    mensaje.style.color = "red";
    return;
  }

  mensaje.innerText = "Producto creado";
  mensaje.style.color = "green";

  form.reset();
  await cargarCategorias
  await cargarProductos();
});

btn.addEventListener("click", cargarProductos);

async function inicializarPantallaProductos() {
  await cargarCategorias();
  await cargarProductos();
}

inicializarPantallaProductos();