<template>
	<!-- Standalone: full table card chrome (drop-in replacement before DataTable mounts) -->
	<div
		v-if="standalone"
		class="overflow-hidden rounded-2xl border border-slate-300/60 bg-white shadow-[0_4px_24px_-4px_rgba(30,58,138,0.12),0_2px_8px_-2px_rgba(30,58,138,0.08)] dark:border-slate-700/50 dark:bg-sidebar-bg-dark dark:shadow-[0_4px_24px_-4px_rgba(0,0,0,0.4)]"
	>
		<!-- Header row -->
		<div
			class="flex items-center gap-4 border-b border-outline-variant bg-table-header px-6 py-3 dark:border-slate-700/50"
		>
			<div v-if="selectable" class="h-4 w-4 shrink-0 rounded bg-slate-200 dark:bg-slate-700" />
			<div
				v-for="col in columnCount"
				:key="col"
				class="h-2.5 rounded-full bg-slate-200 dark:bg-slate-700"
				:style="{ width: headerWidths[(col - 1) % headerWidths.length] }"
			/>
		</div>

		<!-- Skeleton rows -->
		<div
			v-for="row in rows"
			:key="row"
			class="flex items-center gap-4 border-b border-slate-200/70 px-6 py-3.5 last:border-b-0 dark:border-slate-700/60"
			:style="{ opacity: 1 - ((row - 1) / rows) * 0.35 }"
		>
			<div
				v-if="selectable"
				class="skeleton-cell h-4 w-4 shrink-0 rounded bg-slate-100 dark:bg-slate-800"
			/>
			<div
				v-for="col in columnCount"
				:key="col"
				class="skeleton-cell h-3.5 rounded-full bg-slate-100 dark:bg-slate-800"
				:style="{ width: cellWidths[(row * 3 + col - 4) % cellWidths.length] }"
			/>
		</div>
	</div>

	<!-- Inline: bare <tr> rows for insertion inside an existing <tbody> -->
	<template v-else>
		<tr
			v-for="row in rows"
			:key="row"
			class="border-b border-slate-200/70 dark:border-slate-700/60"
			:style="{ opacity: 1 - ((row - 1) / rows) * 0.35 }"
		>
			<td v-if="selectable" class="w-12 pl-6">
				<div class="skeleton-cell h-4 w-4 rounded bg-slate-100 dark:bg-slate-800" />
			</td>
			<td v-for="col in columnCount" :key="col" class="px-4 py-3 first:pl-6">
				<div
					class="skeleton-cell h-3.5 rounded-full bg-slate-100 dark:bg-slate-800"
					:style="{ width: cellWidths[(row * 3 + col - 4) % cellWidths.length] }"
				/>
			</td>
		</tr>
	</template>
</template>

<script setup>
defineProps({
	rows: {
		type: Number,
		default: 10,
	},
	columnCount: {
		type: Number,
		default: 5,
	},
	selectable: {
		type: Boolean,
		default: false,
	},
	standalone: {
		type: Boolean,
		default: false,
	},
})

const cellWidths = ["48px", "72px", "88px", "56px", "96px", "64px", "80px", "44px", "68px", "52px"]
const headerWidths = ["56px", "80px", "64px", "96px", "72px"]
</script>

<style scoped>
.skeleton-cell {
	animation: skeleton-shimmer 1.6s ease-in-out infinite;
	background-size: 200% 100%;
}

@keyframes skeleton-shimmer {
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
