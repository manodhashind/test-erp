<template>
	<div class="relative shrink-0">
		<!-- ── Skeleton toolbar (while schema is loading) ────────────────────────── -->
		<div
			v-if="!schemaLoaded || !firstDataReceived"
			class="mb-2 flex items-center justify-between gap-2"
		>
			<div class="filterbar-skeleton mt-0.5 h-9 w-72 rounded-lg bg-slate-100 dark:bg-slate-800" />
			<div class="flex items-center gap-2">
				<div class="filterbar-skeleton h-9 w-9 rounded-lg bg-slate-100 dark:bg-slate-800" />
				<div class="filterbar-skeleton h-9 w-20 rounded-lg bg-slate-100 dark:bg-slate-800" />
				<div class="filterbar-skeleton h-9 w-9 rounded-lg bg-slate-100 dark:bg-slate-800" />
				<div class="filterbar-skeleton h-9 w-20 rounded-lg bg-slate-100 dark:bg-slate-800" />
			</div>
		</div>

		<!-- ── Toolbar ──────────────────────────────────────────────────────────────── -->
		<div v-else class="mb-2 flex items-center justify-between gap-2">
			<div class="flex items-center gap-2">
				<slot name="before-search" />
				<SearchField
					v-model="searchQuery"
					placeholder="Search..."
					class="mt-0.5 w-72"
					@update:model-value="handleSearchInput"
					clearable
				/>
			</div>
			<div class="flex items-center gap-2">
				<!-- View toggle -->
				<div
					v-if="showViewToggle"
					class="flex rounded-lg border border-primary/20 bg-primary/5 p-1 dark:border-primary/30 dark:bg-primary/10"
				>
					<button
						class="flex cursor-pointer items-center justify-center rounded-md border-none bg-transparent p-1.5 transition-all"
						:class="{
							'dark:border-slate-650 border border-slate-200/40 bg-white shadow-sm dark:bg-primary/20':
								viewType === 'card',
						}"
						title="Card View"
						@click="$emit('update:viewType', 'card')"
					>
						<svg
							width="16"
							height="16"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
							:class="
								viewType === 'card'
									? 'stroke-[2.5] text-primary dark:text-primary-light'
									: 'text-primary/35 dark:text-primary-light/40'
							"
						>
							<rect x="3" y="3" width="7" height="7" />
							<rect x="14" y="3" width="7" height="7" />
							<rect x="14" y="14" width="7" height="7" />
							<rect x="3" y="14" width="7" height="7" />
						</svg>
					</button>
					<button
						class="flex cursor-pointer items-center justify-center rounded-md border-none bg-transparent p-1.5 transition-all"
						:class="{
							'dark:border-slate-650 border border-slate-200/40 bg-white shadow-sm dark:bg-primary/20':
								viewType === 'table',
						}"
						title="Table View"
						@click="$emit('update:viewType', 'table')"
					>
						<svg
							width="16"
							height="16"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
							:class="
								viewType === 'table'
									? 'stroke-[2.5] text-primary dark:text-primary-light'
									: 'text-primary/35 dark:text-primary-light/40'
							"
						>
							<line x1="8" y1="6" x2="21" y2="6" />
							<line x1="8" y1="12" x2="21" y2="12" />
							<line x1="8" y1="18" x2="21" y2="18" />
							<line x1="3" y1="6" x2="3.01" y2="6" />
							<line x1="3" y1="12" x2="3.01" y2="12" />
							<line x1="3" y1="18" x2="3.01" y2="18" />
						</svg>
					</button>
				</div>

				<!-- Refresh -->
				<button
					class="flex cursor-pointer items-center justify-center rounded-lg border border-primary/25 bg-primary/5 p-2 text-primary transition-all hover:border-primary hover:bg-primary/10 dark:border-primary-light/20 dark:bg-primary-light/5 dark:text-primary-light dark:hover:border-primary-light/40 dark:hover:bg-primary-light/10"
					title="Refresh"
					@click="$emit('refresh')"
				>
					<Icon icon="refresh" :size="15" />
				</button>

				<!-- Sort -->
				<div v-click-outside="closeSortMenu" class="relative flex items-center gap-1">
					<button
						class="flex cursor-pointer items-center gap-2 rounded-lg border border-primary/25 bg-primary/5 px-4 py-2 text-sm font-semibold text-primary transition-all hover:border-primary hover:bg-primary/10 dark:border-primary-light/20 dark:bg-primary-light/5 dark:text-primary-light dark:hover:border-primary-light/40 dark:hover:bg-primary-light/10"
						:class="{
							'!bg-primary/15 !border-primary dark:!border-primary-light/40':
								isSortMenuOpen || sortOrders.length > 0,
						}"
						@click="toggleSortMenu"
					>
						<Icon icon="sort" :size="15" />
						Sort
						<span
							v-if="sortOrders.length > 0"
							class="flex h-4 w-4 items-center justify-center rounded-full bg-primary text-[10px] font-bold text-white dark:bg-primary"
							>{{ sortOrders.length }}</span
						>
					</button>
					<!-- Asc/Desc toggle — visible when at least one sort is active -->
					<button
						v-if="sortOrders.length > 0"
						class="flex h-[36px] w-[36px] cursor-pointer items-center justify-center rounded-lg border border-primary/25 bg-primary/5 text-primary transition-all hover:border-primary hover:bg-primary/10 dark:border-primary-light/20 dark:bg-primary-light/5 dark:text-primary-light dark:hover:border-primary-light/40 dark:hover:bg-primary-light/10"
						:title="
							sortOrders[0].order === 'asc'
								? 'Ascending — click to switch to Descending'
								: 'Descending — click to switch to Ascending'
						"
						@click="togglePrimaryDirection"
					>
						<Icon :icon="sortOrders[0].order === 'asc' ? 'arrow-up' : 'arrow-down'" :size="15" />
					</button>
					<!-- Clear all sorts -->
					<button
						v-if="sortOrders.length > 0"
						class="dark:bg-red-950/20 flex h-[36px] w-[36px] cursor-pointer items-center justify-center rounded-lg border border-red-200 bg-red-50 text-red-500 transition-all hover:border-red-400 hover:bg-red-100 dark:border-red-800/30 dark:text-red-400 dark:hover:border-red-700/50 dark:hover:bg-red-900/30"
						title="Clear all sorts"
						@click="clearSort"
					>
						<Icon icon="close" :size="13" />
					</button>
					<transition name="dropdown">
						<div
							v-if="isSortMenuOpen"
							class="absolute top-[calc(100%+6px)] right-0 z-[2000] flex w-64 flex-col rounded-xl border border-slate-200/80 bg-white py-2 shadow-lg dark:border-primary/30 dark:bg-app-bg-dark"
						>
							<div class="border-b border-slate-200/70 px-3 py-2 dark:border-primary/30">
								<h4 class="m-0 font-sans text-xs font-bold text-slate-900 dark:text-primary-light">
									Sort By
								</h4>
							</div>
							<!-- Active sorts -->
							<div v-if="sortOrders.length > 0" class="py-1">
								<p
									class="px-3 pb-1 pt-1 text-[10px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500"
								>
									Active
								</p>
								<div
									v-for="(sort, i) in sortOrders"
									:key="sort.key"
									draggable="true"
									class="flex items-center gap-2 px-3 py-1.5 transition-opacity"
									:class="{
										'opacity-40': dragFromIdx === i,
										'border-t-2 border-primary dark:border-primary-light':
											dragOverIdx === i && dragFromIdx !== i,
									}"
									@dragstart="onDragStart(i)"
									@dragover.prevent="dragOverIdx = i"
									@drop.prevent="onDrop(i)"
									@dragend="onDragEnd"
								>
									<Icon
										icon="drag-vertical"
										:size="14"
										class="shrink-0 cursor-grab text-slate-300 dark:text-slate-600"
									/>
									<span
										class="flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-primary/10 text-[10px] font-bold text-primary dark:bg-primary/25 dark:text-primary-light"
										>{{ i + 1 }}</span
									>
									<span
										class="min-w-0 flex-1 truncate text-sm font-medium text-slate-700 dark:text-primary-light"
										>{{ labelForKey(sort.key) }}</span
									>
									<button
										class="hover:bg-primary/15 dark:bg-primary/15 flex shrink-0 cursor-pointer items-center gap-0.5 rounded border border-primary/20 bg-primary/5 px-1.5 py-0.5 text-[10px] font-semibold text-primary transition-all dark:border-primary/30 dark:text-primary-light"
										@click.stop="toggleSortDirection(sort.key)"
									>
										<Icon :icon="sort.order === 'asc' ? 'arrow-up' : 'arrow-down'" :size="10" />
										{{ sort.order === "asc" ? "Asc" : "Desc" }}
									</button>
									<button
										class="flex h-5 w-5 shrink-0 cursor-pointer items-center justify-center rounded border-none bg-transparent text-slate-400 transition-all hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400"
										@click.stop="removeSortKey(sort.key)"
									>
										<Icon icon="close" :size="12" />
									</button>
								</div>
								<div class="mx-3 mt-1 border-t border-slate-200/70 dark:border-primary/30" />
							</div>
							<!-- Available fields to add -->
							<div class="flex max-h-[220px] flex-col overflow-y-auto py-1">
								<p
									v-if="availableToAdd.length > 0"
									class="px-3 pb-1 pt-1 text-[10px] font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500"
								>
									Add Sort
								</p>
								<button
									v-for="field in availableToAdd"
									:key="field.key"
									class="flex w-full cursor-pointer items-center gap-2 border-none bg-transparent px-3 py-2 text-left transition-all hover:bg-slate-50 dark:hover:bg-primary/20"
									@click="addSortField(field.key)"
								>
									<Icon icon="plus" :size="12" class="shrink-0 text-slate-400" />
									<span class="text-sm font-medium text-slate-700 dark:text-primary-light">{{
										field.label
									}}</span>
								</button>
								<p
									v-if="availableToAdd.length === 0 && sortOrders.length > 0"
									class="px-3 py-2 text-xs text-slate-400 dark:text-slate-500"
								>
									All sortable fields added.
								</p>
							</div>
							<div
								v-if="sortOrders.length > 0"
								class="flex justify-end border-t border-slate-200/70 px-3 py-2 dark:border-primary/30"
							>
								<button
									class="dark:bg-red-950/20 cursor-pointer rounded-lg border-none bg-red-50 px-3 py-1.5 text-xs font-semibold text-red-600 hover:bg-red-100 dark:text-red-400"
									@click="clearSort"
								>
									Clear All
								</button>
							</div>
						</div>
					</transition>
				</div>

				<!-- Extra controls (Columns) -->
				<slot name="extra-controls" />

				<!-- Filter button + floating panel -->
				<div class="relative flex items-center gap-1">
					<button
						class="flex cursor-pointer items-center gap-2 rounded-lg border border-primary/25 bg-primary/5 px-4 py-2 text-sm font-semibold text-primary transition-all hover:border-primary hover:bg-primary/10 dark:border-primary-light/20 dark:bg-primary-light/5 dark:text-primary-light dark:hover:border-primary-light/40 dark:hover:bg-primary-light/10"
						:class="{
							'!bg-primary/15 !border-primary dark:!border-primary-light/40':
								isFilterPanelOpen || activeFilters.length > 0,
						}"
						@click="toggleFilterPanel"
					>
						<Icon icon="filter-variant" :size="15" />
						Filter
						<span
							v-if="activeFilters.length"
							class="flex h-4 w-4 items-center justify-center rounded-full bg-primary text-[10px] font-bold text-white dark:bg-primary"
							>{{ activeFilters.length }}</span
						>
					</button>
					<!-- Clear all filters -->
					<button
						v-if="activeFilters.length > 0"
						class="dark:bg-red-950/20 flex h-[36px] w-[36px] cursor-pointer items-center justify-center rounded-lg border border-red-200 bg-red-50 text-red-500 transition-all hover:border-red-400 hover:bg-red-100 dark:border-red-800/30 dark:text-red-400 dark:hover:border-red-700/50 dark:hover:bg-red-900/30"
						title="Clear all filters"
						@click="clearAllAndClose"
					>
						<Icon icon="close" :size="13" />
					</button>

					<!-- Backdrop — closes panel when clicking anywhere outside -->
					<div v-if="isFilterPanelOpen" class="fixed inset-0 z-[1999]" @click="closeFilterPanel" />

					<!-- ── Filter Panel ────────────────────────────────────────────────────── -->
					<transition name="filter-panel">
						<div
							v-if="isFilterPanelOpen"
							class="absolute right-0 top-[calc(100%+6px)] z-[2000] w-max min-w-[560px] max-w-[90vw] rounded-xl border border-slate-200 bg-white p-4 shadow-lg dark:border-primary/30 dark:bg-app-bg-dark"
						>
							<!-- Empty state -->
							<p v-if="!draftRows.length" class="mb-2 text-sm text-slate-400 dark:text-slate-500">
								No filters — click "+ Add Filter" or Search to clear all.
							</p>

							<!-- Filter rows -->
							<div
								v-for="(row, idx) in draftRows"
								:key="row._id"
								class="mb-2 flex items-center gap-2 last:mb-0"
							>
								<!-- Connector -->
								<div class="w-20 shrink-0">
									<span v-if="idx === 0" class="block px-2 text-sm font-medium text-slate-400"
										>Where</span
									>
									<FieldRenderer v-else v-model="row.logic" :field="logicFieldConfig" />
								</div>

								<!-- Field -->
								<div class="w-44 shrink-0">
									<FieldRenderer
										v-model="row.field"
										:field="rowFieldSelectConfig"
										@update:model-value="onRowFieldChange(idx)"
									/>
								</div>

								<!-- Operator -->
								<div v-if="row.field" class="w-36 shrink-0">
									<FieldRenderer
										v-model="row.operator"
										:field="rowOperatorConfig(row)"
										@update:model-value="onRowOperatorChange(idx)"
									/>
								</div>

								<!-- Value -->
								<div
									v-if="
										row.field &&
										!['is_empty', 'is_not_empty', 'is_set', 'is_not_set'].includes(row.operator)
									"
									class="min-w-0 flex-1"
								>
									<FieldRenderer v-model="row.value" :field="rowValueConfig(row)" />
								</div>

								<!-- Remove -->
								<button
									class="ml-auto flex h-7 w-7 shrink-0 cursor-pointer items-center justify-center rounded-md border-none bg-transparent text-slate-400 transition-all hover:bg-red-50 hover:text-red-500 dark:hover:bg-red-900/20 dark:hover:text-red-400"
									@click="removeRow(row._id)"
								>
									<Icon icon="close" :size="14" />
								</button>
							</div>

							<!-- Footer -->
							<div
								class="mt-3 flex items-center justify-between border-t border-slate-200/70 pt-3 dark:border-primary/30"
							>
								<button
									class="dark:bg-primary/15 flex cursor-pointer items-center gap-1.5 rounded-lg border border-primary/30 bg-primary/5 px-3 py-1.5 text-sm font-semibold text-primary transition-all hover:bg-primary/10 dark:border-primary/30 dark:text-primary-light"
									@click="addRow"
								>
									<Icon icon="plus" :size="14" /> Add Filter
								</button>

								<div class="flex items-center gap-2">
									<button
										class="dark:bg-primary/15 cursor-pointer rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-sm font-semibold text-slate-600 transition-all hover:bg-slate-50 dark:border-primary/30 dark:text-primary-light"
										@click="clearAllAndClose"
									>
										Clear all Filters
									</button>
									<button
										class="flex cursor-pointer items-center gap-1.5 rounded-lg bg-primary px-4 py-1.5 text-sm font-semibold text-white transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
										:disabled="!hasValidRows"
										@click="applySearch"
									>
										<Icon icon="magnify" :size="14" /> Search
									</button>
								</div>
							</div>
						</div>
					</transition>
				</div>
				<!-- end filter wrapper -->

				<slot name="after-filter" />
			</div>
			<!-- end right controls -->
		</div>
		<!-- end v-else toolbar -->
	</div>
