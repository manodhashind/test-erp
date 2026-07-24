<template>
	<component
		:is="href ? 'a' : 'button'"
		:href="href || undefined"
		:type="href ? undefined : 'button'"
		:class="[
			'inline-flex items-center gap-1.5 font-medium transition-all duration-150 disabled:cursor-not-allowed disabled:opacity-50',
			sizeClass,
			variantClass,
			underline ? 'underline underline-offset-2' : 'no-underline',
		]"
		:disabled="href ? undefined : disabled"
		@click="!href && $emit('click', $event)"
	>
		<Icon v-if="icon && iconPosition === 'left'" :icon="icon" :size="iconSize" />
		<slot>{{ label }}</slot>
		<Icon v-if="icon && iconPosition === 'right'" :icon="icon" :size="iconSize" />
	</component>
</template>

<script setup>
import { computed } from "vue"
import Icon from "@/components/Icon.vue"

const props = defineProps({
	label: { type: String, default: "" },
	icon: { type: String, default: null },
	iconPosition: { type: String, default: "left" },
	href: { type: String, default: null },
	variant: { type: String, default: "primary" },
	size: { type: String, default: "md" },
	underline: { type: Boolean, default: false },
	disabled: { type: Boolean, default: false },
})

defineEmits(["click"])

const sizeClass = computed(() => {
	const sizes = { xs: "text-xs", sm: "text-xs", md: "text-sm", lg: "text-base" }
	return sizes[props.size] || sizes.md
})

const iconSize = computed(() => {
	const sizes = { xs: 12, sm: 13, md: 15, lg: 17 }
	return sizes[props.size] || 15
})

const variantClass = computed(() => {
	const variants = {
		primary: "text-primary hover:text-primary/80 dark:text-primary/90 dark:hover:text-primary",
		secondary:
			"text-on-surface-variant hover:text-on-surface dark:text-slate-400 dark:hover:text-slate-200",
		danger: "text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300",
		muted:
			"text-on-surface-variant/70 hover:text-on-surface-variant dark:text-slate-500 dark:hover:text-slate-400",
	}
	return variants[props.variant] || variants.primary
})
</script>
