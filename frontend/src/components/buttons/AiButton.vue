<template>
	<button
		type="button"
		:disabled="disabled || loading"
		:class="[rootClass, sizeClass]"
		@click="$emit('click', $event)"
	>
		<span v-if="variant === 'gradient'" class="ai-shimmer-sweep" aria-hidden="true" />

		<span v-if="icon || loading" class="relative flex shrink-0 items-center justify-center">
			<Icon v-if="loading" icon="loading" :size="iconSize" class="relative animate-spin" />
			<AiWandIcon v-else-if="icon === 'ai-wand' && iconPosition === 'left'" class="relative" />
			<Icon
				v-else-if="icon && iconPosition === 'left'"
				:icon="icon"
				:size="iconSize"
				class="relative"
			/>
		</span>

		<span v-if="label || $slots.default" class="relative">
			<slot>{{ loading ? loadingLabel || label : label }}</slot>
		</span>

		<AiWandIcon
			v-if="!loading && icon === 'ai-wand' && iconPosition === 'right'"
			class="relative shrink-0"
		/>
		<Icon
			v-else-if="!loading && icon && iconPosition === 'right'"
			:icon="icon"
			:size="iconSize"
			class="relative shrink-0"
		/>
	</button>
</template>

<script setup>
import { computed } from "vue"
import Icon from "@/components/Icon.vue"
import AiWandIcon from "./AiWandIcon.vue"

const props = defineProps({
	label: { type: String, default: "" },
	icon: { type: String, default: "ai-wand" },
	iconPosition: { type: String, default: "left" },
	iconSize: { type: Number, default: 15 },
	/** gradient | outline | ghost */
	variant: { type: String, default: "gradient" },
	size: { type: String, default: "md" },
	loading: { type: Boolean, default: false },
	loadingLabel: { type: String, default: "" },
	disabled: { type: Boolean, default: false },
})

defineEmits(["click"])

const rootClass = computed(() => {
	const base =
		"relative inline-flex items-center justify-center overflow-hidden font-sans transition-all duration-200 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50 disabled:active:scale-100"
	const variants = {
		gradient: "ai-gradient-btn text-white hover:-translate-y-px",
		outline:
			"ai-outline-btn border border-violet-400/70 bg-transparent hover:bg-violet-50/60 hover:-translate-y-px dark:border-violet-500/50 dark:hover:bg-violet-900/10",
		ghost: "ai-ghost-btn bg-transparent hover:bg-violet-50/60 dark:hover:bg-violet-900/10",
	}
	return `${base} ${variants[props.variant] ?? variants.gradient}`
})

const sizeClass = computed(() => {
	const sizes = {
		xs: "gap-1 px-2.5 py-1 text-xs font-bold rounded-lg",
		sm: "gap-1.5 px-3 py-1.5 text-xs font-bold rounded-xl",
		md: "gap-2 h-9 px-4 text-[13px] font-bold rounded-[9px]",
		lg: "gap-2 px-5 py-2.5 text-base font-bold rounded-2xl",
	}
	return sizes[props.size] ?? sizes.md
})
</script>

<style scoped>
.ai-gradient-btn {
	background: linear-gradient(110deg, #c026d3 0%, #7c3aed 35%, #4f46e5 62%, #0ea5e9 100%);
	box-shadow:
		0 0 0 1px rgb(124 58 237 / 40%),
		0 2px 12px rgb(124 58 237 / 55%);
}

.ai-gradient-btn:not(:disabled):hover {
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

.ai-outline-btn {
	background: transparent;
}

.ai-outline-btn span,
.ai-outline-btn :deep(.iconify) {
	background: linear-gradient(90deg, #7c3aed, #6366f1);
	-webkit-text-fill-color: transparent;
	background-clip: text;
}

.ai-ghost-btn span,
.ai-ghost-btn :deep(.iconify) {
	background: linear-gradient(90deg, #7c3aed, #6366f1);
	-webkit-text-fill-color: transparent;
	background-clip: text;
}
</style>
