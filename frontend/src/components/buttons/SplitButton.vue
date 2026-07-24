<template>
	<div ref="wrapperRef" class="relative inline-flex">
		<!-- Main action -->
		<button
			type="button"
			:class="[
				'inline-flex items-center gap-2 text-sm font-semibold transition-all duration-200 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50',
				sizeClass,
				roundedLeftClass,
				variantMainClass,
			]"
			:disabled="disabled || loading"
			@click="$emit('action')"
		>
			<svg v-if="loading" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
				<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
				<path
					class="opacity-75"
					fill="currentColor"
					d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
				/>
			</svg>
			<Icon v-else-if="icon" :icon="icon" :size="16" />
			<span>{{ label }}</span>
		</button>

		<!-- Divider -->
		<div :class="['w-px self-stretch', dividerClass]" />

		<!-- Dropdown trigger -->
		<button
			type="button"
			:class="[
				'inline-flex items-center justify-center transition-all duration-200 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50',
				dropdownTriggerSize,
				roundedRightClass,
				variantDropClass,
			]"
			:disabled="disabled"
			:aria-expanded="isOpen"
			@click="isOpen = !isOpen"
		>
			<Icon
				icon="chevron-down"
				:size="14"
				:class="['transition-transform duration-200', isOpen ? 'rotate-180' : '']"
			/>
		</button>

		<!-- Dropdown menu -->
		<Transition
			enter-active-class="transition-all duration-150 ease-out"
			enter-from-class="opacity-0 scale-95 translate-y-1"
			enter-to-class="opacity-100 scale-100 translate-y-0"
			leave-active-class="transition-all duration-100 ease-in"
			leave-from-class="opacity-100 scale-100 translate-y-0"
			leave-to-class="opacity-0 scale-95 translate-y-1"
		>
			<div
				v-if="isOpen"
				class="absolute right-0 top-full z-50 mt-1.5 min-w-[180px] origin-top-right rounded-xl border border-outline-variant bg-surface-container py-1 shadow-lg dark:border-slate-700 dark:bg-slate-800"
			>
				<button
					v-for="item in items"
					:key="item.label"
					type="button"
					:class="[
						'flex w-full items-center gap-2.5 px-3.5 py-2 text-sm transition-colors duration-150',
						item.danger
							? 'text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20'
							: 'text-on-surface hover:bg-surface-container-high dark:text-slate-200 dark:hover:bg-slate-700',
					]"
					@click="handleItemClick(item)"
				>
					<Icon v-if="item.icon" :icon="item.icon" :size="16" />
					<span>{{ item.label }}</span>
				</button>
			</div>
		</Transition>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue"
import Icon from "@/components/Icon.vue"

const props = defineProps({
	label: { type: String, default: "Action" },
	icon: { type: String, default: null },
	variant: { type: String, default: "primary" },
	size: { type: String, default: "md" },
	loading: { type: Boolean, default: false },
	disabled: { type: Boolean, default: false },
	items: {
		type: Array,
		default: () => [],
		// [{ label, icon, action, danger }]
	},
})

const emit = defineEmits(["action"])

const wrapperRef = ref(null)
const isOpen = ref(false)

function handleItemClick(item) {
	isOpen.value = false
	item.action?.()
}

function handleOutsideClick(e) {
	if (wrapperRef.value && !wrapperRef.value.contains(e.target)) {
		isOpen.value = false
	}
}

onMounted(() => document.addEventListener("mousedown", handleOutsideClick))
onBeforeUnmount(() => document.removeEventListener("mousedown", handleOutsideClick))

const sizeClass = computed(() => {
	const sizes = { sm: "px-3 py-1.5 text-xs", md: "px-5 py-2.5 text-sm", lg: "px-6 py-3 text-base" }
	return sizes[props.size] || sizes.md
})

const roundedLeftClass = computed(() => (props.size === "sm" ? "rounded-l-lg" : "rounded-l-xl"))
const roundedRightClass = computed(() => (props.size === "sm" ? "rounded-r-lg" : "rounded-r-xl"))

const dropdownTriggerSize = computed(() => {
	const sizes = { sm: "px-2 py-1.5", md: "px-2.5 py-2.5", lg: "px-3 py-3" }
	return sizes[props.size] || sizes.md
})

const variantMainClass = computed(() => {
	const v = {
		primary:
			"bg-primary text-on-primary hover:bg-primary/90 shadow-sm dark:bg-primary dark:text-on-primary",
		secondary:
			"bg-surface-container-high text-on-surface hover:bg-surface-container-highest dark:bg-slate-700 dark:text-slate-100 dark:hover:bg-slate-600",
		danger:
			"bg-red-600 text-white hover:bg-red-700 shadow-sm dark:bg-red-500 dark:hover:bg-red-600",
	}
	return v[props.variant] || v.primary
})

const variantDropClass = computed(() => {
	const v = {
		primary: "bg-primary text-on-primary hover:bg-primary/80 dark:bg-primary dark:text-on-primary",
		secondary:
			"bg-surface-container-high text-on-surface hover:bg-surface-container-highest dark:bg-slate-700 dark:text-slate-100 dark:hover:bg-slate-600",
		danger: "bg-red-600 text-white hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600",
	}
	return v[props.variant] || v.primary
})

const dividerClass = computed(() => {
	const v = {
		primary: "bg-on-primary/30 dark:bg-on-primary/20",
		secondary: "bg-outline-variant dark:bg-slate-600",
		danger: "bg-red-400 dark:bg-red-400/60",
	}
	return v[props.variant] || v.primary
})
</script>
