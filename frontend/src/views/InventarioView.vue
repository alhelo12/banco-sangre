<template>
  <AppLayout>
    <div class="page-header">
      <h2 class="page-title">🗃️ Inventario de Sangre</h2>
      <button class="btn-primary" @click="abrirFormulario()">+ Agregar unidad</button>
    </div>

    <!-- Tabla -->
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Tipo sangre</th>
            <th>Componente</th>
            <th>Volumen</th>
            <th>Vence</th>
            <th>Disponibilidad</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in inventario" :key="u.id">
            <td>#{{ u.id }}</td>
            <td><span class="badge-sangre">{{ u.tipo_sangre }}</span></td>
            <td>{{ u.componente }}</td>
            <td>{{ u.volumen_ml }} ml</td>
            <td>{{ u.fecha_exp }}</td>
            <td>
              <span :class="['badge', u.disponible ? 'disponible' : 'usado']">
                {{ u.disponible ? "Disponible" : "Usado" }}
              </span>
            </td>
            <td>
              <select @change="cambiarDisponible(u.id, $event.target.value)" :value="u.disponible">
                <option :value="true">Disponible</option>
                <option :value="false">Usado</option>
              </select>
            </td>
          </tr>
          <tr v-if="inventario.length === 0">
            <td colspan="7" class="empty">Sin unidades en inventario</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="modal" class="overlay" @click.self="modal = false">
      <div class="modal">
        <h3>Agregar unidad al inventario</h3>

        <div class="grid2">
          <div class="field">
            <label>ID de Donación</label>
            <input v-model="form.donacion_id" type="number" placeholder="Ej: 1" />
          </div>
          <div class="field">
            <label>Tipo de sangre</label>
            <select v-model="form.tipo_sangre">
              <option v-for="t in tipos" :key="t">{{ t }}</option>
            </select>
          </div>
          <div class="field">
            <label>Componente</label>
            <select v-model="form.componente">
              <option value="sangre total">Sangre total</option>
              <option value="plasma">Plasma</option>
              <option value="plaquetas">Plaquetas</option>
              <option value="globulos rojos">Glóbulos rojos</option>
            </select>
          </div>
          <div class="field">
            <label>Volumen (ml)</label>
            <input v-model="form.volumen_ml" type="number" placeholder="450" />
          </div>
          <div class="field full">
            <label>Fecha de vencimiento</label>
            <input v-model="form.fecha_exp" type="date" />
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

const inventario = ref([]);
const modal      = ref(false);
const error      = ref("");
const tipos      = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];
const form       = ref({});

async function cargar() {
  const { data } = await api.get("/api/inventario/");
  inventario.value = data;
}

function abrirFormulario() {
  error.value = "";
  form.value  = {
    donacion_id: "",
    tipo_sangre: "O+",
    componente: "sangre total",
    volumen_ml: 450,
    fecha_exp: "",
  };
  modal.value = true;
}

async function guardar() {
  error.value = "";
  try {
    await api.post("/api/inventario/", form.value);
    modal.value = false;
    cargar();
  } catch (e) {
    error.value = e.response?.data?.detail || "Error al guardar";
  }
}

async function cambiarDisponible(id, valor) {
  try {
    await api.patch(`/api/inventario/${id}/disponible`, {
      disponible: valor === "true" || valor === true,
    });
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

.badge {
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}
.badge.disponible { background: #d4edda; color: #155724; }
.badge.usado      { background: #e2e3e5; color: #383d41; }

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

.field.full { grid-column: 1 / -1; }

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