</template>

<script setup>
import { FieldRenderer } from "../../fields"
import { ApiService } from "../../../services/api"
import { useSchema } from "../../../composables/useSchema"
import Icon from "../../Icon.vue"
import SearchField from "../../fields/essential/SearchField.vue"
import { ref, computed, watch, onMounted } from "vue"

const props = defineProps({
	doctype: { type: String, default: "" },
	data: { type: Array, default: () => [] },
	entriesPerPage: { type: [Number, String], default: 20 },
	activeFilters: { type: Array, default: () => [] },
	availableFields: { type: Array, default: () => [] },
	showViewToggle: { type: Boolean, default: false },
	viewType: { type: String, default: "table" },
	totalItems: { type: Number, default: 0 },
	showingItems: { type: Number, default: 0 },
	sortOrders: { type: Array, default: () => [] },
})

const emit = defineEmits([
	"remove-filter",
	"add-filter",
	"update-filter",
	"clear-all-filters",
	"update:entriesPerPage",
	"update:viewType",
	"toggle-view",
	"sort",
	"refresh",
	"schema-loaded",
	"update:search",
	"search",
])

const searchQuery = ref("")
const handleSearchInput = (val) => {
	searchQuery.value = val
	emit("update:search", val)
	emit("search", val)
}

const { fields: schemaFields, fetchSchema } = useSchema(props.doctype)

