<template>
	<div :class="[baseClass, variantClass, customClass]">
		<slot />
	</div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
	variant: { type: String, default: "default" }, // default, gradient-primary, inverted, surface
	customClass: { type: String, default: "" },
})

const baseClass = "rounded-xl transition-all duration-300 shadow-md"
const variantClass = computed(() => {
	if (props.variant === "gradient-primary")
		return "bg-gradient-to-br from-primary via-primary/90 to-primary/70 shadow-[0_20px_40px_rgba(var(--color-primary-rgb,103,66,207),0.2)] text-white"
	if (props.variant === "inverted") return "bg-slate-900 text-white shadow-2xl"
	if (props.variant === "surface")
		return "bg-surface-containerest shadow-[0_10px_30px_rgba(0,0,0,0.03)] text-on-surface hover:shadow-lg"
	return "bg-surface-container text-on-surface"
})
</script>
