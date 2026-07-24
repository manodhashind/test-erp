<template>
	<Button
		:variant="variant"
		:size="size"
		:disabled="disabled || loading"
		:class="customClass"
		@click="$emit('click', $event)"
	>
		<span v-if="loading" class="flex items-center gap-2">
			<svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
				<path
					class="opacity-75"
					fill="currentColor"
					d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
				/>
			</svg>
			<span>{{ loadingLabel || label }}</span>
		</span>
		<span v-else class="flex items-center gap-2">
			<Icon v-if="icon && iconPosition === 'left'" :icon="icon" :size="iconSize" />
			<span v-if="label">{{ label }}</span>
			<slot />
			<Icon v-if="icon && iconPosition === 'right'" :icon="icon" :size="iconSize" />
		</span>
	</Button>
</template>

<script setup>
import Button from "@/components/common/Button.vue"
import Icon from "@/components/Icon.vue"

defineProps({
	label: { type: String, default: "" },
	icon: { type: String, default: null },
	iconPosition: { type: String, default: "left" },
	iconSize: { type: Number, default: 16 },
	variant: { type: String, default: "primary" },
	size: { type: String, default: "md" },
	loading: { type: Boolean, default: false },
	loadingLabel: { type: String, default: "" },
	disabled: { type: Boolean, default: false },
	customClass: { type: String, default: "" },
})

defineEmits(["click"])
</script>
