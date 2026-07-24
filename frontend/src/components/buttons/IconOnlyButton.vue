<template>
	<div class="relative inline-flex">
		<button
			ref="buttonRef"
			type="button"
			:class="[
				'relative inline-flex items-center justify-center transition-all duration-150 active:scale-90 disabled:cursor-not-allowed disabled:opacity-50',
				shapeClass,
				sizeClass,
				variantClass,
			]"
			:disabled="disabled"
			:aria-label="tooltip"
			@mouseenter="showTooltip"
			@mouseleave="hovered = false"
			@click="$emit('click', $event)"
		>
			<template v-if="hoverSwap">
				<!-- Outline icon — visible at rest -->
				<span
					:class="hovered ? 'scale-75 opacity-0' : 'scale-100 opacity-100'"
					class="absolute transition-all duration-150"
				>
					<Icon :icon="outlineIcon" :size="computedIconSize" />
				</span>

				<!-- Filled icon — visible on hover -->
				<span
					:class="hovered ? 'scale-100 opacity-100' : 'scale-75 opacity-0'"
					class="absolute transition-all duration-150"
				>
					<Icon :icon="filledIcon" :size="computedIconSize" />
				</span>
			</template>

			<!-- Static icon — no hover swap -->
			<template v-else>
				<span class="absolute">
					<Icon :icon="icon" :size="computedIconSize" />
				</span>
			</template>

			<!-- Invisible spacer keeps button size stable -->
			<Icon :icon="icon" :size="computedIconSize" class="invisible" />
		</button>

		<!-- Tooltip — teleported to body to escape overflow:hidden parents -->
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

const OUTLINE_SUFFIX = "-outline"

const props = defineProps({
	icon: { type: String, required: true },
	tooltip: { type: String, default: "" },
	variant: { type: String, default: "secondary" },
	size: { type: String, default: "md" },
	shape: { type: String, default: "square" }, // square | round
	hoverSwap: { type: Boolean, default: false }, // swap outline↔filled on hover
	disabled: { type: Boolean, default: false },
})

defineEmits(["click"])

const outlineIcon = computed(() =>
	props.icon.endsWith(OUTLINE_SUFFIX) ? props.icon : `${props.icon}${OUTLINE_SUFFIX}`,
)
const filledIcon = computed(() =>
	props.icon.endsWith(OUTLINE_SUFFIX) ? props.icon.slice(0, -OUTLINE_SUFFIX.length) : props.icon,
)

const shapeClass = computed(() => {
	if (props.shape === "round") return "rounded-full"
	const sizes = { xs: "rounded-md", sm: "rounded-md", md: "rounded-lg", lg: "rounded-xl" }
	return sizes[props.size] || "rounded-lg"
})

const sizeClass = computed(() => {
	const sizes = { xs: "h-6 w-6", sm: "h-8 w-8", md: "h-9 w-9", lg: "h-11 w-11" }
	return sizes[props.size] || sizes.md
})

const computedIconSize = computed(() => {
	const sizes = { xs: 14, sm: 16, md: 18, lg: 22 }
	return sizes[props.size] || 18
})

const variantClass = computed(() => {
	const v = {
		primary:
			"bg-primary text-on-primary shadow-sm hover:bg-primary/80 dark:bg-primary dark:text-on-primary dark:hover:bg-primary/80",
		secondary:
			"bg-surface-container-high text-on-surface hover:bg-surface-container-highest dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600",
		outline:
			"border border-outline-variant bg-transparent text-on-surface hover:bg-surface-container-high dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-700",
		ghost:
			"bg-transparent text-on-surface-variant hover:bg-surface-container-high dark:text-slate-400 dark:hover:bg-slate-700/50",
		danger:
			"bg-red-50 text-red-600 hover:bg-red-100 dark:bg-red-900/20 dark:text-red-400 dark:hover:bg-red-900/40",
	}
	return v[props.variant] || v.secondary
})
</script>
