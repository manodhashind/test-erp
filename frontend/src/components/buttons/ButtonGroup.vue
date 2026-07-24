<template>
	<div
		ref="containerRef"
		:class="[
			'inline-flex items-center',
			orientation === 'vertical' ? 'flex-col' : 'flex-row',
			isGhost
				? [
						'relative gap-1',
						ghostContainerRadiusClass,
						ghostContainerPaddingClass,
						'bg-slate-100 dark:bg-slate-800/70',
					]
				: rounded
					? `overflow-hidden ${containerRoundedClass}`
					: '',
		]"
		role="radiogroup"
	>
		<!-- Sliding pill — measured against the active button and animated to it,
		     instead of just swapping each button's own background on click. -->
		<div
			v-if="isGhost && indicatorStyle"
			class="pointer-events-none absolute left-0 top-0 z-0 bg-white shadow-sm transition-[transform,width,height] duration-200 ease-out dark:bg-slate-700"
			:class="itemGhostRadiusClass"
			:style="indicatorStyle"
		/>

		<button
			v-for="(item, index) in items"
			:key="item.key ?? index"
			:ref="(el) => setButtonRef(el, index)"
			type="button"
			:class="[
				'relative inline-flex items-center justify-center gap-2 text-sm font-semibold leading-none transition-colors duration-150 focus:z-10 focus:outline-none active:scale-95 disabled:cursor-not-allowed disabled:opacity-50',
				sizeClass,
				itemVariantClass(item, index),
				isGhost
					? itemGhostRadiusClass
					: [borderClass(index), rounded ? '' : itemRadiusClass(index)],
			]"
			:disabled="item.disabled"
			:aria-checked="modelValue === item.value"
			role="radio"
			:tabindex="rovingTabIndex(item, index)"
			@click="handleClick(item)"
			@keydown="handleKeydown($event, index)"
		>
			<Icon v-if="item.icon" :icon="item.icon" :size="iconSize" />
			<span>{{ item.label }}</span>
			<span
				v-if="item.badge"
				class="rounded-full px-1.5 py-0.5 text-[10px] font-bold leading-none"
				:class="
					modelValue === item.value
						? 'bg-on-primary/20 text-on-primary'
						: 'bg-primary/10 text-primary dark:bg-primary/20 dark:text-primary-light'
				"
			>
				{{ item.badge }}
			</span>
		</button>
	</div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue"
import Icon from "@/components/Icon.vue"

const props = defineProps({
	modelValue: { type: [String, Number, null], default: null },
	items: {
		type: Array,
		required: true,
		// [{ label, value, icon, disabled, key, badge }]
	},
	variant: { type: String, default: "outline" },
	size: { type: String, default: "md" },
	orientation: { type: String, default: "horizontal" },
	rounded: { type: Boolean, default: true },
	// Focuses the active (or first enabled) segment as soon as this group
	// mounts — for callers like a modal that opens straight onto this toggle,
	// where the user shouldn't have to click or Tab into it before arrow keys
	// (or immediate Left/Right navigation) work.
	autofocus: { type: Boolean, default: false },
})

const emit = defineEmits(["update:modelValue", "change"])

function selectItem(item) {
	if (item.disabled) return
	emit("update:modelValue", item.value)
	emit("change", item.value)
}

function handleClick(item) {
	selectItem(item)
}

// ── Keyboard navigation (roving tabindex) ──────────────────────────────────────
// Only the active segment (or the first enabled one, before anything is picked)
// sits in the tab order; arrow keys move both focus and the selection between
// segments, per the standard radiogroup keyboard pattern — Left/Right for a
// horizontal toggle, Up/Down for a vertical one.

function rovingTabIndex(item, index) {
	if (item.disabled) return -1
	const activeIndex = props.items.findIndex((i) => i.value === props.modelValue)
	const current = activeIndex === -1 ? props.items.findIndex((i) => !i.disabled) : activeIndex
	return index === current ? 0 : -1
}

function stepIndex(from, delta) {
	const count = props.items.length
	let next = from
	for (let i = 0; i < count; i++) {
		next = (next + delta + count) % count
		if (!props.items[next]?.disabled) return next
	}
	return from
}

function handleKeydown(event, index) {
	const nextKey = props.orientation === "vertical" ? "ArrowDown" : "ArrowRight"
	const prevKey = props.orientation === "vertical" ? "ArrowUp" : "ArrowLeft"
	let targetIndex = null
	if (event.key === nextKey) targetIndex = stepIndex(index, 1)
	else if (event.key === prevKey) targetIndex = stepIndex(index, -1)
	else if (event.key === "Home") targetIndex = stepIndex(-1, 1)
	else if (event.key === "End") targetIndex = stepIndex(props.items.length, -1)
	if (targetIndex === null || targetIndex === index) return

	event.preventDefault()
	selectItem(props.items[targetIndex])
	nextTick(() => buttonRefs.value[targetIndex]?.focus())
}