const schemaLoaded = ref(false)
const firstDataReceived = ref(false)

// After schema loads, watch for the first data update from the parent's fetch
watch(
	() => props.data,
	() => {
		if (schemaLoaded.value && !firstDataReceived.value) {
			firstDataReceived.value = true
		}
	},
)

onMounted(async () => {
	if (props.doctype) {
		await fetchSchema()
		schemaLoaded.value = true
		emit("schema-loaded", schemaFields.value)
	}
})

// ── Sort ──────────────────────────────────────────────────────────────────────

const isSortMenuOpen = ref(false)

const sortableFields = computed(() =>
	props.availableFields.filter((f) => {
		const field = schemaFields.value.find((sf) => sf.fieldname === f.key)
		return (
			field &&
			["Data", "Int", "Float", "Date", "Datetime", "Link", "Select"].includes(field.fieldtype)
		)
	}),
)

const availableToAdd = computed(() => {
	const activeKeys = new Set(props.sortOrders.map((s) => s.key))
	return sortableFields.value.filter((f) => !activeKeys.has(f.key))
})

const labelForKey = (key) => props.availableFields.find((f) => f.key === key)?.label ?? key

const toggleSortMenu = () => {
	isSortMenuOpen.value = !isSortMenuOpen.value
}
const closeSortMenu = () => {
	isSortMenuOpen.value = false
}

