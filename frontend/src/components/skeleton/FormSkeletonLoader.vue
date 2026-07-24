<template>
	<div class="flex flex-col gap-4">
		<!-- Tab bar -->
		<div class="flex items-center gap-1 border-b border-slate-200 pb-0 dark:border-slate-700">
			<div
				v-for="(w, i) in tabWidths.slice(0, tabs)"
				:key="i"
				class="sk h-8 rounded-t-md bg-slate-100 dark:bg-slate-800"
				:style="{ width: w }"
			/>
		</div>

		<!-- Section cards -->
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
					<!-- Label -->
					<div class="sk h-3 w-16 rounded-full bg-slate-100 dark:bg-slate-700" />
					<!-- Input box -->
					<div
						class="sk h-9 w-full rounded-lg bg-slate-100 dark:bg-slate-800"
						:style="{ opacity: 1 - ((f - 1) / 8) * 0.15 }"
					/>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
defineProps({
	tabs: {
		type: Number,
		default: 2,
	},
	sections: {
		type: Number,
		default: 3,
	},
})

const tabWidths = ["72px", "96px", "80px", "88px", "76px"]
const sectionTitleWidths = ["88px", "120px", "72px", "104px"]
const fieldCounts = [6, 4, 5, 3, 6]
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
