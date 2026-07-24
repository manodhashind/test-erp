<template>
	<div class="dynamic-documents-tab">
		<!-- Filter Bar -->
		<div class="filter-bar">
			<SearchField
				v-model="searchQuery"
				placeholder="Search by document name..."
				variant="transparent"
				custom-class="custom-search-field"
			/>

			<div class="divider" />

			<div class="status-filters">
				<span class="filter-label">STATUS:</span>
				<button
					v-for="status in ['All', 'Verified', 'Pending', 'Draft']"
					:key="status"
					class="status-pill"
					:class="{ active: selectedStatus === status }"
					@click="selectedStatus = status"
				>
					{{ status }}
				</button>
			</div>

			<div class="divider" />

			<div class="type-filter">
				<span class="filter-label">TYPE:</span>
				<SelectField v-model="selectedType" :options="typeOptions" class="custom-select-field" />
			</div>

			<button class="btn-filter-icon">
				<svg
					width="20"
					height="20"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
				>
					<line x1="4" y1="21" x2="4" y2="14" />
					<line x1="4" y1="10" x2="4" y2="3" />
					<line x1="12" y1="21" x2="12" y2="12" />
					<line x1="12" y1="8" x2="12" y2="3" />
					<line x1="20" y1="21" x2="20" y2="16" />
					<line x1="20" y1="12" x2="20" y2="3" />
					<line x1="1" y1="14" x2="7" y2="14" />
					<line x1="9" y1="8" x2="15" y2="8" />
					<line x1="17" y1="16" x2="23" y2="16" />
				</svg>
			</button>
		</div>

		<!-- Loading State -->
		<div v-if="loading" class="loading-state">
			<div class="spinner" />
			<p>Loading documents...</p>
		</div>

		<!-- Error State -->
		<div v-else-if="error" class="error-state">
			<p>{{ error }}</p>
			<button class="btn-secondary" @click="fetchDocuments">Retry</button>
		</div>

		<!-- Empty State -->
		<div v-else-if="filteredDocuments.length === 0" class="empty-state">
			<svg
				width="48"
				height="48"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="1.5"
			>
				<path d="M13 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V9l-7-7z" />
				<path d="M13 2v7h7" />
			</svg>
			<p>No documents found.</p>
		</div>

		<!-- Documents Grid -->
		<div v-else class="documents-grid">
			<div v-for="doc in processedDocuments" :key="doc.name" class="document-card">
				<div class="card-header">
					<div class="doc-icon" :class="doc.iconClass">
						<span v-if="doc.iconText" class="icon-text">{{ doc.iconText }}</span>
						<svg
							v-else
							width="20"
							height="20"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
						>
							<path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
							<polyline points="7 10 12 15 17 10" />
							<line x1="12" y1="15" x2="12" y2="3" />
						</svg>
					</div>
					<span class="status-badge" :class="doc.statusClass">{{ doc.status }}</span>
				</div>

				<div class="card-body">
					<h4 class="doc-name" :title="doc.file_name">
						{{ doc.file_name }}
					</h4>
					<div class="doc-meta">
						<span class="type-pill">{{ doc.typeLabel }}</span>
						<span class="file-size">
							<svg
								width="12"
								height="12"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
							>
								<path
									d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48"
								/>
							</svg>
							{{ doc.size }}
						</span>
					</div>
				</div>

				<div class="card-footer">
					<span class="doc-date">{{ formatDate(doc.creation) }}</span>
					<div class="card-actions">
						<button class="icon-btn" title="View">
							<svg
								width="16"
								height="16"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
							>
								<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
								<circle cx="12" cy="12" r="3" />
							</svg>
						</button>
						<button class="icon-btn" title="More actions">
							<svg
								width="16"
								height="16"
								viewBox="0 0 24 24"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
							>
								<circle cx="12" cy="12" r="1" />
								<circle cx="12" cy="5" r="1" />
								<circle cx="12" cy="19" r="1" />
							</svg>
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue"
import { ApiService } from "../../services/api"
import SearchField from "../fields/essential/SearchField.vue"
import SelectField from "../fields/core/SelectField.vue"

const props = defineProps({
	doctype: {
		type: String,
		required: true,
	},
	docname: {
		type: String,
		required: true,
	},
})

const documents = ref([])
const loading = ref(false)
const error = ref(null)

const searchQuery = ref("")
const selectedStatus = ref("All")
const selectedType = ref("All Types")

const typeOptions = [
	{ label: "All Types", value: "All Types" },
	{ label: "PDF", value: "PDF" },
	{ label: "Image", value: "Image" },
	{ label: "Document", value: "Document" },
]