const togglePrimaryDirection = () => {
	if (!props.sortOrders.length) return
	emit(
		"sort",
		props.sortOrders.map((s, i) =>
			i === 0 ? { ...s, order: s.order === "asc" ? "desc" : "asc" } : s,
		),
	)
}

const toggleSortDirection = (key) => {
	emit(
		"sort",
		props.sortOrders.map((s) =>
			s.key === key ? { ...s, order: s.order === "asc" ? "desc" : "asc" } : s,
		),
	)
}

const addSortField = (key) => {
	emit("sort", [...props.sortOrders, { key, order: "asc" }])
}

const removeSortKey = (key) => {
	emit(
		"sort",
		props.sortOrders.filter((s) => s.key !== key),
	)
}

const clearSort = () => {
	emit("sort", [])
	closeSortMenu()
}

// ── Sort drag-to-reorder ──────────────────────────────────────────────────────

const dragFromIdx = ref(null)
const dragOverIdx = ref(null)

const onDragStart = (i) => {
	dragFromIdx.value = i
}

const onDrop = (i) => {
	if (dragFromIdx.value === null || dragFromIdx.value === i) return
	const newOrders = [...props.sortOrders]
	const [moved] = newOrders.splice(dragFromIdx.value, 1)
	newOrders.splice(i, 0, moved)
	emit("sort", newOrders)
	dragFromIdx.value = null
	dragOverIdx.value = null
}

