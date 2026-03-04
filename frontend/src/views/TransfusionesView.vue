<template>
  <AppLayout>
    <div class="page-header">
      <h2 class="page-title">🔄 Transfusiones</h2>
      <button class="btn-primary" @click="abrirFormulario()">+ Registrar transfusión</button>
    </div>

    <!-- Tabla -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Solicitud ID</th>
            <th>Inventario ID</th>
            <th>Fecha</th>
            <th>Realizada por</th>
            <th>Observaciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in transfusiones" :key="t.id">
            <td>#{{ t.id }}</td>
            <td>#{{ t.solicitud_id }}</td>
            <td>#{{ t.inventario_id }}</td>
            <td>{{ formatFecha(t.fecha) }}</td>
            <td>{{ t.realizada_por || "—" }}</td>
            <td>{{ t.observaciones || "—" }}</td>
          </tr>
          <tr v-if="transfusiones.length === 0">
            <td colspan="6" class="empty">Sin transfusiones registradas</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="modal" class="overlay" @click.self="modal = false">
      <div class="modal">
        <h3>Registrar transfusión</h3>

        <div class="info-box">
          <p>⚠️ Para registrar una transfusión:</p>
          <ul>
            <li>La <strong>solicitud</strong> debe estar en estado <strong>aprobada</strong></li>
            <li>La <strong>unidad de inventario</strong> debe estar <strong>disponible</strong></li>
          </ul>
        </div>

        <div class="grid2">
          <div class="field">
            <label>ID de Solicitud</label>
            <input v-model="form.solicitud_id" type="number" placeholder="Ej: 1" />
          </div>
          <div class="field">
            <label>ID de Inventario</label>
            <input v-model="form.inventario_id" type="number" placeholder="Ej: 1" />
          </div>
          <div class="field">
            <label>Realizada por</label>
            <input v-model="form.realizada_por" placeholder="Dr. Nombre" />
          </div>
          <div class="field">
            <label>Observaciones</label>
            <input v-model="form.observaciones" placeholder="Observaciones..." />
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

const transfusiones = ref([]);
const modal         = ref(false);
const error         = ref("");
const form          = ref({});

const formatFecha = (f) => new Date(f).toLocaleDateString("es-MX");

async function cargar() {
  const { data } = await api.get("/api/transfusiones/");
  transfusiones.value = data;
}

function abrirFormulario() {
  error.value = "";
  form.value  = {
    solicitud_id: "",
    inventario_id: "",
    realizada_por: "",
    observaciones: "",
  };
  modal.value = true;
}

async function guardar() {
  error.value = "";
  try {
    await api.post("/api/transfusiones/", form.value);
    modal.value = false;
    cargar();
  } catch (e) {
    error.value = e.response?.data?.detail || "Error al registrar";
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
  width: 520px;
  max-width: 95vw;
}

.modal h3 { margin: 0 0 1rem; color: #333; }

.info-box {
  background: #fff8e1;
  border: 1px solid #ffe082;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin-bottom: 1.25rem;
  font-size: 0.85rem;
  color: #5d4037;
}

.info-box p { margin: 0 0 0.4rem; font-weight: 600; }
.info-box ul { margin: 0; padding-left: 1.2rem; }
.info-box li { margin-bottom: 0.2rem; }

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

input {
  padding: 0.6rem 0.8rem;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  font-size: 0.9rem;
  outline: none;
}
input:focus { border-color: #e53935; }

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
  color: #333;
}
</style>