// Generate some mock data attributes that aren't provided by the basic API
const mockEnrichment = (docs) => {
	return docs.map((doc) => {
		const ext = doc.file_name?.split(".").pop()?.toLowerCase() || ""

		// Assign mock status randomly for demonstration, normally this comes from API
		const statuses = ["Verified", "Pending", "Draft"]
		const mockStatus = statuses[doc.name.charCodeAt(doc.name.length - 1) % 3]

		let iconClass = "icon-default"
		let iconText = ""
		let typeLabel = "MISC"

		if (ext === "pdf") {
			iconClass = "icon-pdf"
			iconText = "PDF"
			typeLabel = doc.file_name.toLowerCase().includes("lading") ? "BOL" : "INV"
		} else if (["jpg", "jpeg", "png"].includes(ext)) {
			iconClass = "icon-image"
			iconText = "IMG"
			typeLabel = "POD"
		} else if (["doc", "docx"].includes(ext)) {
			iconClass = "icon-doc"
			iconText = "DOC"
		}

		return {
			...doc,
			status: mockStatus,
			statusClass: `status-${mockStatus.toLowerCase()}`,
			iconClass,
			iconText,
			typeLabel,
			size: `${(Math.random() * 3 + 0.1).toFixed(1)} MB`, // Mock file size
		}
	})
}

const fetchDocuments = async () => {
	if (!props.doctype || !props.docname) return

	loading.value = true
	error.value = null

	try {
		const response = await ApiService.get("frappe.client.get_list", {
			doctype: "File",
			filters: JSON.stringify({
				attached_to_doctype: props.doctype,
				attached_to_name: props.docname,
			}),
			fields: JSON.stringify(["name", "file_name", "file_url", "creation", "owner"]),
			limit_page_length: 100,
		})
		if (response && response.message) {
			documents.value = response.message
		} else {
			documents.value = []
		}
	} catch (err) {
		console.error("Failed to fetch documents:", err)
		error.value = err.message || "Failed to load documents"
	} finally {
		loading.value = false
	}
}

onMounted(() => {
	fetchDocuments()
})

watch(
	() => [props.doctype, props.docname],
	() => {
		fetchDocuments()
	},
)

const processedDocuments = computed(() => {
	let filtered = documents.value

	if (searchQuery.value) {
		const query = searchQuery.value.toLowerCase()
		filtered = filtered.filter((doc) => doc.file_name?.toLowerCase().includes(query))
	}

	// Apply enrichment
	filtered = mockEnrichment(filtered)

	// Filter by status (mocked)
	if (selectedStatus.value !== "All") {
		filtered = filtered.filter((doc) => doc.status === selectedStatus.value)
	}

	return filtered
})

const filteredDocuments = computed(() => processedDocuments.value)

const formatDate = (dateString) => {
	if (!dateString) return ""
	return new Date(dateString).toLocaleDateString("en-US", {
		year: "numeric",
		month: "short",
		day: "numeric",
	})
}
</script>

<style scoped>
.dynamic-documents-tab {
	background: #f8fafc;
	padding: 20px;
}

/* Filter Bar */
.filter-bar {
	display: flex;
	align-items: center;
	background: white;
	border: 1px solid #e2e8f0;
	border-radius: 12px;
	padding: 12px 16px;
	margin-bottom: 24px;
	box-shadow: 0 1px 3px rgb(0 0 0 / 2%);
}

/* Integration overrides for standard fields */
:deep(.custom-search-field) {
	flex: 1;
	max-width: none;
}

:deep(.custom-search-field .field-control) {
	background: transparent;
	border: none;
	min-height: 24px;
}

:deep(.custom-search-field .field-control:focus-within) {
	box-shadow: none;
}

:deep(.custom-select-field) {
	min-width: 130px;
	margin-bottom: 0;
}

:deep(.custom-select-field .base-field-wrapper) {
	margin-bottom: 0;
}

:deep(.custom-select-field .field-control) {
	background: transparent;
	border: none;
	min-height: 24px;
}

:deep(.custom-select-field .field-control:focus-within) {
	box-shadow: none;
}

.divider {
	width: 1px;
	height: 24px;
	background-color: #e2e8f0;
	margin: 0 20px;
}

.filter-label {
	font-size: 12px;
	font-weight: 700;
	color: #64748b;
	margin-right: 12px;
	font-family: Inter, sans-serif;
	letter-spacing: 0.5px;
}

.status-filters {
	display: flex;
	align-items: center;
	gap: 8px;
}

.status-pill {
	background: transparent;
	border: 1px solid #e2e8f0;
	border-radius: 6px;
	padding: 6px 16px;
	font-size: 13px;
	font-weight: 500;
	color: #475569;
	cursor: pointer;
	font-family: Inter, sans-serif;
	transition: all 0.2s;
}

