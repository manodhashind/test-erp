<template>
	<button
		type="button"
		:class="[
			'inline-flex items-center justify-center gap-2 font-semibold transition-all duration-200 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50',
			sizeClass,
			variantClass,
		]"
		:disabled="disabled || loading"
		@click="$emit('click', $event)"
	>
		<svg v-if="loading" class="animate-spin" :class="spinnerSize" viewBox="0 0 24 24" fill="none">
			<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
			<path
				class="opacity-75"
				fill="currentColor"
				d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
			/>
		</svg>
		<Icon v-else-if="icon && iconPosition === 'left'" :icon="icon" :size="iconSize" />
		<span>
			<slot>{{ label }}</slot>
		</span>
		<Icon v-if="!loading && icon && iconPosition === 'right'" :icon="icon" :size="iconSize" />
	</button>
</template>

<script setup>
import { computed } from "vue"
import Icon from "@/components/Icon.vue"

const props = defineProps({
	label: { type: String, default: "" },
	icon: { type: String, default: null },
	iconPosition: { type: String, default: "left" },
	variant: { type: String, default: "primary" },
	size: { type: String, default: "md" },
	loading: { type: Boolean, default: false },
	disabled: { type: Boolean, default: false },
	fullWidth: { type: Boolean, default: false },
})

defineEmits(["click"])

const sizeClass = computed(() => {
	const base = props.fullWidth ? "w-full" : ""
	const sizes = {
		xs: `${base} px-3 py-1.5 text-xs rounded-lg`,
		sm: `${base} px-4 py-2 text-sm rounded-lg`,
		md: `${base} px-6 py-2.5 text-sm rounded-xl`,
		lg: `${base} px-8 py-3 text-base rounded-xl`,
		xl: `${base} px-10 py-4 text-lg rounded-xl`,
	}
	return sizes[props.size] || sizes.md
})

const iconSize = computed(() => {
	const sizes = { xs: 12, sm: 14, md: 16, lg: 18, xl: 20 }
	return sizes[props.size] || 16
})

const spinnerSize = computed(() => {
	const sizes = { xs: "h-3 w-3", sm: "h-3.5 w-3.5", md: "h-4 w-4", lg: "h-5 w-5", xl: "h-6 w-6" }
	return sizes[props.size] || "h-4 w-4"
})

const variantClass = computed(() => {
	const variants = {
		primary:
			"bg-primary text-on-primary hover:bg-primary/90 hover:-translate-y-0.5 shadow-sm hover:shadow-primary/30 dark:bg-primary dark:text-on-primary",
		secondary:
			"bg-surface-container-high text-on-surface hover:bg-surface-container-highest dark:bg-slate-700 dark:text-slate-100 dark:hover:bg-slate-600",
		outline:
			"border border-primary text-primary bg-transparent hover:bg-primary/5 dark:border-primary/70 dark:text-primary/90",
		danger:
			"bg-red-600 text-white hover:bg-red-700 hover:-translate-y-0.5 shadow-sm hover:shadow-red-500/30 dark:bg-red-500 dark:hover:bg-red-600",
		success:
			"bg-emerald-600 text-white hover:bg-emerald-700 hover:-translate-y-0.5 shadow-sm dark:bg-emerald-500 dark:hover:bg-emerald-600",
		warning:
			"bg-amber-500 text-white hover:bg-amber-600 hover:-translate-y-0.5 shadow-sm dark:bg-amber-500 dark:hover:bg-amber-400",
	}
	return variants[props.variant] || variants.primary
})
</script>
