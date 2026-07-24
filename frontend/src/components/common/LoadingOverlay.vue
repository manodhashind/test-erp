<template>
	<div
		v-if="active"
		class="z-[1000] flex items-center justify-center bg-white/80 backdrop-blur-sm transition-all duration-300 dark:bg-transparent dark:backdrop-blur-sm"
		:class="[fullscreen ? 'fixed inset-0' : 'rounded-inherit absolute inset-0']"
	>
		<div class="flex flex-col items-center gap-3">
			<div class="h-12 w-12">
				<svg class="h-full w-full animate-spin" viewBox="0 0 50 50">
					<circle
						class="path stroke-primary dark:stroke-primary"
						cx="25"
						cy="25"
						r="20"
						fill="none"
						stroke-width="5"
						stroke-linecap="round"
					/>
				</svg>
			</div>
			<p
				v-if="text"
				class="m-0 font-sans text-sm font-semibold tracking-wide text-primary dark:text-primary"
			>
				{{ text }}
			</p>
		</div>
	</div>
</template>

<script setup>
defineProps({
	active: {
		type: Boolean,
		default: false,
	},
	text: {
		type: String,
		default: "Loading...",
	},
	fullscreen: {
		type: Boolean,
		default: false,
	},
})
</script>

<style scoped>
.path {
	animation: dash 1.5s ease-in-out infinite;
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
