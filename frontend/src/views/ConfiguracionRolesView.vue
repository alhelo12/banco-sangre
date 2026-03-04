<template>
  <AppLayout>
    <div class="page-header">
      <h2 class="page-title">⚙️ Configuración de Roles</h2>
      <button class="btn-primary" @click="abrirFormulario()">+ Nuevo prefijo</button>
    </div>

    <p class="descripcion">
      Define los prefijos de matrícula que identifican cada rol al momento del registro.
      Por ejemplo: si configuras <strong>MED → médico</strong>, cualquier matrícula que
      empiece con <strong>MED-</strong> asignará automáticamente el rol de médico.
    </p>

    <!-- Tabla -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Prefijo</th>
            <th>Rol asignado</th>
            <th>Descripción</th>
            <th>Ejemplo de matrícula</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in configuraciones" :key="c.id">
            <td><span class="badge-prefijo">{{ c.prefijo }}</span></td>
            <td><span :class="['badge-rol', c.rol]">{{ c.rol }}</span></td>
            <td>{{ c.descripcion || "—" }}</td>
            <td class="ejemplo">{{ c.prefijo }}-0001</td>
            <td class="acciones">
              <button class="btn-sm" @click="abrirFormulario(c)">✏️ Editar</button>
              <button class="btn-sm danger" @click="eliminar(c.id)">🗑️ Eliminar</button>
            </td>
          </tr>
          <tr v-if="configuraciones.length === 0">
            <td colspan="5" class="empty">Sin prefijos configurados</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="modal" class="overlay" @click.self="modal = false">
      <div class="modal">
        <h3>{{ form.id ? "Editar prefijo" : "Nuevo prefijo" }}</h3>

        <div class="field">
          <label>Prefijo de matrícula</label>
          <input v-model="form.prefijo" placeholder="Ej: MED, ENF, ADM" />
          <span class="hint">Se guardará en mayúsculas automáticamente</span>
        </div>
        <div class="field">
          <label>Rol que asigna</label>
          <select v-model="form.rol">
            <option value="medico">Médico</option>
            <option value="enfermero">Enfermero</option>
          </select>
        </div>
        <div class="field">
          <label>Descripción (opcional)</label>
          <input v-model="form.descripcion" placeholder="Ej: Personal médico general" />
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <div class="modal-actions">
          <button @click="modal = false">Cancelar</button>
          <button class="btn-primary" @click="guardar">Guardar</button>
        </div>
      </div>
    </div>

  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import api from "@/apiServices/authService";

const configuraciones = ref([]);
const modal           = ref(false);
const error           = ref("");
const form            = ref({});

async function cargar() {
  const { data } = await api.get("/api/configuracion-roles/");
  configuraciones.value = data;
}

function abrirFormulario(c = null) {
  error.value = "";
  form.value  = c
    ? { ...c }
    : { prefijo: "", rol: "medico", descripcion: "" };
  modal.value = true;
}

async function guardar() {
  error.value = "";
  try {
    if (form.value.id) {
      await api.put(`/api/configuracion-roles/${form.value.id}`, form.value);
    } else {
      await api.post("/api/configuracion-roles/", form.value);
    }
    modal.value = false;
    cargar();
  } catch (e) {
    error.value = e.response?.data?.detail || "Error al guardar";
  }
}

async function eliminar(id) {
  if (confirm("¿Eliminar este prefijo? Los usuarios ya registrados no se verán afectados.")) {
    await api.delete(`/api/configuracion-roles/${id}`);
    cargar();
  }
}

onMounted(cargar);
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.page-title { margin: 0; color: #333; font-size: 1.4rem; }

.descripcion {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1.5rem;
  background: #fff8e1;
  border: 1px solid #ffe082;
  border-radius: 8px;
  padding: 0.75rem 1rem;
}

.table-wrapper {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

table { width: 100%; border-collapse: collapse; }

th {
  background: #f9f9f9;
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.85rem;
  color: #666;
}

td {
  padding: 0.75rem 1rem;
  border-top: 1px solid #f0f0f0;
  font-size: 0.9rem;
  color: #333;
}

.empty { text-align: center; color: #aaa; }

.badge-prefijo {
  background: #333;
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 700;
  font-family: monospace;
  letter-spacing: 1px;
}

.badge-rol {
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: capitalize;
}
.badge-rol.medico    { background: #e8fde8; color: #1b5e20; }
.badge-rol.enfermero { background: #e8f4fd; color: #1565c0; }

.ejemplo {
  font-family: monospace;
  color: #888;
  font-size: 0.85rem;
}

.acciones { display: flex; gap: 0.4rem; }

.btn-primary {
  background: #e53935;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
}
.btn-primary:hover { background: #b71c1c; }

.btn-sm {
  background: #f0f0f0;
  border: none;
  padding: 0.35rem 0.7rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
}
.btn-sm.danger { background: #fde8e8; color: #b71c1c; }
.btn-sm:hover { opacity: 0.8; }

/* ── Modal ───────────────────────────────────────── */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  width: 420px;
  max-width: 95vw;
}

.modal h3 { margin: 0 0 1.5rem; color: #333; }

.field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  margin-bottom: 1rem;
}

label { font-size: 0.8rem; font-weight: 600; color: #555; }

.hint { font-size: 0.75rem; color: #999; }

input, select {
  padding: 0.6rem 0.8rem;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 0.9rem;
  outline: none;
}
input:focus, select:focus { border-color: #e53935; }

.error { color: #e53935; font-size: 0.85rem; margin: 0; }

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.modal-actions button {
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}
</style>
