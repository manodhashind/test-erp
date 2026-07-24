<template>
	<div
		:class="[
			'ai-icon-badge relative flex shrink-0 items-center justify-center overflow-hidden text-white',
			rounded,
			sizeClass,
		]"
	>
		<span class="ai-shimmer-sweep" aria-hidden="true" />
		<AiWandIcon :size="iconSize" class="relative" />
	</div>
</template>

<script setup>
import { computed } from "vue"
import AiWandIcon from "./AiWandIcon.vue"

const props = defineProps({
	/** xs | sm | md | lg */
	size: { type: String, default: "md" },
	rounded: { type: String, default: "rounded-xl" },
})

const SIZES = {
	xs: { box: "h-7 w-7", icon: 14 },
	sm: { box: "h-8 w-8", icon: 16 },
	md: { box: "h-9 w-9", icon: 20 },
	lg: { box: "h-11 w-11", icon: 24 },
}

const sizeClass = computed(() => (SIZES[props.size] ?? SIZES.md).box)
const iconSize = computed(() => (SIZES[props.size] ?? SIZES.md).icon)
</script>

<style scoped>
.ai-icon-badge {
	background: linear-gradient(110deg, #c026d3 0%, #7c3aed 35%, #4f46e5 62%, #0ea5e9 100%);
	box-shadow:
		0 0 0 1px rgb(124 58 237 / 40%),
		0 2px 12px rgb(124 58 237 / 55%);
}

.ai-shimmer-sweep {
	position: absolute;
	inset: 0;
	background: linear-gradient(
		105deg,
		transparent 30%,
		rgb(255 255 255 / 22%) 50%,
		transparent 70%
	);
	background-size: 200% 100%;
	animation: ai-shimmer 2.4s ease-in-out infinite;
	pointer-events: none;
}

@keyframes ai-shimmer {
	0% {
		background-position: 200% 0;
	}
	100% {
		background-position: -200% 0;
	}
}
</style>
