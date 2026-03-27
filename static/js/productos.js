const form = document.getElementById("form-producto");
const tabla = document.getElementById("tabla-productos");
const mensaje = document.getElementById("mensaje");
const btn = document.getElementById("recargar");

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
      <td>${p.categoria_id}</td>
      <td>${p.activo ? "Sí" : "No"}</td>
    `;

    tabla.appendChild(row);
  });
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
    categoria_id: Number(document.getElementById("categoria_id").value)
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
  cargarProductos();
});

btn.addEventListener("click", cargarProductos);

cargarProductos();