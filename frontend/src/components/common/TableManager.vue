<template>
	<div
		class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800"
	>
		<!-- Section Header -->
		<div class="mb-6 flex items-center justify-between">
			<div class="flex items-center gap-3 text-primary dark:text-primary-light">
				<slot name="icon">
					<svg
						width="18"
						height="18"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<rect x="3" y="3" width="18" height="18" rx="2" />
					</svg>
				</slot>
				<h3 class="m-0 text-lg font-bold text-primary dark:text-primary-light">
					{{ title }}
				</h3>
			</div>
			<slot name="badge" />
		</div>

		<!-- Empty State -->
		<div v-if="items.length === 0" class="flex flex-col items-center justify-center py-12">
			<div
				class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-700"
			>
				<slot name="empty-icon">
					<svg
						width="28"
						height="28"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						class="text-slate-400 dark:text-slate-500"
					>
						<rect x="3" y="3" width="18" height="18" rx="2" />
					</svg>
				</slot>
			</div>
			<p class="mb-4 text-sm text-slate-500 dark:text-slate-400">
				{{ emptyMessage }}
			</p>
			<Button variant="primary" @click="openModal()">
				<Icon icon="plus" :size="16" />
				{{ addButtonText }}
			</Button>
		</div>

		<!-- Table -->
		<div v-else class="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-700">
			<div class="overflow-x-auto">
				<table class="w-full">
					<thead
						class="dark:border-primary/15 border-b border-primary/10 bg-primary/5 dark:bg-primary/10"
					>
						<tr>
							<th
								v-for="column in columns"
								:key="column.key"
								class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-primary/70 dark:text-primary"
								:class="column.headerClass"
							>
								{{ column.label }}
							</th>
							<th
								class="px-4 py-3 text-center text-xs font-semibold uppercase tracking-wider text-slate-600 dark:text-slate-300"
							>
								Actions
							</th>
						</tr>
					</thead>
					<tbody
						class="divide-y divide-slate-200 bg-white dark:divide-slate-700 dark:bg-slate-800"
					>
						<tr
							v-for="(item, index) in items"
							:key="index"
							class="hover:bg-slate-50 dark:hover:bg-slate-700/50"
						>
							<td
								v-for="column in columns"
								:key="column.key"
								class="px-4 py-3 text-sm text-slate-700 dark:text-slate-300"
								:class="column.cellClass"
							>
								<slot
									:name="`cell-${column.key}`"
									:item="item"
									:value="getCellValue(item, column)"
								>
									<component :is="column.component || 'span'" v-bind="column.componentProps">
										{{ formatCellValue(item, column) }}
									</component>
								</slot>
							</td>
							<td class="px-4 py-3 text-center">
								<div class="flex items-center justify-center gap-2">
									<button
										type="button"
										class="rounded p-1.5 text-primary hover:bg-primary/10 dark:text-primary-light dark:hover:bg-primary/20"
										title="Edit"
										@click="openModal(index)"
									>
										<svg
											width="16"
											height="16"
											viewBox="0 0 24 24"
											fill="none"
											stroke="currentColor"
											stroke-width="2"
										>
											<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
											<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
										</svg>
									</button>
									<button
										type="button"
										class="rounded p-1.5 text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/30"
										title="Delete"
										@click="confirmDelete(index)"
									>
										<svg
											width="16"
											height="16"
											viewBox="0 0 24 24"
											fill="none"
											stroke="currentColor"
											stroke-width="2"
										>
											<polyline points="3 6 5 6 21 6" />
											<path
												d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
											/>
										</svg>
									</button>
								</div>
							</td>
						</tr>
					</tbody>
				</table>
			</div>

			<div
				class="border-t border-slate-200 bg-slate-50 px-4 py-3 dark:border-slate-700 dark:bg-slate-900"
			>
				<button
					type="button"
					class="flex items-center gap-2 text-sm font-semibold text-primary transition-colors hover:text-primary/80 dark:text-primary dark:hover:text-primary/80"
					@click="openModal()"
				>
					<Icon icon="plus" :size="16" />
					{{ addAnotherButtonText }}
				</button>
			</div>
		</div>
	</div>

	<!-- Add/Edit Modal -->
	<FormModal
		v-model="showModal"
		:title="editingIndex !== null ? editTitle : addTitle"
		:subtitle="editingIndex !== null ? editSubtitle : addSubtitle"
		:size="modalSize"
		:submit-text="editingIndex !== null ? 'Update' : 'Add'"
		:loading="saving"
		@submit="handleSave"
		@cancel="handleCancel"
	>
		<template #form>
			<slot name="form" :form-data="formData" :editing="editingIndex !== null" />
		</template>
	</FormModal>

	<!-- Delete Confirmation Modal -->
	<Modal :is-open="showDeleteModal" :title="deleteTitle" size="sm" @close="cancelDelete">
		<div v-if="deletingIndex !== null" class="p-6">
			<p class="mb-4 text-sm text-slate-600 dark:text-slate-400">
				{{ deleteMessage }}
			</p>
			<div class="mb-4 rounded-lg bg-slate-50 p-4 dark:bg-slate-700">
				<slot name="delete-preview" :item="items[deletingIndex]">
					<pre class="text-xs text-slate-700 dark:text-slate-300">{{ items[deletingIndex] }}</pre>
				</slot>
			</div>
			<p class="text-sm font-medium text-red-600 dark:text-red-400">
				{{ deleteWarning }}
			</p>
		</div>

		<template #footer>
			<div class="flex justify-end gap-3 px-6 pb-6">
				<button
					type="button"
					class="rounded-lg border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-700 dark:text-slate-300 dark:hover:bg-slate-600"
					@click="cancelDelete"
				>
					Cancel
				</button>
				<button
					type="button"
					class="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700 dark:bg-red-700 dark:hover:bg-red-800"
					@click="handleDelete"
				>
					{{ deleteButtonText }}
				</button>
			</div>
		</template>
	</Modal>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import FormModal from "./FormModal.vue"
