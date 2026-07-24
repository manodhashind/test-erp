<template>
	<div v-click-outside="close" class="relative">
		<button
			class="flex cursor-pointer items-center gap-2 rounded-lg border border-primary/25 bg-primary/5 px-4 py-2 text-sm font-semibold text-primary transition-all hover:border-primary hover:bg-primary/10 dark:border-primary-light/20 dark:bg-primary-light/5 dark:text-primary-light dark:hover:border-primary-light/40 dark:hover:bg-primary-light/10"
			@click="isOpen = !isOpen"
		>
			<Icon icon="view-column" :size="16" />
			<span>Columns</span>
		</button>

		<transition name="dropdown">
			<div
				v-if="isOpen"
				class="dark:border-primary-light/15 absolute right-0 top-[calc(100%+8px)] z-[100] flex w-[280px] flex-col overflow-hidden rounded-2xl border border-primary/20 bg-white shadow-lg dark:bg-app-bg-dark"
			>
				<div
					class="border-primary/15 dark:border-primary-light/15 flex shrink-0 items-center justify-between border-b p-4"
				>
					<h4 class="m-0 font-sans text-sm font-bold text-slate-900 dark:text-primary-light">
						Show/Hide Columns
					</h4>
					<div class="flex gap-2">
						<button
							class="cursor-pointer rounded border-none bg-transparent px-2 py-1 text-xs font-semibold text-primary transition-all hover:bg-slate-100 dark:text-primary-light dark:hover:bg-primary-light/10"
							@click="selectAll"
						>
							All
						</button>
					</div>
				</div>

				<div class="flex max-h-[300px] flex-col gap-0.5 overflow-y-auto p-2">
					<template v-for="(column, index) in sortedColumns" :key="column.key">
						<!-- Divider between visible and hidden -->
						<div
							v-if="
								index === selectedCount &&
								selectedCount > 0 &&
								selectedCount < sortedColumns.length
							"
							class="flex items-center gap-2 px-3 py-2 text-[10px] font-bold uppercase tracking-wider text-slate-400 before:h-[1px] before:flex-1 before:bg-slate-100 before:content-[''] after:h-[1px] after:flex-1 after:bg-slate-100 after:content-[''] dark:text-primary-light/40 dark:before:bg-primary-light/10 dark:after:bg-primary-light/10"
						>
							<span>Hidden</span>
						</div>
						<div
							class="dark:hover:bg-primary-light/8 flex items-center gap-2.5 rounded-lg p-2 px-3 transition-all hover:bg-slate-50"
							:class="{
								'cursor-not-allowed opacity-60': column.required,
								'border-t-2 border-primary': dragOverIndex === index && draggedIndex > index,
								'border-b-2 border-primary': dragOverIndex === index && draggedIndex < index,
								'bg-slate-100 opacity-40 dark:bg-slate-800': draggedIndex === index,
								'bg-primary/[0.04] hover:bg-primary/[0.08] dark:bg-primary/10 dark:hover:bg-primary/20':
									isColumnVisible(column.key),
							}"
							draggable="true"
							@dragstart="onDragStart(index)"
							@dragover.prevent="onDragOver(index)"
							@dragleave="onDragLeave(index)"
							@drop="onDrop(index)"
							@dragend="onDragEnd"
						>
							<div
								class="text-slate-350 cursor-grab select-none pr-1 font-bold active:cursor-grabbing dark:text-primary-light/25"
								title="Drag to reorder"
							>
								⋮⋮
							</div>
							<Checkbox
								:model-value="isColumnVisible(column.key)"
								:disabled="column.required"
								:label="column.label"
								size="sm"
								class="min-w-0 flex-1"
								@update:model-value="toggleColumn(column.key)"
							/>
							<span
								v-if="column.required"
								class="dark:bg-red-950/20 rounded border border-red-200/50 bg-red-50 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-red-500 dark:border-red-900/30"
								>Required</span
							>
						</div>
					</template>
				</div>

				<div
					class="border-primary/15 dark:border-primary-light/15 flex shrink-0 gap-2 border-t p-3"
				>
					<button
						class="hover:bg-primary-hover flex-1 cursor-pointer rounded-lg bg-primary py-2 px-3 text-xs font-semibold text-white shadow-sm transition-all hover:shadow"
						title="Save column preferences"
						@click="savePreferences"
					>
						Save Layout
					</button>
					<button
						class="flex-1 cursor-pointer rounded-lg border border-primary/20 bg-transparent py-2 px-3 text-xs font-semibold text-slate-600 transition-all hover:bg-slate-50 dark:border-primary-light/20 dark:text-primary-light/70 dark:hover:bg-primary-light/10"
						title="Reset to default columns and order"
						@click="resetToDefault"
					>
						Reset
					</button>
				</div>
			</div>
		</transition>
	</div>