const onDragEnd = () => {
	dragFromIdx.value = null
	dragOverIdx.value = null
}

// ── Filter panel ──────────────────────────────────────────────────────────────

const isFilterPanelOpen = ref(false)
const draftRows = ref([])

let _rowId = 0
const blankRow = () => ({ _id: ++_rowId, field: "", operator: "equals", value: "", logic: "AND" })

const toggleFilterPanel = () => {
	if (isFilterPanelOpen.value) {
		closeFilterPanel()
	} else {
		draftRows.value = props.activeFilters.length
			? props.activeFilters.map((f) => ({ ...f, _id: ++_rowId }))
			: [blankRow()]
		isFilterPanelOpen.value = true
	}
}

const closeFilterPanel = () => {
	isFilterPanelOpen.value = false
	draftRows.value = []
}

const addRow = () => {
	draftRows.value.push(blankRow())
}

const removeRow = (id) => {
	draftRows.value = draftRows.value.filter((r) => r._id !== id)
}

const hasValidRows = computed(() =>
	draftRows.value.some((row) => {
		if (!row.field) return false
		if (["is_set", "is_not_set", "is_empty", "is_not_empty"].includes(row.operator)) return true
		const val = row.value
		return val !== null && val !== undefined && val !== ""
	}),
)

const applySearch = () => {
	emit("clear-all-filters")
	for (const row of draftRows.value) {
		if (!row.field) continue
		const needsValue = !["is_set", "is_not_set", "is_empty", "is_not_empty"].includes(row.operator)
		if (needsValue && (row.value === null || row.value === undefined || row.value === "")) continue
		const field = props.availableFields.find((f) => f.key === row.field)
		emit("add-filter", { ...row, label: buildLabel(row, field) })
	}
	closeFilterPanel()
}

