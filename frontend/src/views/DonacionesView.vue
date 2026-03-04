<template>
  <AppLayout>
    <div class="page-header">
      <h2 class="page-title">💉 Donaciones</h2>
      <button class="btn-primary" @click="abrirFormulario()">+ Nueva donación</button>
    </div>

    <!-- Tabla -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Donante ID</th>
            <th>Fecha</th>
            <th>Volumen</th>
            <th>Estado</th>
            <th>Notas</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in donaciones" :key="d.id">
            <td>#{{ d.id }}</td>
            <td>#{{ d.donante_id }}</td>
            <td>{{ formatFecha(d.fecha) }}</td>
            <td>{{ d.volumen_ml }} ml</td>
            <td><span :class="['badge', d.estado]">{{ d.estado }}</span></td>
            <td>{{ d.notas || "—" }}</td>
            <td>
              <select @change="cambiarEstado(d.id, $event.target.value)" :value="d.estado">
                <option value="pendiente">Pendiente</option>
                <option value="aprobada">Aprobada</option>
                <option value="rechazada">Rechazada</option>
              </select>
            </td>
          </tr>
          <tr v-if="donaciones.length === 0">
            <td colspan="7" class="empty">Sin donaciones registradas</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="modal" class="overlay" @click.self="modal = false">
      <div class="modal">
        <h3>Nueva donación</h3>

        <div class="field">
          <label>ID del Donante</label>
          <input v-model="form.donante_id" type="number" placeholder="Ej: 1" />
        </div>
        <div class="field">
          <label>Volumen (ml)</label>
          <input v-model="form.volumen_ml" type="number" placeholder="450" />
        </div>
        <div class="field">
          <label>Notas</label>
          <textarea v-model="form.notas" rows="3" placeholder="Observaciones..."></textarea>
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

const donaciones = ref([]);
const modal      = ref(false);
const error      = ref("");
const form       = ref({ donante_id: "", volumen_ml: 450, notas: "" });

const formatFecha = (f) => new Date(f).toLocaleDateString("es-MX");

async function cargar() {
  const { data } = await api.get("/api/donaciones/");
  donaciones.value = data;
}

function abrirFormulario() {
  error.value = "";
  form.value  = { donante_id: "", volumen_ml: 450, notas: "" };
  modal.value = true;
}

async function guardar() {
  error.value = "";
  try {
    await api.post("/api/donaciones/", form.value);
    modal.value = false;
    cargar();
  } catch (e) {
    error.value = e.response?.data?.detail || "Error al guardar";
  }
}

async function cambiarEstado(id, estado) {
  try {
    await api.patch(`/api/donaciones/${id}/estado`, { estado });
    cargar();
  } catch (e) {
    console.error(e);
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

.badge {
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}
.badge.pendiente { background: #fff3cd; color: #856404; }
.badge.aprobada  { background: #d4edda; color: #155724; }
.badge.rechazada { background: #f8d7da; color: #721c24; }

select {
  padding: 0.35rem 0.6rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
}

.btn-primary {
  background: #e53935;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  color: #333;
}
.btn-primary:hover { background: #b71c1c; }

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

input, textarea {
  padding: 0.6rem 0.8rem;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 0.9rem;
  outline: none;
  resize: vertical;
}
input:focus, textarea:focus { border-color: #e53935; }

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
  color: #333;
}
</style>
