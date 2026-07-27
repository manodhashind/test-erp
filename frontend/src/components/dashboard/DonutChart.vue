<template>
  <svg
    viewBox="0 0 156 156"
    :style="fluid ? {} : { height: `${size}px`, width: `${size}px` }"
    style="display:block; flex-shrink:0"
  >
    <circle :cx="cx" :cy="cy" r="52" fill="none" stroke="var(--line)" :stroke-width="sw" />
    <g :transform="`rotate(-90 ${cx} ${cy})`">
      <circle
        v-for="(s, i) in arcs"
        :key="i"
        :cx="cx"
        :cy="cy"
        r="52"
        fill="none"
        :stroke="s.color"
        :stroke-width="sw"
        :stroke-dasharray="s.dash"
        :stroke-dashoffset="s.offset"
      />
    </g>
    <text :x="cx" :y="cy - 7" text-anchor="middle" font-size="20" font-weight="800" fill="var(--charcoal)">
      {{ total.toLocaleString() }}
    </text>
    <text :x="cx" :y="cy + 11" text-anchor="middle" font-size="9.5" fill="var(--muted)">
      {{ unitLabel }}
    </text>
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  segments: { type: Array, required: true },
  total: { type: Number, required: true },
  size: { type: Number, default: 132 },
  fluid: { type: Boolean, default: false },
  unitLabel: { type: String, default: 'items' },
})

const cx = 78
const cy = 78
const sw = 18
const C = 2 * Math.PI * 52
const GAP = C * 0.012

const arcs = computed(() => {
  let acc = 0
  return props.segments.map((s) => {
    const len = (s.pct / 100) * C
    const dash = Math.max(0, len - GAP)
    const arc = {
      color: s.color,
      dash: `${dash.toFixed(2)} ${(C - dash).toFixed(2)}`,
      offset: (-acc).toFixed(2),
    }
    acc += len
    return arc
  })
})
</script>