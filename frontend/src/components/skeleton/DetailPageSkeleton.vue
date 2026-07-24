<template>
	<div class="min-h-screen bg-app-bg-secondary transition-colors duration-300 dark:bg-app-bg-dark">
		<!-- Breadcrumb -->
		<div class="px-1 pb-2">
			<div class="flex items-center gap-2">
				<div class="sk h-3.5 w-20 rounded-full bg-slate-200 dark:bg-slate-700" />
				<div class="sk h-3 w-2 rounded-full bg-slate-200 dark:bg-slate-700" />
				<div class="sk h-3.5 w-28 rounded-full bg-slate-200 dark:bg-slate-700" />
			</div>
		</div>

		<!-- Sticky header -->
		<div class="-mx-5 bg-app-bg-secondary px-5 pt-3 pb-1 dark:bg-app-bg-dark">
			<div
				class="flex flex-col items-start justify-between gap-4 px-1 sm:flex-row sm:items-center"
			>
				<!-- Avatar / icon badge + title + subtitle -->
				<div class="flex items-center gap-3">
					<!-- Circle avatar (user) -->
					<div
						v-if="shape === 'circle'"
						class="sk h-20 w-20 shrink-0 rounded-full bg-slate-200 dark:bg-slate-700"
					/>
					<!-- Square icon badge (default) -->
					<div v-else class="sk h-11 w-11 shrink-0 rounded-xl bg-slate-200 dark:bg-slate-700" />
					<div class="flex flex-col gap-2">
						<div class="sk h-6 w-48 rounded-full bg-slate-200 dark:bg-slate-700" />
						<div class="sk h-4 w-32 rounded-full bg-slate-100 dark:bg-slate-800" />
					</div>
				</div>
				<!-- Action + back buttons -->
				<div class="flex items-center gap-2">
					<div class="sk h-9 w-28 rounded-lg bg-slate-100 dark:bg-slate-800" />
					<div class="sk h-9 w-20 rounded-lg bg-slate-100 dark:bg-slate-800" />
				</div>
			</div>

			<!-- Tab bar -->
			<div class="mt-3 flex items-center gap-1 border-b border-slate-200 dark:border-slate-700">
				<div
					v-for="(w, i) in tabWidths.slice(0, tabs)"
					:key="i"
					class="sk h-8 rounded-t-md bg-slate-100 dark:bg-slate-800"
					:style="{ width: w }"
				/>
			</div>
		</div>

		<!-- Content -->
		<div
			class="mt-5"
			:class="
				hasSideCard
					? 'flex w-full flex-col gap-5 desktop:flex-row desktop:items-start desktop:gap-8'
					: 'flex flex-col gap-4'
			"
		>
			<!-- Main column -->
			<div :class="hasSideCard ? 'min-w-0 flex-1' : 'w-full'">
				<div
					v-for="s in sections"
					:key="s"
					class="mb-4 overflow-hidden rounded-2xl border border-slate-200/60 bg-white shadow-sm dark:border-slate-700/50 dark:bg-slate-800"
				>
					<!-- Section header -->
					<div class="border-b border-slate-100 px-5 py-3.5 dark:border-slate-700/50">
						<div
							class="sk h-4 rounded-full bg-slate-200 dark:bg-slate-700"
							:style="{ width: sectionTitleWidths[(s - 1) % sectionTitleWidths.length] }"
						/>
					</div>
					<!-- Field rows -->
					<div class="grid grid-cols-1 gap-x-8 gap-y-5 p-5 sm:grid-cols-2">
						<div
							v-for="f in sectionFieldCounts[(s - 1) % sectionFieldCounts.length]"
							:key="f"
							class="flex flex-col gap-1.5"
						>
							<div class="sk h-3 w-14 rounded-full bg-slate-100 dark:bg-slate-800" />
							<div
								class="sk h-4 rounded-full bg-slate-200 dark:bg-slate-700"
								:style="{ width: fieldWidths[(s * 4 + f) % fieldWidths.length] }"
							/>
						</div>
					</div>
				</div>
			</div>

			<!-- Side card -->
			<aside v-if="hasSideCard" class="w-full shrink-0 desktop:w-[260px]">
				<div
					class="rounded-2xl border border-slate-200/60 bg-white p-5 shadow-sm dark:border-slate-700/50 dark:bg-slate-800"
				>
					<!-- Avatar / identity block -->
					<div
						class="mb-5 flex flex-col items-center gap-3 border-b border-slate-100 pb-5 dark:border-slate-700"
					>
						<div class="sk h-16 w-16 rounded-full bg-slate-200 dark:bg-slate-700" />
						<div class="sk h-4 w-32 rounded-full bg-slate-200 dark:bg-slate-700" />
						<div class="sk h-3.5 w-24 rounded-full bg-slate-100 dark:bg-slate-800" />
					</div>
					<!-- Stat rows -->
					<div class="mb-5 flex flex-col gap-3">
						<div v-for="i in 4" :key="i" class="flex items-center justify-between">
							<div
								class="sk h-3.5 rounded-full bg-slate-100 dark:bg-slate-800"
								:style="{ width: cardLabelWidths[(i - 1) % cardLabelWidths.length] }"
							/>
							<div class="sk h-3.5 w-14 rounded-full bg-slate-200 dark:bg-slate-700" />
						</div>
					</div>
					<!-- Action button -->
					<div class="sk h-9 w-full rounded-lg bg-slate-100 dark:bg-slate-800" />
				</div>
			</aside>
		</div>
	</div>
</template>

<script setup>
defineProps({
	shape: {
		type: String,
		default: "square", // 'square' | 'circle'
	},
	hasSideCard: {
		type: Boolean,
		default: false,
	},
	tabs: {
		type: Number,
		default: 4,
	},
	sections: {
		type: Number,
		default: 3,
	},
})

const tabWidths = ["72px", "88px", "80px", "96px", "76px", "84px"]
const sectionTitleWidths = ["80px", "120px", "96px"]
const sectionFieldCounts = [6, 4, 5]
const fieldWidths = ["60%", "75%", "50%", "80%", "65%", "70%", "55%", "85%"]
const cardLabelWidths = ["72px", "88px", "64px", "80px"]
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
