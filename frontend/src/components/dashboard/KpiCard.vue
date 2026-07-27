<template>
  <div class="kpi-card">
    <div class="kpi-card-top">
      <div class="kpi-icon" :style="{ background: color + '18' }">
        <Icon :icon="icon" :size="15" :color="color" />
      </div>
      <Sparkline :data="spark" :color="color" />
    </div>
    <div class="kpi-value">{{ value }}</div>
    <div class="kpi-sub">{{ sub }}</div>
    <div class="kpi-change">
      <span class="kpi-change-value" :class="up ? 'kpi-up' : 'kpi-down'">
        {{ up ? '▲' : '▼' }} {{ Math.abs(change) }}%
      </span>
      <span class="kpi-change-label">vs last period</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Icon from '../Icon.vue'
import Sparkline from './Sparkline.vue'

const props = defineProps({
  label: { type: String, default: '' },
  value: { type: [String, Number], required: true },
  sub: { type: String, default: '' },
  change: { type: Number, required: true },
  color: { type: String, required: true },
  spark: { type: Array, required: true },
  icon: { type: String, required: true },
})
const up = computed(() => props.change >= 0)
</script>