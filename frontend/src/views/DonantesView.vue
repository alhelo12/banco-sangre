<template>
  <AppLayout>
    <div class="page-header">
      <h2 class="page-title">👤 Donantes</h2>
      <button class="btn-primary" @click="abrirFormulario()">+ Nuevo donante</button>
    </div>

    <!-- Tabla -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Tipo sangre</th>
            <th>Fecha nac.</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in donantes" :key="d.id">
            <td>{{ d.nombre }} {{ d.apellido }}</td>
            <td><span class="badge-sangre">{{ d.tipo_sangre }}</span></td>
            <td>{{ d.fecha_nac }}</td>
            <td>{{ d.telefono || "—" }}</td>
            <td>{{ d.email || "—" }}</td>
            <td class="acciones">
              <button class="btn-sm" @click="abrirFormulario(d)">✏️ Editar</button>
              <button class="btn-sm danger" @click="eliminar(d.id)">🗑️ Eliminar</button>
            </td>
          </tr>
          <tr v-if="donantes.length === 0">
            <td colspan="6" class="empty">Sin donantes registrados</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="modal" class="overlay" @click.self="modal = false">
      <div class="modal">
        <h3>{{ form.id ? "Editar donante" : "Nuevo donante" }}</h3>

        <div class="grid2">
          <div class="field">
            <label>Nombre</label>
            <input v-model="form.nombre" placeholder="Juan" />
          </div>
          <div class="field">
            <label>Apellido</label>
            <input v-model="form.apellido" placeholder="Pérez" />
          </div>
          <div class="field">
            <label>Fecha de nacimiento</label>
            <input v-model="form.fecha_nac" type="date" />
          </div>
          <div class="field">
            <label>Tipo de sangre</label>
            <select v-model="form.tipo_sangre">
              <option v-for="t in tipos" :key="t">{{ t }}</option>
            </select>
          </div>
          <div class="field">
            <label>Teléfono</label>
            <input v-model="form.telefono" placeholder="5551234567" />
          </div>
          <div class="field">
            <label>Email</label>
            <input v-model="form.email" type="email" placeholder="juan@email.com" />
          </div>
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

const donantes = ref([]);
const modal    = ref(false);
const error    = ref("");
const tipos    = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];
const form     = ref({});

async function cargar() {
  const { data } = await api.get("/api/donantes/");
  donantes.value = data;
}

function abrirFormulario(d = null) {
  error.value = "";
  form.value  = d
    ? { ...d }
    : { nombre: "", apellido: "", fecha_nac: "", tipo_sangre: "O+", telefono: "", email: "" };
  modal.value = true;
}

async function guardar() {
  error.value = "";
  try {
    if (form.value.id) {
      await api.put(`/api/donantes/${form.value.id}`, form.value);
    } else {
      await api.post("/api/donantes/", form.value);
    }
    modal.value = false;
    cargar();
  } catch (e) {
    error.value = e.response?.data?.detail || "Error al guardar";
  }
}

async function eliminar(id) {
  if (confirm("¿Eliminar este donante?")) {
    await api.delete(`/api/donantes/${id}`);
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
  margin-bottom: 1.5rem;
}

.page-title { margin: 0; color: #333; font-size: 1.4rem; }

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

.badge-sangre {
  background: #fde8e8;
  color: #b71c1c;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.8rem;
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
  width: 520px;
  max-width: 95vw;
}

.modal h3 { margin: 0 0 1.5rem; color: #333; }

.grid2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

label { font-size: 0.8rem; font-weight: 600; color: #555; }

input, select {
  padding: 0.6rem 0.8rem;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 0.9rem;
  outline: none;
}
input:focus, select:focus { border-color: #e53935; }

.error { color: #e53935; font-size: 0.85rem; margin: 0.5rem 0 0; }

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
