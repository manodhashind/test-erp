<template>
	<div ref="wrapperRef" class="relative inline-flex">
		<button
			type="button"
			:class="[
				'inline-flex items-center gap-2 font-semibold transition-all duration-150 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50',
				sizeClass,
				variantClass,
				isOpen ? ringClass : '',
			]"
			:disabled="disabled"
			:aria-haspopup="true"
			:aria-expanded="isOpen"
			@click="isOpen = !isOpen"
		>
			<Icon v-if="icon" :icon="icon" :size="iconSize" />
			<span>{{ label }}</span>
			<Icon
				icon="chevron-down"
				:size="12"
				:class="['ml-0.5 transition-transform duration-200', isOpen ? 'rotate-180' : '']"
			/>
		</button>

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
				:class="[
					'absolute z-50 mt-1.5 min-w-[180px] origin-top rounded-xl border border-outline-variant bg-surface-container py-1.5 shadow-lg dark:border-slate-700 dark:bg-slate-800',
					alignClass,
				]"
				style="top: 100%"
			>
				<template v-for="(item, index) in items" :key="item.key ?? index">
					<!-- Divider -->
					<div
						v-if="item.divider"
						class="my-1 border-t border-outline-variant dark:border-slate-700"
					/>

					<!-- Item -->
					<button
						v-else
						type="button"
						:disabled="item.disabled"
						:class="[
							'flex w-full items-center gap-2.5 px-3.5 py-2 text-sm transition-colors duration-100 disabled:cursor-not-allowed disabled:opacity-40',
							item.danger
								? 'text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20'
								: 'text-on-surface hover:bg-surface-container-high dark:text-slate-200 dark:hover:bg-slate-700',
						]"
						@click="handleItem(item)"
					>
						<Icon v-if="item.icon" :icon="item.icon" :size="16" />
						<span class="flex-1 text-left">{{ item.label }}</span>
						<span
							v-if="item.badge"
							class="rounded-full bg-primary/10 px-1.5 py-0.5 text-xs font-medium text-primary dark:bg-primary/20"
						>
							{{ item.badge }}
						</span>
					</button>
				</template>
			</div>
		</Transition>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue"
import Icon from "@/components/Icon.vue"

const props = defineProps({
	label: { type: String, default: "Options" },
	icon: { type: String, default: null },
	variant: { type: String, default: "secondary" },
	size: { type: String, default: "md" },
	align: { type: String, default: "left" }, // left | right
	disabled: { type: Boolean, default: false },
	items: {
		type: Array,
		default: () => [],
		// [{ label, icon, action, danger, disabled, badge, key }]
		// { divider: true } inserts a separator
	},
})

const emit = defineEmits(["open", "close"])

const wrapperRef = ref(null)
const isOpen = ref(false)

function handleItem(item) {
	if (item.disabled) return
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

const alignClass = computed(() => (props.align === "right" ? "right-0" : "left-0"))

const sizeClass = computed(() => {
	const sizes = {
		xs: "px-2.5 py-1.5 text-xs rounded-lg",
		sm: "px-3 py-1.5 text-xs rounded-lg",
		md: "px-4 py-2.5 text-sm rounded-xl",
		lg: "px-5 py-3 text-base rounded-xl",
	}
	return sizes[props.size] || sizes.md
})

const iconSize = computed(() => ({ xs: 13, sm: 14, md: 16, lg: 18 })[props.size] ?? 16)

const variantClass = computed(() => {
	const v = {
		primary:
			"bg-primary text-on-primary shadow-sm hover:bg-primary/90 dark:bg-primary dark:text-on-primary",
		secondary:
			"bg-surface-container-high text-on-surface hover:bg-surface-container-highest dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600",
		outline:
			"border border-outline-variant bg-transparent text-on-surface hover:bg-surface-container-high dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-700",
		ghost:
			"bg-transparent text-on-surface-variant hover:bg-surface-container-high dark:text-slate-400 dark:hover:bg-slate-700/50",
	}
	return v[props.variant] || v.secondary
})

// Subtle ring when open to show active state
const ringClass = computed(() => {
	const v = {
		primary: "ring-2 ring-primary/40",
		secondary: "ring-2 ring-outline-variant dark:ring-slate-500",
		outline: "ring-2 ring-outline-variant dark:ring-slate-500",
		ghost: "ring-2 ring-outline-variant dark:ring-slate-500",
	}
	return v[props.variant] || v.secondary
})
</script>
