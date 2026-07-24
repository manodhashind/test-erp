<template>
	<button
		:type="type"
		:class="[
			'inline-flex items-center justify-center gap-2 font-sans font-semibold outline-none transition-all duration-200 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50 disabled:active:scale-100',
			variantClasses,
			sizeClasses,
		]"
		:disabled="disabled"
		@click="$emit('click', $event)"
	>
		<div
			v-if="icon"
			class="h-4 w-4 bg-current"
			:style="{
				maskImage: `url(${icon})`,
				maskRepeat: 'no-repeat',
				maskSize: 'contain',
				maskPosition: 'center',
				webkitMaskImage: `url(${icon})`,
				webkitMaskRepeat: 'no-repeat',
				webkitMaskSize: 'contain',
				webkitMaskPosition: 'center',
			}"
		/>
		<slot />
	</button>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
	variant: {
		type: String,
		default: "primary",
		validator: (value) =>
			["primary", "secondary", "danger", "ghost", "success", "warning"].includes(value),
	},
	size: {
		type: String,
		default: "md",
		validator: (value) => ["xs", "sm", "md", "lg"].includes(value),
	},
	/** HTML button type. Defaults to "button" so Button never accidentally submits a <form>. */
	type: {
		type: String,
		default: "button",
		validator: (value) => ["button", "submit", "reset"].includes(value),
	},
	disabled: {
		type: Boolean,
		default: false,
	},
	icon: {
		type: String,
		default: null,
	},
})

defineEmits(["click"])

const variantClasses = computed(() => {
	const base = {
		primary:
			"bg-primary text-on-primary hover:bg-primary/90 dark:bg-primary dark:text-on-primary dark:hover:bg-primary shadow-sm hover:shadow-primary/30 hover:-translate-y-0.5",
		secondary:
			"bg-[#e0e3e5] text-[#191c1e] hover:bg-slate-300 dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600",
		danger:
			"bg-red-600 text-white hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 shadow-sm hover:shadow-red-500/30 hover:-translate-y-0.5",
		ghost:
			"bg-transparent border border-primary text-primary hover:bg-primary/10 dark:border-primary-light dark:text-primary-light dark:hover:bg-primary/20",
		success:
			"bg-emerald-600 text-white hover:bg-emerald-700 dark:bg-emerald-500 dark:hover:bg-emerald-600 shadow-sm hover:shadow-emerald-500/30 hover:-translate-y-0.5",
		warning:
			"bg-amber-500 text-white hover:bg-amber-600 dark:bg-amber-600 dark:hover:bg-amber-500 shadow-sm hover:shadow-amber-500/30 hover:-translate-y-0.5",
	}
	return base[props.variant]
})

const sizeClasses = computed(() => {
	const sizes = {
		xs: "p-1.5 rounded-lg",
		sm: "px-2.5 py-1.5 text-xs rounded-lg",
		md: "px-5 py-2.5 text-sm rounded-xl",
		lg: "px-6 py-3 text-base rounded-xl",
	}
	return sizes[props.size]
})
</script>
