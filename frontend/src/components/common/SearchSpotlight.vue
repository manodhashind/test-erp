<template>
	<Teleport to="body">
		<Transition name="spotlight-fade">
			<div
				v-if="isOpen"
				class="fixed inset-0 z-[9999] flex items-start justify-center bg-black/25 p-4 pt-[10vh] backdrop-blur-md dark:bg-black/50 sm:p-5 sm:pt-[12vh]"
				@click.self="close"
			>
				<div
					class="spotlight-search dark:bg-slate-900/85 relative w-full max-w-[95vw] overflow-hidden rounded-2xl border border-slate-200/80 bg-white/90 shadow-[0_20px_60px_-12px_rgba(0,0,0,0.45)] ring-1 ring-black/5 backdrop-blur-2xl backdrop-saturate-150 dark:border-slate-700/60 dark:ring-white/10 sm:max-w-lg md:max-w-2xl"
				>
					<SearchField
						v-model="query"
						size="lg"
						autofocus
						show-search-button
						placeholder="Search shipments, vehicles, drivers..."
						@search="handleSearch"
						@keydown.esc="close"
					/>

					<div
						v-if="filteredCategories.length"
						class="max-h-[360px] overflow-y-auto border-t border-slate-200/80 bg-white p-2 dark:border-slate-700/60 dark:bg-slate-900"
					>
						<div v-for="category in filteredCategories" :key="category.label">
							<div
								class="px-3 pt-3 pb-1 text-[11px] font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400"
							>
								{{ category.label }}
							</div>
							<button
								v-for="item in category.items"
								:key="item.label"
								class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left transition-colors hover:bg-black/5 dark:hover:bg-white/5"
								@click="selectItem(item)"
							>
								<Icon
									:icon="category.icon"
									size="16"
									class="shrink-0 text-slate-500 dark:text-slate-400"
								/>
								<span
									class="min-w-0 flex-1 truncate text-sm font-medium text-slate-800 dark:text-slate-100"
								>
									{{ item.label }}
								</span>
								<span class="shrink-0 text-xs text-slate-400 dark:text-slate-500">{{
									item.subtitle
								}}</span>
							</button>
						</div>
					</div>

					<div
						v-else
						class="border-t border-slate-200/80 bg-white p-6 text-center text-sm text-slate-400 dark:border-slate-700/60 dark:bg-slate-900 dark:text-slate-500"
					>
						No results found
					</div>
				</div>
			</div>
		</Transition>
	</Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from "vue"
import SearchField from "../fields/essential/SearchField.vue"
import Icon from "../Icon.vue"

const props = defineProps({
	isOpen: {
		type: Boolean,
		default: false,
	},
})

const emit = defineEmits(["close", "search"])

const query = ref("")

// Dummy dataset used until this is wired up to a real search endpoint.
const dummyCategories = [
	{
		label: "Shipments",
		icon: "truck-fast",
		items: [
			{ label: "SR-2024-001", subtitle: "Pending Approval" },
			{ label: "SR-2024-002", subtitle: "In Transit" },
		],
	},
	{
		label: "Vehicles",
		icon: "truck",
		items: [
			{ label: "TRK-101", subtitle: "Available" },
			{ label: "TRK-102", subtitle: "In Maintenance" },
		],
	},
	{
		label: "Drivers",
		icon: "steering",
		items: [
			{ label: "Rajesh Kumar", subtitle: "On Duty" },
			{ label: "Amit Singh", subtitle: "Off Duty" },
		],
	},
	{
		label: "Customers",
		icon: "account-tie",
		items: [
			{ label: "Acme Logistics", subtitle: "Active Customer" },
			{ label: "Global Traders", subtitle: "Active Customer" },
		],
	},
]

const filteredCategories = computed(() => {
	const q = query.value.trim().toLowerCase()
	if (!q) return dummyCategories

	return dummyCategories
		.map((category) => ({
			...category,
			items: category.items.filter(
				(item) => item.label.toLowerCase().includes(q) || item.subtitle.toLowerCase().includes(q),
			),
		}))
		.filter((category) => category.items.length > 0)
})

const selectItem = (item) => {
	emit("search", item.label)
	close()
}

const close = () => {
	emit("close")
}

const handleSearch = (value) => {
	emit("search", value)
	close()
}

const handleEsc = (e) => {
	if (e.key === "Escape" && props.isOpen) {
		close()
	}
}

onMounted(() => {
	document.addEventListener("keydown", handleEsc)
})

onUnmounted(() => {
	document.removeEventListener("keydown", handleEsc)
	document.body.style.overflow = ""
})

watch(
	() => props.isOpen,
	(open) => {
		document.body.style.overflow = open ? "hidden" : ""
		if (!open) {
			query.value = ""
		}
	},
)
</script>

<style scoped>
.spotlight-fade-enter-active,
.spotlight-fade-leave-active {
	transition: opacity 0.15s ease;
}

.spotlight-fade-enter-from,
.spotlight-fade-leave-to {
	opacity: 0;
}

/* The field's default border/ring/background is meant for compact form
   contexts on a solid page background; here the field IS the frosted-glass
   modal, so its own border/fill only doubles up and hides the glass. Drop
   them so the panel's blur/translucency reads through the whole box. */
.spotlight-search :deep(.rounded-field) {
	border: none !important;
	box-shadow: none !important;
	border-radius: 0 !important;
	padding: 1.1rem 1.25rem !important;
	background: transparent !important;
}

.spotlight-search :deep(input) {
	font-size: 1.05rem !important;
	background: transparent !important;
}

/* Soft glossy sheen across the top of the panel, like macOS's vibrancy. */
.spotlight-search::before {
	content: "";
	position: absolute;
	inset: 0;
	background: linear-gradient(180deg, rgb(255 255 255 / 35%), rgb(255 255 255 / 0%) 45%);
	pointer-events: none;
}
</style>
