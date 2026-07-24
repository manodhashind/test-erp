<template>
	<!-- Fields variant: section cards with label/value grid (default) -->
	<div v-if="variant === 'fields'" class="flex flex-col gap-4">
		<div
			v-for="s in sections"
			:key="s"
			class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-800"
		>
			<!-- Section header -->
			<div
				class="flex items-center gap-2.5 border-b border-slate-200 bg-slate-50 px-5 py-3.5 dark:border-slate-700 dark:bg-slate-900/40"
			>
				<div class="sk h-5 w-5 rounded-md bg-slate-200 dark:bg-slate-700" />
				<div
					class="sk h-4 rounded-full bg-slate-200 dark:bg-slate-700"
					:style="{ width: sectionTitleWidths[(s - 1) % sectionTitleWidths.length] }"
				/>
			</div>
			<!-- Field grid -->
			<div class="grid grid-cols-1 gap-x-8 gap-y-5 p-5 sm:grid-cols-2">
				<div
					v-for="f in fieldCounts[(s - 1) % fieldCounts.length]"
					:key="f"
					class="flex flex-col gap-1.5"
				>
					<div class="sk h-3 w-14 rounded-full bg-slate-100 dark:bg-slate-800" />
					<div
						class="sk h-4 rounded-full bg-slate-200 dark:bg-slate-700"
						:style="{ width: fieldWidths[(s * 5 + f) % fieldWidths.length] }"
					/>
				</div>
			</div>
		</div>
	</div>

	<!-- Table / list variant: rows with icon + text + meta -->
	<div
		v-else-if="variant === 'list'"
		class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-800"
	>
		<div
			class="flex items-center gap-2.5 border-b border-slate-200 bg-slate-50 px-5 py-3.5 dark:border-slate-700 dark:bg-slate-900/40"
		>
			<div class="sk h-4 w-32 rounded-full bg-slate-200 dark:bg-slate-700" />
		</div>
		<div class="divide-y divide-slate-100 dark:divide-slate-700/60">
			<div
				v-for="row in rows"
				:key="row"
				class="flex items-center gap-4 px-5 py-3.5"
				:style="{ opacity: 1 - ((row - 1) / rows) * 0.3 }"
			>
				<div class="sk h-8 w-8 shrink-0 rounded-lg bg-slate-100 dark:bg-slate-800" />
				<div class="flex flex-1 flex-col gap-1.5">
					<div
						class="sk h-3.5 rounded-full bg-slate-200 dark:bg-slate-700"
						:style="{ width: listTitleWidths[(row - 1) % listTitleWidths.length] }"
					/>
					<div class="sk h-3 w-24 rounded-full bg-slate-100 dark:bg-slate-800" />
				</div>
				<div class="sk h-3.5 w-16 rounded-full bg-slate-100 dark:bg-slate-800" />
			</div>
		</div>
	</div>

	<!-- Activity variant: timeline rows -->
	<div
		v-else-if="variant === 'activity'"
		class="max-w-[800px] overflow-hidden rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-700 dark:bg-slate-800"
	>
		<!-- Header -->
		<div class="mb-4 flex items-center gap-2.5">
			<div class="sk h-8 w-8 rounded-lg bg-slate-200 dark:bg-slate-700" />
			<div class="sk h-4 w-20 rounded-full bg-slate-200 dark:bg-slate-700" />
		</div>
		<!-- Timeline entries -->
		<div class="flex flex-col gap-4">
			<div
				v-for="row in rows"
				:key="row"
				class="flex items-start gap-3 border-b border-slate-100 pb-4 last:border-0 last:pb-0 dark:border-slate-700"
			>
				<div class="sk mt-0.5 h-7 w-7 shrink-0 rounded-full bg-slate-100 dark:bg-slate-800" />
				<div class="flex flex-1 flex-col gap-1.5">
					<div
						class="sk h-3.5 rounded-full bg-slate-200 dark:bg-slate-700"
						:style="{ width: activityWidths[(row - 1) % activityWidths.length] }"
					/>
					<div class="sk h-3 w-28 rounded-full bg-slate-100 dark:bg-slate-800" />
				</div>
				<div class="sk h-3 w-24 shrink-0 rounded-full bg-slate-100 dark:bg-slate-800" />
			</div>
		</div>
	</div>
</template>

<script setup>
defineProps({
	/** 'fields' | 'list' | 'activity' */
	variant: {
		type: String,
		default: "fields",
	},
	/** Number of section cards (fields variant) */
	sections: {
		type: Number,
		default: 3,
	},
	/** Number of rows (list / activity variants) */
	rows: {
		type: Number,
		default: 6,
	},
})

const sectionTitleWidths = ["80px", "120px", "96px", "108px"]
const fieldCounts = [6, 4, 5, 3]
const fieldWidths = ["60%", "75%", "50%", "80%", "65%", "70%", "55%", "85%"]
const listTitleWidths = ["160px", "200px", "140px", "180px", "120px", "190px"]
const activityWidths = ["180px", "140px", "220px", "160px", "200px", "130px"]
</script>

<style scoped>
.sk {
	animation: sk-pulse 1.6s ease-in-out infinite;
}

@keyframes sk-pulse {
	0% {
		opacity: 1;
	}
	50% {
		opacity: 0.45;
	}
	100% {
		opacity: 1;
	}
}
</style>
