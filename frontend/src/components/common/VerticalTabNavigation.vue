<template>
	<div class="flex flex-col gap-2">
		<a
			v-for="tab in tabs"
			:key="tab.id"
			:href="`#${tab.id}`"
			class="group relative flex items-center gap-2 whitespace-nowrap rounded-lg border-l-2 border-transparent px-3 py-2.5 font-sans text-sm transition-all duration-200"
			:class="[
				modelValue === tab.id
					? 'border-primary bg-primary/10 font-extrabold text-primary dark:bg-primary/20 dark:text-on-primary-container'
					: 'font-semibold text-on-surface-variant hover:bg-surface-container hover:text-on-surface dark:text-slate-400 dark:hover:bg-slate-700/60 dark:hover:text-slate-200',
			]"
			@click.prevent="handleTabClick(tab.id)"
		>
			<Icon
				v-if="tab.icon"
				:icon="tab.icon"
				:size="16"
				:class="[
					modelValue === tab.id
						? 'text-primary dark:text-on-primary-container'
						: 'text-on-surface-variant/70 group-hover:text-on-surface dark:text-slate-500',
				]"
			/>

			<span class="min-w-0 flex-1 truncate">{{ tab.label }}</span>

			<span
				v-if="tab.badge"
				class="min-w-[18px] shrink-0 rounded-full px-1.5 py-0.5 text-center text-[10px] font-bold transition-colors duration-200"
				:class="[modelValue === tab.id ? 'bg-primary text-on-primary' : 'bg-red-500 text-white']"
			>
				{{ tab.badge }}
			</span>
		</a>
	</div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, watch } from "vue"
import Icon from "../Icon.vue"

// Same API as TabNavigation.vue (horizontal), just rendered as a vertical
// sidebar list instead of a top bar with an underline indicator.
const props = defineProps({
	tabs: {
		type: Array,
		required: true,
	},
	modelValue: {
		type: String,
		required: true,
	},
	useHashRouting: {
		type: Boolean,
		default: false,
	},
})

const emit = defineEmits(["update:modelValue", "tab-change"])

const currentHashId = () => decodeURIComponent(window.location.hash.replace(/^#/, ""))

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

watch(
	() => props.tabs,
	() => {
		if (props.useHashRouting) syncFromHash()
	},
)
</script>
