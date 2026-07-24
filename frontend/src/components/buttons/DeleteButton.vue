<template>
	<div class="relative inline-flex">
		<Button variant="danger" :size="size" :disabled="disabled || loading" @click="handleClick">
			<span v-if="loading" class="flex items-center gap-2">
				<svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
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
				<span>Deleting...</span>
			</span>
			<span v-else-if="confirmStep" class="flex items-center gap-2">
				<Icon icon="alert" :size="16" />
				<span>{{ confirmLabel }}</span>
			</span>
			<span v-else class="flex items-center gap-2">
				<Icon icon="trash-can-outline" :size="16" />
				<span>{{ label }}</span>
			</span>
		</Button>

		<!-- Cancel confirm -->
		<button
			v-if="confirmStep && requireConfirm"
			type="button"
			class="ml-1.5 rounded-xl px-2 py-1 text-xs font-medium text-on-surface-variant hover:bg-surface-container-high dark:text-slate-400 dark:hover:bg-slate-700"
			@click="confirmStep = false"
		>
			Cancel
		</button>
	</div>
</template>

<script setup>
import { ref } from "vue"
import Button from "@/components/common/Button.vue"
import Icon from "@/components/Icon.vue"

const props = defineProps({
	label: { type: String, default: "Delete" },
	confirmLabel: { type: String, default: "Confirm Delete?" },
	requireConfirm: { type: Boolean, default: true },
	size: { type: String, default: "md" },
	loading: { type: Boolean, default: false },
	disabled: { type: Boolean, default: false },
})

const emit = defineEmits(["delete"])

const confirmStep = ref(false)

function handleClick() {
	if (props.requireConfirm && !confirmStep.value) {
		confirmStep.value = true
		return
	}
	confirmStep.value = false
	emit("delete")
}
</script>
