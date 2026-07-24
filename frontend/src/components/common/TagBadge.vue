<template>
	<span
		v-if="label"
		class="inline-flex items-center justify-center rounded-md border border-transparent px-2.5 py-0.5 font-sans text-[10px] font-black uppercase tracking-wider"
		:class="badgeClass"
	>
		{{ label }}
	</span>
	<span
		v-else
		class="text-slate-650 inline-flex items-center justify-center rounded-md border border-slate-200/40 bg-slate-100 px-2.5 py-0.5 font-sans text-[10px] font-black uppercase tracking-wider dark:border-slate-800 dark:bg-slate-800 dark:text-slate-400"
	>
		{{ fallback }}
	</span>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
	label: {
		type: String,
		default: "",
	},
	fallback: {
		type: String,
		default: "—",
	},
})

const COLORS = [
	"bg-blue-50 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300 border border-blue-150/40 dark:border-blue-800/30",
	"bg-purple-50 dark:bg-purple-950/30 text-purple-700 dark:text-purple-300 border border-purple-150/40 dark:border-purple-800/30",
	"bg-orange-50 dark:bg-orange-950/30 text-orange-700 dark:text-orange-300 border border-orange-150/40 dark:border-orange-800/30",
	"bg-emerald-50 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300 border border-emerald-150/40 dark:border-emerald-800/30",
	"bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300 border border-amber-150/40 dark:border-amber-800/30",
	"bg-teal-50 dark:bg-teal-950/30 text-teal-700 dark:text-teal-300 border border-teal-150/40 dark:border-teal-800/30",
	"bg-indigo-50 dark:bg-indigo-950/30 text-indigo-700 dark:text-indigo-300 border border-indigo-150/40 dark:border-indigo-800/30",
	"bg-pink-50 dark:bg-pink-950/30 text-pink-700 dark:text-pink-300 border border-pink-150/40 dark:border-pink-800/30",
	"bg-slate-50 dark:bg-slate-800/50 text-slate-600 dark:text-slate-400 border border-slate-200/40 dark:border-slate-800",
	"bg-red-50 dark:bg-red-950/30 text-red-700 dark:text-red-300 border border-red-150/40 dark:border-red-800/30",
]

const badgeClass = computed(() => {
	const value = props.label || ""
	let hash = 0
	for (let i = 0; i < value.length; i++) {
		hash = value.charCodeAt(i) + ((hash << 5) - hash)
	}
	return COLORS[Math.abs(hash) % COLORS.length]
})
</script>
