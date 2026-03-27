// async function cargarKPIs() {
//   try {
//     const ventas = await fetch("/ventas").then(r => r.json());
//     const clientes = await fetch("/clientes").then(r => r.json());
//     const productos = await fetch("/productos").then(r => r.json());

//     document.getElementById("kpi-clientes").textContent = clientes.length;
//     document.getElementById("kpi-productos").textContent = productos.length;

//     let totalUnidades = 0;
//     let ventasHoy = 0;

//     const hoy = new Date().toISOString().split("T")[0];

//     for (const v of ventas) {
//       // Contar ventas del día
//       if (v.fecha.startsWith(hoy)) {
//         ventasHoy++;
//       }

//       // Necesitamos detalle de la venta
//       const detalle = await fetch(`/ventas/${v.id}`).then(r => r.json());

//       for (const item of detalle.items) {
//         totalUnidades += item.cantidad;
//       }
//     }

//     document.getElementById("kpi-unidades").textContent = totalUnidades;
//     document.getElementById("kpi-ventas-hoy").textContent = ventasHoy;

//   } catch (e) {
//     console.error("Error cargando KPIs", e);
//   }
// }

// cargarKPIs();

async function cargarKPIs() {
  try {
    const response = await fetch("/dashboard/kpis");
    const data = await response.json();

    const clientesEl = document.getElementById("kpi-clientes");
    const productosEl = document.getElementById("kpi-productos");
    const unidadesEl = document.getElementById("kpi-unidades");
    const ventasHoyEl = document.getElementById("kpi-ventas-hoy");

    if (clientesEl) clientesEl.textContent = data.clientes;
    if (productosEl) productosEl.textContent = data.productos;
    if (unidadesEl) unidadesEl.textContent = data.unidades_vendidas;
    if (ventasHoyEl) ventasHoyEl.textContent = data.ventas_del_dia;
  } catch (error) {
    console.error("Error cargando KPIs:", error);
  }
}

cargarKPIs();