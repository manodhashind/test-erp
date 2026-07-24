<template>
	<div class="relative flex items-end justify-between gap-4">
		<!-- Shared baseline spanning the whole bar (tabs + trailing actions) -->
		<div
			v-if="!hideTrack"
			class="dark:bg-primary/15 pointer-events-none absolute inset-x-0 bottom-0 h-0.5 bg-primary/20"
		/>
		<div
			class="tab-navigation scrollbar-hide mb-0 min-w-0 flex-1 overflow-x-auto transition-colors duration-300"
		>
			<div class="flex gap-6 sm:gap-8">
				<a
					v-for="tab in tabs"
					:key="tab.id"
					:href="`#${tab.id}`"
					class="tab group relative flex shrink-0 items-center gap-2 whitespace-nowrap border-b-2 border-transparent pb-3 font-sans text-sm transition-all duration-200"
					:class="[
						modelValue === tab.id
							? 'border-primary font-extrabold text-primary'
							: 'font-semibold text-primary/60 hover:text-primary',
					]"
					@click.prevent="handleTabClick(tab.id)"
				>
					<Icon
						v-if="tab.icon"
						:icon="tab.icon"
						:size="16"
						:class="[
							modelValue === tab.id ? 'text-primary' : 'text-primary/60 group-hover:text-primary',
						]"
					/>

					{{ tab.label }}

					<span
						v-if="tab.badge"
						class="min-w-[18px] rounded-full px-1.5 py-0.5 text-center text-[10px] font-bold transition-colors duration-200"
						:class="[
							modelValue === tab.id ? 'bg-primary text-on-primary' : 'bg-red-500 text-white',
						]"
					>
						{{ tab.badge }}
					</span>
				</a>
			</div>
		</div>

		<!-- Trailing actions (e.g. page-level buttons) pinned to the end of the bar -->
		<div v-if="$slots.actions" class="shrink-0 pb-3">
			<slot name="actions" />
		</div>
	</div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, watch } from "vue"

// 1. Define Props
const props = defineProps({
	tabs: {
		type: Array,
		required: true,
	},
	modelValue: {
		type: String,
		required: true,
	},
	// When true, the active tab is mirrored to window.location.hash so tabs are
	// deep-linkable and survive reloads / back-forward. Off by default: only
	// opt-in callers touch the hash, so it never competes with modal hash
	// routing (e.g. #item-N / #tax-N). The hash is read/written ONLY when it
	// matches a tab id — other hashes are left untouched.
	useHashRouting: {
		type: Boolean,
		default: false,
	},
	hideTrack: {
		type: Boolean,
		default: false,
	},
})

// 2. Define Emits
const emit = defineEmits(["update:modelValue", "tab-change"])

// 3. Logic & Methods
const currentHashId = () => decodeURIComponent(window.location.hash.replace(/^#/, ""))

// Adopt the URL hash if (and only if) it points at one of our tabs.
const syncFromHash = () => {
	const id = currentHashId()
	if (!id || id === props.modelValue) return
	if (props.tabs.some((t) => t.id === id)) {
		emit("update:modelValue", id)
		emit("tab-change", id)
	}
}

const handleTabClick = (tabId) => {
	if (props.useHashRouting && currentHashId() !== tabId) {
		window.location.hash = tabId
	}
	emit("update:modelValue", tabId)
	emit("tab-change", tabId)
}

onMounted(() => {
	if (!props.useHashRouting) return
	syncFromHash()
	window.addEventListener("hashchange", syncFromHash)
})

onBeforeUnmount(() => {
	if (props.useHashRouting) window.removeEventListener("hashchange", syncFromHash)
})

// Tabs can arrive after mount (e.g. meta-derived tabs) — re-check the hash once
// the matching tab becomes available.
watch(
	() => props.tabs,
	() => {
		if (props.useHashRouting) syncFromHash()
	},
)
</script>

<style scoped>
.tab-navigation::-webkit-scrollbar {
	height: 4px;
}
.tab-navigation::-webkit-scrollbar-track {
	background: transparent;
}
.tab-navigation::-webkit-scrollbar-thumb {
	background: transparent;
	border-radius: 10px;
}
.tab-navigation:hover::-webkit-scrollbar-thumb {
	background: var(--primary-soft, #d2d1dd);
}
.dark .tab-navigation:hover::-webkit-scrollbar-thumb {
	background: var(--dark-primary-soft, #2d2a42);
}
</style>