import Modal from "./Modal.vue"

const props = defineProps({
	// Table configuration
	title: {
		type: String,
		required: true,
	},
	columns: {
		type: Array,
		required: true,
		// Example: [{ key: 'name', label: 'Name', formatter: (value) => value }]
	},
	items: {
		type: Array,
		default: () => [],
	},

	// Empty state
	emptyMessage: {
		type: String,
		default: "No items added yet",
	},
	addButtonText: {
		type: String,
		default: "Add Item",
	},
	addAnotherButtonText: {
		type: String,
		default: "Add Another Item",
	},

	// Modal configuration
	modalSize: {
		type: String,
		default: "md",
		validator: (value) => ["sm", "md", "lg", "xl"].includes(value),
	},
	addTitle: {
		type: String,
		default: "Add New Item",
	},
	addSubtitle: {
		type: String,
		default: "Enter the item details",
	},
	editTitle: {
		type: String,
		default: "Edit Item",
	},
	editSubtitle: {
		type: String,
		default: "Update the item details",
	},

	// Delete confirmation
	deleteTitle: {
		type: String,
		default: "Delete Item",
	},
	deleteMessage: {
		type: String,
		default: "You are about to delete:",
	},
	deleteWarning: {
		type: String,
		default: "This action cannot be undone.",
	},
	deleteButtonText: {
		type: String,
		default: "Delete",
	},

	// Initial form data structure
	defaultFormData: {
		type: Object,
		default: () => ({}),
	},

	// Callbacks for custom logic
	onBeforeSave: {
		type: Function,
		default: null,
	},
	onAfterSave: {
		type: Function,
		default: null,
	},
	onBeforeDelete: {
		type: Function,
		default: null,
	},
	onAfterDelete: {
		type: Function,
		default: null,
	},
})

const emit = defineEmits(["add", "update", "delete", "save", "cancel"])

// State
const showModal = ref(false)
const showDeleteModal = ref(false)
const editingIndex = ref(null)
const deletingIndex = ref(null)
const formData = ref({})
const saving = ref(false)

// Methods
const openModal = (index = null) => {
	if (index !== null) {
		editingIndex.value = index
		formData.value = { ...props.items[index] }
	} else {
		editingIndex.value = null
		formData.value = { ...props.defaultFormData }
	}
	showModal.value = true
}

const handleCancel = () => {
	showModal.value = false
	editingIndex.value = null
	formData.value = { ...props.defaultFormData }
	emit("cancel")
}

const handleSave = async () => {
	try {
		saving.value = true

		// Call before save hook if provided
		if (props.onBeforeSave) {
			const result = await props.onBeforeSave(formData.value, editingIndex.value)
			if (result === false) {
				saving.value = false
				return
			}
			// If hook returns modified data, use it
			if (result && typeof result === "object") {
				formData.value = result
			}
		}

		if (editingIndex.value !== null) {
			emit("update", editingIndex.value, formData.value)
		} else {
			emit("add", formData.value)
		}

		emit("save", formData.value, editingIndex.value)

		// Call after save hook if provided
		if (props.onAfterSave) {
			await props.onAfterSave(formData.value, editingIndex.value)
		}

		handleCancel()
	} catch (error) {
		console.error("Save error:", error)
	} finally {
		saving.value = false
	}
}

const confirmDelete = (index) => {
	deletingIndex.value = index
	showDeleteModal.value = true
}

const handleDelete = async () => {
	if (deletingIndex.value === null) return

	try {
		// Call before delete hook if provided
		if (props.onBeforeDelete) {
			const result = await props.onBeforeDelete(
				deletingIndex.value,
				props.items[deletingIndex.value],
			)
			if (result === false) {
				return
			}
		}

		emit("delete", deletingIndex.value)

		// Call after delete hook if provided
		if (props.onAfterDelete) {
			await props.onAfterDelete(deletingIndex.value)
		}

		cancelDelete()
	} catch (error) {
		console.error("Delete error:", error)
	}
}

const cancelDelete = () => {
	showDeleteModal.value = false
	deletingIndex.value = null
}

// Cell value helpers
const getCellValue = (item, column) => {
	if (column.key.includes(".")) {
		const keys = column.key.split(".")
		let value = item
		for (const key of keys) {
			value = value?.[key]
		}
		return value
	}
	return item[column.key]
}

const formatCellValue = (item, column) => {
	const value = getCellValue(item, column)

	if (column.formatter && typeof column.formatter === "function") {
		return column.formatter(value, item)
	}

	if (value === null || value === undefined) {
		return "-"
	}

	return value
}

// Expose methods for parent component
defineExpose({
	openModal,
	formData,
})
</script>

<script>
export default {
	name: "TableManager",
}
</script>
