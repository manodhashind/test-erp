<template>
	<span
		class="material-symbols-outlined shrink-0"
		:class="[sizeClass, customClass]"
		:data-icon="icon"
		>{{ icon }}</span
	>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
	icon: { type: String, required: true },
	size: { type: String, default: "md" }, // sm, md, lg, xl, 2xl
	customClass: { type: String, default: "" },
})

const sizeClass = computed(() => {
	if (props.size === "sm") return "text-[16px]"
	if (props.size === "lg") return "text-[24px]"
	if (props.size === "xl") return "text-[32px]"
	if (props.size === "2xl") return "text-[48px]"
	return "text-[20px]" // md default
})
</script>