</template>

<script setup>
import { ref, computed } from "vue"
import Checkbox from "../fields/Checkbox.vue"

const props = defineProps({
	columns: {
		type: Array,
		required: true,
	},
	visibleColumns: {
		type: Array,
		default: () => [],
	},
})

const emit = defineEmits(["update:visibleColumns", "update:columns", "reset", "save"])

// State
const isOpen = ref(false)
const draggedIndex = ref(null)
const dragOverIndex = ref(null)

// Computed
const sortedColumns = computed(() => {
	const visible = props.columns.filter((c) => props.visibleColumns.includes(c.key))
	const hidden = props.columns.filter((c) => !props.visibleColumns.includes(c.key))
	return [...visible, ...hidden]
})

const selectedCount = computed(() => {
	return sortedColumns.value.filter((c) => props.visibleColumns.includes(c.key)).length
})

// Methods
const isColumnVisible = (columnKey) => {
	return props.visibleColumns.includes(columnKey)
}

const toggleColumn = (columnKey) => {
	const column = props.columns.find((c) => c.key === columnKey)
	if (column?.required) return

	const wasVisible = props.visibleColumns.includes(columnKey)
	let newVisible = [...props.visibleColumns]
	let newColumns = props.columns

	if (wasVisible) {
		newVisible = newVisible.filter((k) => k !== columnKey)
	} else {
		newVisible.push(columnKey)
		// Move the newly-shown column to the end of the column order so it
		// appends after the currently visible columns instead of reappearing
		// at its old schema position.
		newColumns = [...props.columns.filter((c) => c.key !== columnKey), column]
	}
	emit("update:visibleColumns", newVisible)
	emit("update:columns", newColumns)
}

const selectAll = () => {
	const allKeys = props.columns.map((c) => c.key)
	emit("update:visibleColumns", allKeys)
	// Keep column order as-is
	emit("update:columns", props.columns)
}

const selectNone = () => {
	const requiredKeys = props.columns.filter((c) => c.required).map((c) => c.key)
	emit("update:visibleColumns", requiredKeys)
	// Keep column order as-is
	emit("update:columns", props.columns)
}

const resetToDefault = () => {
	emit("reset")
}

const savePreferences = () => {
	emit("save")
	close()
}

const close = () => {
	isOpen.value = false
}

const onDragStart = (index) => {
	draggedIndex.value = index
}

const onDragOver = (index) => {
	dragOverIndex.value = index
}

const onDragLeave = (index) => {
	if (dragOverIndex.value === index) {
		dragOverIndex.value = null
	}
}

const onDragEnd = () => {
	draggedIndex.value = null
	dragOverIndex.value = null
}

const onDrop = (index) => {
	if (draggedIndex.value === null || draggedIndex.value === index) {
		onDragEnd()
		return
	}

	const movedItem = props.columns[draggedIndex.value]
	const wasChecked = isColumnVisible(movedItem.key)
	const checkedCount = props.columns.filter((c) => isColumnVisible(c.key)).length

	let newVisible = [...props.visibleColumns]
	let visibilityChanged = false

	if (!wasChecked && index < checkedCount) {
		newVisible.push(movedItem.key)
		visibilityChanged = true
	} else if (wasChecked && index >= checkedCount) {
		if (!movedItem.required) {
			newVisible = newVisible.filter((k) => k !== movedItem.key)
			visibilityChanged = true
		} else {
			index = checkedCount - 1
		}
	}

	const newColumns = [...props.columns]
	const [extracted] = newColumns.splice(draggedIndex.value, 1)
	newColumns.splice(index, 0, extracted)

	if (visibilityChanged) {
		emit("update:visibleColumns", newVisible)
	}
	// Emit new column order directly without partitioning
	emit("update:columns", newColumns)
	onDragEnd()
}

// Click outside directive
const vClickOutside = {
	mounted(el, binding) {
		el.clickOutsideEvent = function (event) {
			if (!(el === event.target || el.contains(event.target))) {
				binding.value()
			}
		}
		document.addEventListener("click", el.clickOutsideEvent)
	},
	unmounted(el) {
		document.removeEventListener("click", el.clickOutsideEvent)
	},
}
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
	transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
	opacity: 0;
	transform: translateY(-10px);
}
</style>
