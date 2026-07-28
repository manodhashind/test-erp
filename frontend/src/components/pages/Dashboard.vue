<script setup>
import { ref, onMounted } from 'vue'
import KpiCard from '../dashboard/KpiCard.vue'
import DonutChart from '../dashboard/DonutChart.vue'

const colors = {
  primary: '#6742CF',
  success: '#10B981',
  info: '#3B82F6',
  amber: '#CE5BA9',
}

const projectTrend = [8, 9, 10, 11, 12, 13, 13, 14]
const workerTrend = ref([98, 102, 105, 110, 118, 120, 124, 127]) // last value gets replaced live below
const scheduleTrend = [92, 91, 90, 89, 90, 89, 88, 88]
const deliveryTrend = [280, 295, 300, 310, 320, 330, 336, 342]

const siteStatusSegments = [
  { label: 'On track', pct: 58, color: '#10B981' },
  { label: 'At risk', pct: 27, color: '#CE5BA9' },
  { label: 'Delayed', pct: 15, color: '#EF4444' },
]

const activeUserCount = ref(0)
const loadingUsers = ref(true)

async function loadActiveUsers() {
  loadingUsers.value = true
  try {
    const res = await fetch('/api/method/construction_management.api.get_all_users', {
      credentials: 'include',
    })
    const data = await res.json()
    const users = data.message || []
    activeUserCount.value = users.filter(u => u.enabled).length
    // swap the trend's last point with the real live count so the sparkline reflects reality
    workerTrend.value = [...workerTrend.value.slice(0, -1), activeUserCount.value]
  } catch (e) {
    console.error('Failed to load active users', e)
  } finally {
    loadingUsers.value = false
  }
}

onMounted(loadActiveUsers)
</script>

<template>
  <div>
    <div class="kpi-row">
      <KpiCard
        icon="hard-hat"
        label="Active projects"
        value="14"
        sub="currently in progress"
        :change="8.3"
        :color="colors.primary"
        :spark="projectTrend"
      />
      <KpiCard
        icon="users"
        label="On-site workers"
        :value="loadingUsers ? '…' : activeUserCount.toLocaleString()"
        sub="Active Users"
        :change="4.1"
        :color="colors.farimary"
        :spark="workerTrend"
      />
      <KpiCard
        icon="check-circle"
        label="On-schedule rate"
        value="88%"
        sub="milestone average"
        :change="-2.4"
        :color="colors.info"
        :spark="scheduleTrend"
      />
      <KpiCard
        icon="package"
        label="Material deliveries"
        value="342"
        sub="this quarter"
        :change="6.7"
        :color="colors.amber"
        :spark="deliveryTrend"
      />
    </div>

    <div class="dashboard-row">
      <div class="panel" style="max-width:none; flex:2">
        <h3 style="margin-bottom:16px">Project status</h3>
        <p style="color:var(--muted); font-size:13px">Trend charts for project progress will go here.</p>
      </div>
      <div class="panel" style="max-width:none; flex:1; display:flex; flex-direction:column; align-items:center">
        <h3 style="margin-bottom:16px; align-self:flex-start">Site status</h3>
        <DonutChart :segments="siteStatusSegments" :total="14" unit-label="projects" :size="150" />
        <div class="donut-legend">
          <div v-for="s in siteStatusSegments" :key="s.label" class="donut-legend-item">
            <span class="donut-dot" :style="{ background: s.color }"></span>
            {{ s.label }} — {{ s.pct }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>