const clearAllAndClose = () => {
	emit("clear-all-filters")
	closeFilterPanel()
}

const buildLabel = (row, field) => {
	if (!field) return row.field
	const sym = getOperatorSymbol(row.operator)
	if (["is_set", "is_not_set", "is_empty", "is_not_empty"].includes(row.operator)) {
		return `${field.label} ${sym}`
	}
	return `${field.label} ${sym} ${row.value}`
}

// ── Per-row field / operator / value configs ──────────────────────────────────

const logicFieldConfig = computed(() => ({
	type: "select",
	size: "sm",
	showArrow: false,
	options: [
		{ label: "AND", value: "AND" },
		{ label: "OR", value: "OR" },
	],
}))

const rowFieldSelectConfig = computed(() => ({
	type: "select",
	size: "sm",
	showArrow: false,
	placeholder: "Select field…",
	options: props.availableFields.map((f) => ({ label: f.label, value: f.key })),
}))

const rowOperatorConfig = (row) => ({
	type: "select",
	size: "sm",
	showArrow: false,
	placeholder: "Condition…",
	options: getOperatorsForType(props.availableFields.find((f) => f.key === row.field)?.type),
})

const rowValueConfig = (row) => {
	const field = props.availableFields.find((f) => f.key === row.field)
	return field ? buildValueFieldConfig(field, row.operator) : null
}

const onRowFieldChange = (idx) => {
	const row = draftRows.value[idx]
	const ops = getOperatorsForType(props.availableFields.find((f) => f.key === row.field)?.type)
	row.operator = ops?.[0]?.value || "equals"
	row.value = ""
}

const onRowOperatorChange = (idx) => {
	draftRows.value[idx].value = ""
}

// ── Operator helpers ──────────────────────────────────────────────────────────

const getOperatorSymbol = (operator) =>
	({
		equals: "=",
		not_equals: "≠",
		contains: "contains",
		not_contains: "does not contain",
		starts_with: "starts with",
		ends_with: "ends with",
		is_empty: "is empty",
		is_not_empty: "is not empty",
		is_set: "is set",
		is_not_set: "is not set",
		like: "like",
		not_like: "not like",
		in: "in",
		not_in: "not in",
		between: "between",
		timespan: "timespan",
		">": ">",
		"<": "<",
		">=": "≥",
		"<=": "≤",
	})[operator] || operator

const getOperatorsForType = (type) => {
	const eq = { value: "equals", label: "=" }
	const neq = { value: "not_equals", label: "≠" }
	const gt = { value: ">", label: ">" }
	const gte = { value: ">=", label: "≥" }
	const lt = { value: "<", label: "<" }
	const lte = { value: "<=", label: "≤" }
	const like = { value: "like", label: "like" }
	const nlike = { value: "not_like", label: "not like" }
	const inn = { value: "in", label: "in" }
	const nin = { value: "not_in", label: "not in" }
	const btwn = { value: "between", label: "between" }
	const tspan = { value: "timespan", label: "timespan" }
	const isset = { value: "is_set", label: "is set" }
	const notset = { value: "is_not_set", label: "is not set" }

	return (
		{
			Data: [eq, neq, like, nlike, inn, nin, isset, notset],
			"Small Text": [eq, neq, like, nlike, isset, notset],
			Text: [like, nlike, isset, notset],
			"Long Text": [like, nlike, isset, notset],
			Int: [eq, neq, gt, gte, lt, lte, btwn, isset, notset],
			Float: [eq, neq, gt, gte, lt, lte, btwn, isset, notset],
			Currency: [eq, neq, gt, gte, lt, lte, btwn, isset, notset],
			Date: [eq, neq, gt, gte, lt, lte, btwn, tspan, isset, notset],
			Datetime: [eq, neq, gt, gte, lt, lte, btwn, tspan, isset, notset],
			Select: [eq, neq, inn, nin, isset, notset],
			Link: [eq, neq, inn, nin, like, nlike, isset, notset],
			Check: [eq],
			Phone: [eq, neq, like, nlike, isset, notset],
			Email: [eq, neq, like, nlike, inn, nin, isset, notset],
		}[type] || [eq, neq, like, nlike, isset, notset]
	)
}

