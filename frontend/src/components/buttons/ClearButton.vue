<template>
	<Button variant="secondary" :size="size" :disabled="disabled" @click="$emit('click', $event)">
		<span class="flex items-center gap-2">
			<Icon :icon="icon" :size="16" />
			<span v-if="label">{{ label }}</span>
			<slot />
		</span>
	</Button>
</template>

<script setup>
import Button from "@/components/common/Button.vue"
import Icon from "@/components/Icon.vue"

defineProps({
	label: { type: String, default: "Clear" },
	icon: { type: String, default: "close-circle-outline" },
	size: { type: String, default: "md" },
	disabled: { type: Boolean, default: false },
})

defineEmits(["click"])
</script>
