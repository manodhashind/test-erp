<template>
	<button
		:class="[
			'relative flex items-center justify-center gap-2 overflow-hidden rounded-xl px-6 py-3 text-sm font-bold transition-all duration-200',
			variantClass,
			customClass,
			loading ? 'cursor-wait opacity-80' : '',
		]"
		:disabled="loading"
		@click="$emit('click')"
	>
		<span v-if="loading" class="absolute inset-0 flex items-center justify-center bg-inherit">
			<svg
				class="h-5 w-5 animate-spin text-current"
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 24 24"
			>
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
				<path
					class="opacity-75"
					fill="currentColor"
					d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
				/>
			</svg>
		</span>
		<span :class="['flex items-center gap-2', { invisible: loading }]">
			<slot />
		</span>
	</button>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
	variant: { type: String, default: "primary" },
	customClass: { type: String, default: "" },
	loading: { type: Boolean, default: false }, // New loading prop
})
console.log("Button props:", props) // Debugging log
const variantClass = computed(() => {
	const variants = {
		primary:
			"bg-primary text-on-primary hover:bg-[var(--primary-hover)] dark:bg-primary dark:text-[var(--dark-primary)] dark:hover:bg-[var(--dark-primary-container)] shadow-sm",
		secondary: "bg-surface-container text-on-surface hover:bg-surface-container shadow-sm",
		outline: "bg-white border border-outline-variant text-on-surface hover:bg-surface-container",
		danger: "bg-red-500 text-white hover:bg-red-600 shadow-sm",
	}
	return variants[props.variant] || variants.primary
})

defineEmits(["click"])
</script>
