<template>
  <AppLayout>
    <h2 class="page-title">Dashboard</h2>

    <!-- Tarjetas de resumen -->
    <div class="cards">
      <div class="card" v-for="stat in stats" :key="stat.label">
        <div class="card-icon">{{ stat.icon }}</div>
        <div class="card-info">
          <span class="card-value">{{ stat.value }}</span>
          <span class="card-label">{{ stat.label }}</span>
        </div>
      </div>
    </div>

    <!-- Últimas donaciones -->
    <div class="section">
      <h3>Últimas donaciones</h3>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Donante ID</th>
              <th>Fecha</th>
              <th>Volumen</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in ultimasDonaciones" :key="d.id">
              <td>#{{ d.id }}</td>
              <td>#{{ d.donante_id }}</td>
              <td>{{ formatFecha(d.fecha) }}</td>
              <td>{{ d.volumen_ml }} ml</td>
              <td><span :class="['badge', d.estado]">{{ d.estado }}</span></td>
            </tr>
            <tr v-if="ultimasDonaciones.length === 0">
              <td colspan="5" class="empty">Sin donaciones registradas</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppLayout from "@/components/AppLayout.vue";
import api from "@/apiServices/authService";

const stats = ref([
  { icon: "👤", label: "Donantes",      value: "—" },
  { icon: "💉", label: "Donaciones",    value: "—" },
  { icon: "🗃️", label: "Inventario",    value: "—" },
  { icon: "📋", label: "Solicitudes",   value: "—" },
]);

const ultimasDonaciones = ref([]);

const formatFecha = (f) => new Date(f).toLocaleDateString("es-MX");

onMounted(async () => {
  try {
    const [donantes, donaciones, inventario, solicitudes] = await Promise.all([
      api.get("/api/donantes/"),
      api.get("/api/donaciones/"),
      api.get("/api/inventario/"),
      api.get("/api/solicitudes/"),
    ]);
    stats.value[0].value = donantes.data.length;
    stats.value[1].value = donaciones.data.length;
    stats.value[2].value = inventario.data.length;
    stats.value[3].value = solicitudes.data.length;

    // Mostrar solo las últimas 5 donaciones
    ultimasDonaciones.value = donaciones.data.slice(-5).reverse();
  } catch (e) {
    console.error(e);
  }
});
</script>

<style scoped>
.page-title {
  margin: 0 0 1.5rem;
  color: #333;
  font-size: 1.4rem;
}

/* ── Tarjetas ─────────────────────────────────────── */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.card-icon { font-size: 2rem; }

.card-value {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: #b71c1c;
  line-height: 1;
}

.card-label {
  font-size: 0.85rem;
  color: #888;
}

/* ── Sección tabla ────────────────────────────────── */
.section h3 {
  margin: 0 0 1rem;
  color: #333;
  font-size: 1rem;
}

.table-wrapper {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

table {
  width: 100%;
  border-collapse: collapse;
}

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

.empty {
  text-align: center;
  color: #aaa;
}

.badge {
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge.pendiente { background: #fff3cd; color: #856404; }
.badge.aprobada  { background: #d4edda; color: #155724; }
.badge.rechazada { background: #f8d7da; color: #721c24; }
</style>