// ── Sliding pill indicator (ghost variant only) ────────────────────────────────
// Measures the active button's own box and animates the indicator to match,
// rather than each button owning its own background — that's what gives the
// "sliding" motion instead of an instant swap.

const containerRef = ref(null)
const buttonRefs = ref([])
const indicatorStyle = ref(null)

function setButtonRef(el, index) {
	buttonRefs.value[index] = el
}

function updateIndicator() {
	if (!isGhost.value) return
	const activeIndex = props.items.findIndex((item) => item.value === props.modelValue)
	const btn = buttonRefs.value[activeIndex]
	if (!btn) {
		indicatorStyle.value = null
		return
	}
	indicatorStyle.value = {
		width: `${btn.offsetWidth}px`,
		height: `${btn.offsetHeight}px`,
		transform: `translate(${btn.offsetLeft}px, ${btn.offsetTop}px)`,
	}
}

watch([() => props.modelValue, () => props.items], () => nextTick(updateIndicator), {
	immediate: true,
	deep: true,
})

let resizeObserver = null
onMounted(() => {
	nextTick(updateIndicator)
	if (containerRef.value && typeof ResizeObserver !== "undefined") {
		resizeObserver = new ResizeObserver(() => updateIndicator())
		resizeObserver.observe(containerRef.value)
	}
	if (props.autofocus) {
		const activeIndex = props.items.findIndex((i) => i.value === props.modelValue)
		const target = activeIndex === -1 ? props.items.findIndex((i) => !i.disabled) : activeIndex
		nextTick(() => buttonRefs.value[target]?.focus())
	}
})
onBeforeUnmount(() => resizeObserver?.disconnect())

const sizeClass = computed(() => {
	const sizes = {
		xs: "px-2.5 py-1 text-xs",
		sm: "px-3 py-1.5 text-xs",
		md: "px-4 py-2 text-sm",
		lg: "px-5 py-2.5 text-sm",
	}
	return sizes[props.size] || sizes.md
})

const iconSize = computed(() => {
	const sizes = { xs: 12, sm: 13, md: 15, lg: 16 }
	return sizes[props.size] || 15
})

const isSmallSize = computed(() => props.size === "xs" || props.size === "sm")
const containerRoundedClass = computed(() => (isSmallSize.value ? "rounded-lg" : "rounded-xl"))

// Ghost segments float inside their own padded track instead of being butted
// up against each other, so each one is fully rounded rather than only the
// first/last (which is what the bordered/connected variants need).
const isGhost = computed(() => props.variant === "ghost")
const itemGhostRadiusClass = computed(() => (isSmallSize.value ? "rounded-lg" : "rounded-xl"))
// Rounding/padding scale with size — a large rounded-2xl track on a ~28px-tall
// "sm" toggle reads as excess padding since the corner radius eats into the
// already-small height; keep both proportional to the toggle's actual size.
const ghostContainerRadiusClass = computed(() => {
	if (props.size === "xs") return "rounded-lg"
	if (props.size === "sm") return "rounded-xl"
	return "rounded-2xl"
})
const ghostContainerPaddingClass = computed(() => (isSmallSize.value ? "p-1" : "p-1.5"))

function itemVariantClass(item, _index) {
	const isActive = props.modelValue === item.value
	if (isActive) {
		const active = {
			outline: "bg-primary text-on-primary dark:bg-primary dark:text-on-primary z-10",
			secondary: "bg-primary text-on-primary dark:bg-primary dark:text-on-primary z-10",
			// No background here — the sliding pill behind it (indicatorStyle)
			// provides the fill, so only the text color needs to change.
			ghost: "text-primary dark:text-primary-light z-10",
		}
		return active[props.variant] || active.outline
	}
	const inactive = {
		outline:
			"border-outline-variant bg-surface-container text-on-surface hover:bg-surface-container-high dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700",
		secondary:
			"bg-surface-container-high text-on-surface hover:bg-surface-container-highest dark:bg-slate-700 dark:text-slate-200 dark:hover:bg-slate-600",
		ghost:
			"bg-transparent text-slate-600 hover:text-slate-800 dark:text-slate-400 dark:hover:text-slate-200",
	}
	return inactive[props.variant] || inactive.outline
}

function borderClass(index) {
	if (props.orientation === "vertical") {
		if (index === 0) return "border border-outline-variant dark:border-slate-600"
		return "border border-t-0 border-outline-variant dark:border-slate-600"
	}
	if (index === 0) return "border border-outline-variant dark:border-slate-600"
	return "border border-l-0 border-outline-variant dark:border-slate-600"
}

function itemRadiusClass(index) {
	const last = props.items.length - 1
	const small = isSmallSize.value
	if (props.orientation === "vertical") {
		if (index === 0) return small ? "rounded-t-lg" : "rounded-t-xl"
		if (index === last) return small ? "rounded-b-lg" : "rounded-b-xl"
		return ""
	}
	if (index === 0) return small ? "rounded-l-lg" : "rounded-l-xl"
	if (index === last) return small ? "rounded-r-lg" : "rounded-r-xl"
	return ""
}
</script>
