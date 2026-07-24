<template>
	<div
		class="min-h-screen bg-app-bg-secondary p-5 transition-colors duration-300 dark:bg-app-bg-dark lg:p-[20px_28px]"
	>
		<!-- Header skeleton -->
		<div class="mb-7 border-b-2 border-slate-300 px-1 pb-4 dark:border-slate-600">
			<div class="flex flex-wrap items-center justify-between gap-4">
				<!-- Icon + title/description -->
				<div class="flex items-center gap-3">
					<div class="sk h-11 w-11 shrink-0 rounded-xl bg-slate-200 dark:bg-slate-700" />
					<div class="flex flex-col gap-2">
						<div class="sk h-6 w-40 rounded-full bg-slate-200 dark:bg-slate-700" />
						<div class="sk h-4 w-60 rounded-full bg-slate-100 dark:bg-slate-800" />
					</div>
				</div>
				<!-- Search bar -->
				<div class="sk h-10 w-full rounded-xl bg-slate-100 dark:bg-slate-800 sm:w-72" />
			</div>
		</div>

		<!-- Groups skeleton -->
		<div class="flex flex-col gap-10">
			<section v-for="group in skeletonGroups" :key="group.id">
				<!-- Group heading -->
				<div class="mb-5 flex items-center gap-3">
					<div class="sk h-9 w-9 rounded-xl bg-slate-200 dark:bg-slate-700" />
					<div class="sk h-5 w-36 rounded-full bg-slate-200 dark:bg-slate-700" />
					<div class="sk h-4 w-16 rounded-full bg-slate-100 dark:bg-slate-800" />
				</div>

				<!-- Cards grid -->
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
					<div
						v-for="card in group.cards"
						:key="card"
						class="flex items-start gap-4 rounded-2xl bg-white p-5 shadow-sm dark:bg-slate-800 dark:shadow-slate-900/40"
					>
						<!-- Icon badge -->
						<div class="sk mt-0.5 h-11 w-11 shrink-0 rounded-xl bg-slate-100 dark:bg-slate-700" />
						<!-- Text lines -->
						<div class="flex flex-1 flex-col gap-2 pt-1">
							<div
								class="sk h-4 rounded-full bg-slate-200 dark:bg-slate-700"
								:style="{ width: titleWidths[(group.id * 3 + card) % titleWidths.length] }"
							/>
							<div class="sk h-3 w-full rounded-full bg-slate-100 dark:bg-slate-800" />
							<div
								class="sk h-3 rounded-full bg-slate-100 dark:bg-slate-800"
								:style="{ width: descWidths[(group.id + card * 2) % descWidths.length] }"
							/>
						</div>
					</div>
				</div>
			</section>
		</div>
	</div>
</template>

<script setup>
const skeletonGroups = [
	{ id: 0, cards: [1, 2, 3, 4, 5, 6] },
	{ id: 1, cards: [1, 2, 3] },
	{ id: 2, cards: [1, 2, 3, 4] },
]

const titleWidths = ["60%", "75%", "55%", "80%", "65%", "70%"]
const descWidths = ["85%", "70%", "90%", "75%", "80%"]
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
