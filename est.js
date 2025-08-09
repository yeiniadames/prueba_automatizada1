let estudiantes = JSON.parse(localStorage.getItem("estudiantes")) || [];
let editIndex = null;

function guardarEnLocal() {
  localStorage.setItem("estudiantes", JSON.stringify(estudiantes));
}

function renderTabla() {
  const tabla = document.getElementById("tablaEstudiantes");
  tabla.innerHTML = "";
  estudiantes.forEach((e, i) => {
    tabla.innerHTML += `
      <tr>
        <td>${e.nombre}</td>
        <td>${e.apellido}</td>
        <td>${e.matricula}</td>
        <td>${e.carrera}</td>
        <td class="actions">
          <button class="editar" onclick="editar(${i})">Editar</button>
          <button class="eliminar" onclick="eliminar(${i})">Eliminar</button>
        </td>
      </tr>
    `;
  });
}

function editar(index) {
  const estudiante = estudiantes[index];
  document.getElementById("nombre").value = estudiante.nombre;
  document.getElementById("apellido").value = estudiante.apellido;
  document.getElementById("matricula").value = estudiante.matricula;
  document.getElementById("carrera").value = estudiante.carrera;
  editIndex = index;
}

function eliminar(index) {
  if (confirm("¿Estás seguro de eliminar este estudiante?")) {
    estudiantes.splice(index, 1);
    guardarEnLocal();
    renderTabla();
  }
}

document.getElementById("estudianteForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const nombre = document.getElementById("nombre").value.trim();
  const apellido = document.getElementById("apellido").value.trim();
  const matricula = document.getElementById("matricula").value.trim();
  const carrera = document.getElementById("carrera").value.trim();

  const nuevoEstudiante = { nombre, apellido, matricula, carrera };

  if (editIndex === null) {
    estudiantes.push(nuevoEstudiante);
  } else {
    estudiantes[editIndex] = nuevoEstudiante;
    editIndex = null;
  }

  guardarEnLocal();
  renderTabla();
  this.reset();
});

renderTabla();