.status-pill:hover {
	background: #f8fafc;
}

.status-pill.active {
	background: rgb(var(--color-primary-rgb, 103, 66, 207), 0.1);
	border-color: rgb(var(--color-primary-rgb, 103, 66, 207), 0.3);
	color: var(--color-primary, #6742cf);
	font-weight: 600;
}

.type-filter {
	display: flex;
	align-items: center;
}

.btn-filter-icon {
	background: transparent;
	border: none;
	color: #64748b;
	margin-left: 20px;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 4px;
	border-radius: 4px;
}

.btn-filter-icon:hover {
	background: #f1f5f9;
	color: #0f172a;
}

/* Grid & Cards */
.documents-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
	gap: 20px;
}

.document-card {
	background: white;
	border: 1px solid #e2e8f0;
	border-radius: 16px;
	padding: 20px;
	display: flex;
	flex-direction: column;
	transition: all 0.2s;
	box-shadow: 0 1px 3px rgb(0 0 0 / 2%);
}

.document-card:hover {
	box-shadow: 0 8px 16px -4px rgb(0 0 0 / 5%);
	border-color: #cbd5e1;
	transform: translateY(-2px);
}

.card-header {
	display: flex;
	justify-content: space-between;
	align-items: flex-start;
	margin-bottom: 16px;
}

.doc-icon {
	width: 44px;
	height: 44px;
	border-radius: 10px;
	display: flex;
	align-items: center;
	justify-content: center;
	font-weight: 800;
	font-size: 12px;
	letter-spacing: 0.5px;
}

.icon-pdf {
	background: #fee2e2;
	color: #dc2626;
}

.icon-image {
	background: #e0e7ff;
	color: #4f46e5;
}

.icon-doc {
	background: #f1f5f9;
	color: #475569;
}

.icon-default {
	background: #f1f5f9;
	color: #64748b;
}

.status-badge {
	padding: 4px 10px;
	border-radius: 4px;
	font-size: 12px;
	font-weight: 600;
	font-family: Inter, sans-serif;
}

.status-verified {
	background: #ecfdf5;
	color: #059669;
}

.status-pending {
	background: #fffbeb;
	color: #d97706;
}

.status-draft {
	background: #f8fafc;
	color: #64748b;
}

.card-body {
	margin-bottom: 24px;
	flex: 1;
}

.doc-name {
	font-size: 16px;
	font-weight: 700;
	color: #0f172a;
	margin: 0 0 12px;
	font-family: Inter, sans-serif;
	line-height: 1.4;
	word-break: break-word;
}

.doc-meta {
	display: flex;
	align-items: center;
	gap: 12px;
}

.type-pill {
	background: #f1f5f9;
	color: #64748b;
	padding: 4px 8px;
	border-radius: 4px;
	font-size: 11px;
	font-weight: 700;
	letter-spacing: 0.5px;
}

.file-size {
	display: flex;
	align-items: center;
	gap: 4px;
	font-size: 13px;
	color: #94a3b8;
	font-weight: 500;
}

.card-footer {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding-top: 16px;
	border-top: 1px solid #f1f5f9;
}

.doc-date {
	font-size: 13px;
	color: #94a3b8;
	font-weight: 500;
	font-family: Inter, sans-serif;
}

.card-actions {
	display: flex;
	gap: 8px;
}

.icon-btn {
	width: 32px;
	height: 32px;
	border-radius: 8px;
	background: #f8fafc;
	border: 1px solid transparent;
	color: #64748b;
	display: flex;
	align-items: center;
	justify-content: center;
	cursor: pointer;
	transition: all 0.2s;
}

.icon-btn:hover {
	background: white;
	border-color: #e2e8f0;
	color: #0f172a;
	box-shadow: 0 1px 2px rgb(0 0 0 / 5%);
}

/* Loading & Empty States */
.loading-state,
.error-state,
.empty-state {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	padding: 64px 0;
	color: #64748b;
	font-family: Inter, sans-serif;
}

.spinner {
	width: 32px;
	height: 32px;
	border: 3px solid #e2e8f0;
	border-top-color: var(--color-primary, #6742cf);
	border-radius: 50%;
	animation: spin 0.8s linear infinite;
	margin-bottom: 16px;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

.btn-secondary {
	margin-top: 16px;
	background: white;
	color: #475569;
	border: 1px solid #cbd5e1;
	border-radius: 6px;
	padding: 8px 16px;
	font-size: 14px;
	font-weight: 600;
	cursor: pointer;
	font-family: Inter, sans-serif;
}
</style>
