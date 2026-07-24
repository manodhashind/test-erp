<template>
	<div class="relative inline-flex">
		<button
			ref="buttonRef"
			type="button"
			:class="[
				'relative inline-flex items-center justify-center overflow-hidden transition-all duration-200 active:scale-90 disabled:cursor-not-allowed disabled:opacity-50 disabled:active:scale-100',
				shapeClass,
				sizeClass,
			]"
			:disabled="disabled || loading"
			:aria-label="tooltip || icon"
			@mouseenter="showTooltip"
			@mouseleave="hovered = false"
			@click="$emit('click', $event)"
		>
			<span class="ai-shimmer-sweep" aria-hidden="true" />

			<span class="relative flex items-center justify-center">
				<Icon
					v-if="loading"
					icon="loading"
					:size="computedIconSize"
					class="animate-spin text-white"
				/>
				<AiWandIcon v-else-if="icon === 'ai-wand'" :size="computedIconSize" />
				<Icon v-else :icon="icon" :size="computedIconSize" class="text-white" />
			</span>
		</button>

		<!-- Tooltip -->
		<Teleport to="body">
			<div
				v-if="tooltip && hovered"
				class="pointer-events-none fixed z-[9999] -translate-x-1/2 -translate-y-full whitespace-nowrap rounded-md bg-on-surface px-2.5 py-1 text-xs font-medium text-surface shadow-lg dark:bg-slate-700 dark:text-slate-100"
				:style="tooltipStyle"
			>
				{{ tooltip }}
				<div
					class="absolute left-1/2 top-full -translate-x-1/2 border-4 border-transparent border-t-on-surface dark:border-t-slate-700"
				/>
			</div>
		</Teleport>
	</div>
</template>

<script setup>
import { ref, computed } from "vue"
import Icon from "@/components/Icon.vue"
import AiWandIcon from "./AiWandIcon.vue"

const hovered = ref(false)
const buttonRef = ref(null)
const tooltipStyle = ref({})

const showTooltip = () => {
	hovered.value = true
	if (buttonRef.value) {
		const rect = buttonRef.value.getBoundingClientRect()
		tooltipStyle.value = {
			left: `${rect.left + rect.width / 2}px`,
			top: `${rect.top - 6}px`,
		}
	}
}

const props = defineProps({
	icon: { type: String, default: "ai-wand" },
	tooltip: { type: String, default: "" },
	size: { type: String, default: "md" },
	shape: { type: String, default: "square" }, // square | round
	loading: { type: Boolean, default: false },
	disabled: { type: Boolean, default: false },
})

defineEmits(["click"])

const shapeClass = computed(() => {
	if (props.shape === "round") return "rounded-full"
	const map = { xs: "rounded-md", sm: "rounded-lg", md: "rounded-[9px]", lg: "rounded-xl" }
	return map[props.size] || "rounded-lg"
})

const sizeClass = computed(() => {
	const map = { xs: "h-6 w-6", sm: "h-8 w-8", md: "h-9 w-9", lg: "h-11 w-11" }
	return map[props.size] || map.md
})

const computedIconSize = computed(() => {
	const map = { xs: 13, sm: 15, md: 17, lg: 21 }
	return map[props.size] || 17
})
</script>

<style scoped>
button {
	background: linear-gradient(110deg, #c026d3 0%, #7c3aed 35%, #4f46e5 62%, #0ea5e9 100%);
	box-shadow:
		0 0 0 1px rgb(124 58 237 / 40%),
		0 2px 12px rgb(124 58 237 / 55%);
}

button:not(:disabled):hover {
	filter: brightness(1.08);
	transform: translateY(-1px);
	box-shadow:
		0 0 0 1px rgb(124 58 237 / 50%),
		0 4px 16px rgb(124 58 237 / 65%);
}

.ai-shimmer-sweep {
	position: absolute;
	inset: 0;
	background: linear-gradient(
		105deg,
		transparent 30%,
		rgb(255 255 255 / 22%) 50%,
		transparent 70%
	);
	background-size: 200% 100%;
	animation: ai-shimmer 2.4s ease-in-out infinite;
	pointer-events: none;
}

@keyframes ai-shimmer {
	0% {
		background-position: 200% 0;
	}
	100% {
		background-position: -200% 0;
	}
}
</style>
