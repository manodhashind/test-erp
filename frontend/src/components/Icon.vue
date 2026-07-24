<script setup>
import { Icon } from "@iconify/vue"
import { computed } from "vue"

const props = defineProps({
	icon: { type: String, required: true },
	size: { type: [String, Number], default: 20 },
	color: { type: String, default: "currentColor" },
	background: { type: Boolean, default: false },
	backgroundOpacity: { type: Number, default: 0.1 },
	strokeWidth: { type: [String, Number], default: 0 },
})

const computedSize = computed(() => {
	if (typeof props.size === "number") {
		return `${props.size}px`
	}
	return String(props.size).match(/^\d+$/) ? `${props.size}px` : props.size
})

const backgroundColor = computed(() => {
	if (!props.background) return "transparent"

	if (props.color === "currentColor") {
		return `color-mix(in srgb, currentColor ${props.backgroundOpacity * 100}%, transparent)`
	}

	const hex = props.color.replace("#", "")
	if (hex.length === 3) {
		const r = parseInt(hex[0] + hex[0], 16)
		const g = parseInt(hex[1] + hex[1], 16)
		const b = parseInt(hex[2] + hex[2], 16)
		return `rgba(${r}, ${g}, ${b}, ${props.backgroundOpacity})`
	} else if (hex.length === 6) {
		const r = parseInt(hex.substring(0, 2), 16)
		const g = parseInt(hex.substring(2, 4), 16)
		const b = parseInt(hex.substring(4, 6), 16)
		return `rgba(${r}, ${g}, ${b}, ${props.backgroundOpacity})`
	}
	return "transparent"
})

const containerSize = computed(() => {
	const baseSize = typeof props.size === "number" ? props.size : parseInt(props.size) || 20
	return `${baseSize + 16}px`
})

const strokeAttrs = computed(() => {
	if (!props.strokeWidth || props.strokeWidth === 0) return {}
	return {
		stroke: "currentColor",
		"stroke-width": String(props.strokeWidth),
		"paint-order": "stroke fill",
	}
})
</script>

<template>
	<div
		v-if="background"
		:style="{
			display: 'inline-flex',
			alignItems: 'center',
			justifyContent: 'center',
			width: containerSize,
			height: containerSize,
			borderRadius: '8px',
			backgroundColor: backgroundColor,
			transition: 'background-color 0.3s',
		}"
	>
		<Icon
			:icon="`mdi:${icon}`"
			v-bind="strokeAttrs"
			:style="{
				fontSize: computedSize,
				...(color !== 'currentColor' && { color }),
				transition: 'color 0.3s, font-size 0.3s',
			}"
		/>
	</div>
	<Icon
		v-else
		:icon="`mdi:${icon}`"
		:style="{
			fontSize: computedSize,
			...(color !== 'currentColor' && { color }),
			transition: 'color 0.3s, font-size 0.3s',
		}"
	/>
</template>
