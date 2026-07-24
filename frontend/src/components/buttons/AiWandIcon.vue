<template>
	<svg class="ai-wand-icon" :width="size" :height="size" viewBox="0 0 24 24" fill="none">
		<!-- wand body -->
		<path d="M15 4l5 5-9.5 9.5-5-5z" fill="#fff" opacity="0.9" />
		<!-- wand tip -->
		<path d="M3 21l3.5-3.5" stroke="#fff" stroke-width="2" stroke-linecap="round" />
		<!-- large sparkle -->
		<path d="M18 2l.7 2L21 5l-2.3.7L18 8l-.7-2.3L15 5l2.3-.7z" fill="#fff" />
		<!-- small sparkle -->
		<path d="M8 3l.5 1.4 1.5.6-1.5.6L8 7l-.5-1.4L6 5l1.5-.6z" fill="rgba(255,255,255,0.75)" />
	</svg>
</template>

<script setup>
defineProps({
	size: { type: [Number, String], default: 16 },
})
</script>

<style scoped>
.ai-wand-icon {
	animation: ai-wand-pulse 2.4s ease-in-out infinite;
}

@keyframes ai-wand-pulse {
	0%,
	100% {
		filter: drop-shadow(0 0 3px rgb(255 255 255 / 50%));
	}
	50% {
		filter: drop-shadow(0 0 8px rgb(255 255 255 / 95%));
	}
}
</style>
