<template>
	<div class="loader-spinner" :class="sizeClass">
		<svg class="spinner" viewBox="0 0 50 50">
			<circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5" />
		</svg>
	</div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
	size: {
		type: String,
		default: "md",
		validator: (value) => ["xs", "sm", "md", "lg", "xl"].includes(value),
	},
	color: {
		type: String,
		default: "var(--color-primary, #6742CF)",
	},
})

const sizeClass = computed(() => `size-${props.size}`)
</script>

<script>
export default {
	name: "Loader",
}
</script>

<style scoped>
.loader-spinner {
	display: flex; /* Changed from inline-flex */
	align-items: center;
	justify-content: center;
	margin: 0 auto; /* Centers horizontally in a block context */
	width: 100%; /* Takes up full width to allow centering */
}

/* Size variants */
.size-xs {
	width: 16px;
	height: 16px;
}

.size-sm {
	width: 24px;
	height: 24px;
}

.size-md {
	width: 32px;
	height: 32px;
}

.size-lg {
	width: 48px;
	height: 48px;
}

.size-xl {
	width: 64px;
	height: 64px;
}

.spinner {
	animation: rotate 2s linear infinite;
	width: 100%;
	height: 100%;
}

.spinner .path {
	stroke: v-bind(color);
	stroke-linecap: round;
	animation: dash 1.5s ease-in-out infinite;
}

@keyframes rotate {
	100% {
		transform: rotate(360deg);
	}
}

@keyframes dash {
	0% {
		stroke-dasharray: 1, 150;
		stroke-dashoffset: 0;
	}
	50% {
		stroke-dasharray: 90, 150;
		stroke-dashoffset: -35;
	}
	100% {
		stroke-dasharray: 90, 150;
		stroke-dashoffset: -124;
	}
}
</style>
