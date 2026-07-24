<template>
	<div :class="fixed ? positionClass : 'relative inline-flex'">
		<div class="group relative inline-flex">
			<button
				type="button"
				:class="[
					'inline-flex items-center justify-center rounded-full font-semibold shadow-lg transition-all duration-200 hover:-translate-y-0.5 hover:shadow-xl active:translate-y-0 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50',
					sizeClass,
					variantClass,
					extended ? extendedPaddingClass : '',
				]"
				:disabled="disabled || loading"
				:aria-label="tooltip || label"
				@click="$emit('click', $event)"
			>
				<svg
					v-if="loading"
					:class="spinnerSize"
					class="animate-spin"
					viewBox="0 0 24 24"
					fill="none"
				>
					<circle
						class="opacity-25"
						cx="12"
						cy="12"
						r="10"
						stroke="currentColor"
						stroke-width="4"
					/>
					<path
						class="opacity-75"
						fill="currentColor"
						d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
					/>
				</svg>
				<Icon v-else :icon="icon" :size="iconSize" />
				<span v-if="extended && label" class="ml-2 text-sm font-semibold">{{ label }}</span>
			</button>

			<!-- Tooltip (only when not extended) -->
			<div
				v-if="tooltip && !extended"
				class="pointer-events-none absolute bottom-full right-0 z-50 mb-2 whitespace-nowrap rounded-md bg-on-surface px-2.5 py-1 text-xs font-medium text-surface opacity-0 shadow-lg transition-opacity duration-150 group-hover:opacity-100 dark:bg-slate-700 dark:text-slate-100"
			>
				{{ tooltip }}
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue"
import Icon from "@/components/Icon.vue"

const props = defineProps({
	icon: { type: String, default: "plus" },
	label: { type: String, default: "" },
	tooltip: { type: String, default: "" },
	variant: { type: String, default: "primary" },
	size: { type: String, default: "md" },
	fixed: { type: Boolean, default: false },
	position: { type: String, default: "bottom-right" }, // bottom-right | bottom-left | top-right | top-left
	extended: { type: Boolean, default: false },
	loading: { type: Boolean, default: false },
	disabled: { type: Boolean, default: false },
})

defineEmits(["click"])

const positionClass = computed(() => {
	const positions = {
		"bottom-right": "fixed bottom-6 right-6 z-40",
		"bottom-left": "fixed bottom-6 left-6 z-40",
		"top-right": "fixed top-6 right-6 z-40",
		"top-left": "fixed top-6 left-6 z-40",
	}
	return positions[props.position] || positions["bottom-right"]
})

const sizeClass = computed(() => {
	if (props.extended) return ""
	const sizes = { sm: "h-10 w-10", md: "h-14 w-14", lg: "h-16 w-16" }
	return sizes[props.size] || sizes.md
})

const extendedPaddingClass = computed(() => {
	const sizes = { sm: "px-4 py-2", md: "px-6 py-3.5", lg: "px-8 py-4" }
	return sizes[props.size] || sizes.md
})

const iconSize = computed(() => {
	const sizes = { sm: 18, md: 24, lg: 28 }
	return sizes[props.size] || 24
})

const spinnerSize = computed(() => {
	const sizes = { sm: "h-4 w-4", md: "h-6 w-6", lg: "h-7 w-7" }
	return sizes[props.size] || "h-6 w-6"
})

const variantClass = computed(() => {
	const variants = {
		primary:
			"bg-primary text-on-primary hover:bg-primary/90 dark:bg-primary dark:text-on-primary shadow-primary/25",
		secondary:
			"bg-surface-container text-on-surface hover:bg-surface-container-high dark:bg-slate-700 dark:text-slate-100 dark:hover:bg-slate-600 shadow-slate-300/50 dark:shadow-slate-900/50",
		success:
			"bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600 shadow-emerald-500/25",
		danger:
			"bg-red-600 text-white hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 shadow-red-500/25",
	}
	return variants[props.variant] || variants.primary
})
</script>
