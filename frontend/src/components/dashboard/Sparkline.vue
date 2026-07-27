<template>
	<svg :width="w" :height="h" class="block shrink-0">
		<path
			:d="path"
			fill="none"
			:stroke="color"
			stroke-width="1.8"
			stroke-linecap="round"
			stroke-linejoin="round"
			opacity="0.65"
		/>
		<circle :cx="lastPoint[0]" :cy="lastPoint[1]" r="2.5" :fill="color" />
	</svg>
</template>

<script setup>
import { computed } from "vue"
import { smoothPath } from "../../utils/charts"

const props = defineProps({
	data: { type: Array, required: true },
	color: { type: String, required: true },
	w: { type: Number, default: 72 },
	h: { type: Number, default: 28 },
})

const points = computed(() => {
	const mn = Math.min(...props.data)
	const mx = Math.max(...props.data)
	const rng = mx - mn || 1
	return props.data.map((v, i) => [
		1 + (i * (props.w - 2)) / (props.data.length - 1),
		1 + (1 - (v - mn) / rng) * (props.h - 2),
	])
})

const path = computed(() => smoothPath(points.value))
const lastPoint = computed(() => points.value[points.value.length - 1])
</script>
