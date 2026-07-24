<template>
	<button
		type="button"
		:class="[
			'inline-flex items-center gap-2 border text-sm font-semibold transition-all duration-200 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50',
			sizeClass,
			modelValue ? activeClass : inactiveClass,
		]"
		:disabled="disabled"
		:aria-pressed="modelValue"
		@click="toggle"
	>
		<Icon v-if="modelValue ? onIcon : offIcon" :icon="modelValue ? onIcon : offIcon" :size="16" />
		<span>{{ modelValue ? onLabel : offLabel }}</span>
	</button>
</template>

<script setup>
import { computed } from "vue"
import Icon from "@/components/Icon.vue"

const props = defineProps({
	modelValue: { type: Boolean, default: false },
	onLabel: { type: String, default: "On" },
	offLabel: { type: String, default: "Off" },
	onIcon: { type: String, default: "toggle-switch-outline" },
	offIcon: { type: String, default: "toggle-switch-off-outline" },
	size: { type: String, default: "md" },
	activeVariant: { type: String, default: "primary" },
	disabled: { type: Boolean, default: false },
})

const emit = defineEmits(["update:modelValue", "change"])

function toggle() {
	emit("update:modelValue", !props.modelValue)
	emit("change", !props.modelValue)
}

const sizeClass = computed(() => {
	const sizes = {
		sm: "px-3 py-1.5 text-xs rounded-lg",
		md: "px-4 py-2 text-sm rounded-xl",
		lg: "px-5 py-2.5 text-base rounded-xl",
	}
	return sizes[props.size] || sizes.md
})

const activeClass = computed(() => {
	const variants = {
		primary:
			"border-primary bg-primary text-on-primary dark:border-primary dark:bg-primary dark:text-on-primary shadow-sm shadow-primary/20",
		success:
			"border-emerald-600 bg-emerald-600 text-white dark:border-emerald-500 dark:bg-emerald-500",
		warning: "border-amber-500 bg-amber-500 text-white dark:border-amber-400 dark:bg-amber-400",
	}
	return variants[props.activeVariant] || variants.primary
})

const inactiveClass =
	"border-outline-variant bg-surface-container text-on-surface-variant hover:bg-surface-container-high dark:border-slate-600 dark:bg-slate-800 dark:text-slate-400 dark:hover:bg-slate-700"
</script>