// ── Value field config ────────────────────────────────────────────────────────

const resolveValueFieldType = (frappeType, operator) => {
	const textOps = ["like", "not_like", "contains", "not_contains", "starts_with", "ends_with"]
	const listOps = ["in", "not_in"]
	if (textOps.includes(operator)) return "text"
	if (listOps.includes(operator)) return "tagInput"
	if (operator === "between")
		return frappeType === "Date"
			? "dateRange"
			: frappeType === "Datetime"
				? "datetimeRange"
				: "text"
	if (operator === "timespan") return "select"
	return (
		{
			Data: "text",
			"Small Text": "text",
			Text: "text",
			"Long Text": "text",
			Int: "number",
			Float: "number",
			Currency: "currency",
			Percent: "number",
			Date: "date",
			Datetime: "datetime",
			Select: "select",
			Autocomplete: "autocomplete",
			Link: "asyncLookup",
			"Dynamic Link": "asyncLookup",
			Check: "select",
			Phone: "phone",
			Email: "email",
		}[frappeType] || "text"
	)
}

const buildValueFieldConfig = (field, operator) => {
	const frappeType = field.type
	const uiType = resolveValueFieldType(frappeType, operator)
	const config = {
		type: uiType,
		label: "",
		placeholder: operator === "timespan" ? "Select timespan…" : "Type to search",
		size: "sm",
		clearable: true,
		showArrow: false,
	}
	if (uiType === "select") {
		if (operator === "timespan") {
			config.options = [
				{ label: "Today", value: "today" },
				{ label: "Yesterday", value: "yesterday" },
				{ label: "This Week", value: "this week" },
				{ label: "Last Week", value: "last week" },
				{ label: "This Month", value: "this month" },
				{ label: "Last Month", value: "last month" },
				{ label: "This Quarter", value: "this quarter" },
				{ label: "Last Quarter", value: "last quarter" },
				{ label: "This Year", value: "this year" },
				{ label: "Last Year", value: "last year" },
			]
		} else {
			const raw = field.options || ""
			if (frappeType === "Check") {
				config.options = [
					{ label: "Yes", value: 1 },
					{ label: "No", value: 0 },
				]
			} else {
				config.options = raw
					.split("\n")
					.filter(Boolean)
					.map((o) => ({ label: o.trim(), value: o.trim() }))
			}
		}
	}
	if (uiType === "asyncLookup") {
		config.fetchFunction = async ({ query }) => {
			try {
				const res = await ApiService.get("tms.api.meta.lookup.search_link", {
					doctype: field.options,
					txt: query,
				})
				return res.message ?? { items: [], hasMore: false }
			} catch {
				return { items: [] }
			}
		}
	}
	if (uiType === "tagInput") config.placeholder = "Add values…"
	if (uiType === "dateRange") config.mode = frappeType === "Datetime" ? "datetime" : "date"
	return config
}

// ── Click-outside directive ───────────────────────────────────────────────────

const vClickOutside = {
	mounted(el, binding) {
		el.clickOutsideEvent = (e) => {
			// If the target was removed from the DOM during this click (e.g. a delete button),
			// don't treat it as an outside click.
			if (!document.contains(e.target)) return
			if (!(el === e.target || el.contains(e.target))) binding.value()
		}
		document.addEventListener("click", el.clickOutsideEvent)
	},
	unmounted(el) {
		document.removeEventListener("click", el.clickOutsideEvent)
	},
}
</script>

<style scoped>
.filterbar-skeleton {
	animation: filterbar-shimmer 1.6s ease-in-out infinite;
}

@keyframes filterbar-shimmer {
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

.dropdown-enter-active,
.dropdown-leave-active {
	transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}
.dropdown-enter-from,
.dropdown-leave-to {
	opacity: 0;
	transform: translateY(6px);
}

.filter-panel-enter-active,
.filter-panel-leave-active {
	transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.filter-panel-enter-from,
.filter-panel-leave-to {
	opacity: 0;
	transform: translateY(-6px);
}
</style>
