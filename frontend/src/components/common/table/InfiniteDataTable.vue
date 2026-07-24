<template>
	<div class="flex min-h-0 flex-1 flex-col overflow-hidden">
		<!-- Table card -->
		<div
			class="relative flex min-h-0 flex-1 flex-col overflow-hidden rounded-2xl border border-card-border bg-white shadow-card transition-all duration-300 dark:bg-sidebar-bg-dark"
		>
			<!-- Sticky header -->
			<div ref="headerScroll" class="w-full shrink-0 overflow-x-hidden">
				<table
					class="border-collapse"
					:style="{ tableLayout: 'fixed', width: '100%', minWidth: totalTableWidth + 'px' }"
				>
					<colgroup>
						<col
							v-if="selectable"
							:style="{ width: ((48 / totalTableWidth) * 100).toFixed(3) + '%' }"
						/>
						<col
							v-for="col in filteredColumns"
							:key="col.key"
							:style="{
								width: (((columnWidths[col.key] || 120) / totalTableWidth) * 100).toFixed(3) + '%',
							}"
						/>
					</colgroup>
					<thead class="border-b border-card-border bg-primary/[0.06] dark:bg-primary/10">
						<tr>
							<th v-if="selectable" class="w-12 pr-0 text-center first:pl-6">
								<Checkbox
									:model-value="isAllSelected"
									:indeterminate="isSomeSelected"
									size="sm"
									@update:model-value="toggleSelectAll"
								/>
							</th>
							<th
								v-for="column in filteredColumns"
								:key="column.key"
								:class="[
									column.headerClass,
									'group select-none py-2.5 text-left font-sans text-[11px] font-black uppercase tracking-wider text-primary/70 dark:text-primary',
									{ 'cursor-pointer': column.sortable },
								]"
								:style="{
									width: columnWidths[column.key] ? `${columnWidths[column.key]}px` : 'auto',
									minWidth: columnWidths[column.key] ? `${columnWidths[column.key]}px` : 'auto',
									maxWidth: columnWidths[column.key] ? `${columnWidths[column.key]}px` : 'auto',
									position: 'relative',
								}"
								@click="column.sortable && !resizingColumn && handleSort(column.key)"
							>
								<div class="flex items-center justify-between px-4 first:pl-6">
									<span class="inline-flex min-w-0 flex-1 items-center gap-1.5">
										<span class="truncate">{{ column.label }}</span>
										<svg
											v-if="column.sortable"
											class="flex-shrink-0 text-primary/30 transition-all dark:text-slate-500"
											:class="{
												'!text-primary opacity-100 dark:!text-primary-light': sortOrders.some(
													(s) => s.key === column.key,
												),
												'opacity-60': !sortOrders.some((s) => s.key === column.key),
												'rotate-180':
													sortOrders.find((s) => s.key === column.key)?.order === 'desc',
											}"
											width="12"
											height="12"
											viewBox="0 0 12 12"
											fill="none"
										>
											<path
												d="M6 3L6 9M6 3L3.5 5.5M6 3L8.5 5.5"
												stroke="currentColor"
												stroke-width="1.5"
												stroke-linecap="round"
												stroke-linejoin="round"
											/>
										</svg>
									</span>
								</div>
								<!-- Resize handle -->
								<div
									class="resize-handle group absolute right-0 top-0 bottom-0 w-1 cursor-col-resize"
									@mousedown="startResize($event, column.key)"
									@click.stop
								>
									<div
										class="bg-primary/15 absolute left-1/2 top-2 bottom-2 w-[1px] -translate-x-1/2 transition-colors dark:bg-slate-600"
										:class="{
											'!top-0 !bottom-0 bg-white/60 dark:bg-primary':
												resizingColumn === column.key,
										}"
									/>
									<div
										class="absolute inset-y-0 -left-1 -right-1 w-3 hover:bg-white/10 dark:hover:bg-primary/5"
									/>
								</div>
							</th>
						</tr>
					</thead>
				</table>
			</div>

			<!-- Scrollable body (scroll triggers load-more) -->
			<div
				ref="bodyScroll"
				class="scrolling-touch scrollbar-thin scrollbar-thumb-slate-200 dark:scrollbar-thumb-slate-800 min-h-0 w-full flex-1 overflow-x-auto overflow-y-auto"
				@scroll="onBodyScroll"
			>
				<table
					class="border-collapse"
					:style="{ tableLayout: 'fixed', width: '100%', minWidth: totalTableWidth + 'px' }"
				>
					<colgroup>
						<col
							v-if="selectable"
							:style="{ width: ((48 / totalTableWidth) * 100).toFixed(3) + '%' }"
						/>
						<col
							v-for="col in filteredColumns"
							:key="col.key"
							:style="{
								width: (((columnWidths[col.key] || 120) / totalTableWidth) * 100).toFixed(3) + '%',
							}"
						/>
					</colgroup>
					<tbody class="divide-y divide-slate-200/70 dark:divide-slate-700/60">
						<tr
							v-for="(row, index) in data"
							:key="row[rowKey] || index"
							class="cursor-pointer border-b border-slate-200/70 transition-all duration-200 last:border-b-0 hover:bg-primary/[0.02] hover:shadow-[inset_3px_0_0_0_var(--color-primary,#6742CF)] dark:border-slate-700/60 dark:hover:bg-primary/[0.06] dark:hover:shadow-[inset_3px_0_0_0_var(--color-primary-light,#C4B4FF)]"
							:class="{
								'dark:hover:bg-primary/15 bg-primary/[0.03] hover:bg-primary/[0.05] dark:bg-primary/10':
									isRowSelected(row),
							}"
							@click="handleRowClick(row, $event)"
						>
							<td v-if="selectable" class="w-12 pr-0 text-center first:pl-6" @click.stop>
								<Checkbox
									:model-value="isRowSelected(row)"
									size="sm"
									@update:model-value="toggleSelectRow(row)"
								/>
							</td>
							<td
								v-for="column in filteredColumns"
								:key="column.key"
								:class="[
									column.cellClass,
									'text-slate-650 px-4 py-2 font-sans text-sm first:pl-6 dark:text-slate-300',
								]"
								:style="{
									width: columnWidths[column.key] ? `${columnWidths[column.key]}px` : 'auto',
									minWidth: columnWidths[column.key] ? `${columnWidths[column.key]}px` : 'auto',
									maxWidth: columnWidths[column.key] ? `${columnWidths[column.key]}px` : 'auto',
								}"
							>
								<slot :name="`cell-${column.key}`" :row="row" :value="row[column.key]">
									<template v-if="Array.isArray(row[column.key])">
										{{ formatArrayValue(row[column.key]) || "-" }}
									</template>
									<template
										v-else-if="
											column.key === 'full_name' ||
											column.key === 'party_name' ||
											column.type === 'UserProfile'
										"
									>
										<div class="flex items-center gap-3">
											<div
												class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full border-2 border-slate-200 font-sans text-sm font-bold text-white shadow-sm dark:border-slate-700"
												:style="{
													background: getAvatarColor(row[column.key] || row.name || ''),
												}"
											>
												{{ getInitials(row[column.key] || row.name || "") }}
											</div>
											<div class="flex flex-col gap-0.5">
												<div class="font-semibold text-slate-900 dark:text-white">
													{{ row[column.key] || row.name }}
												</div>
												<div class="text-xs text-slate-400 dark:text-slate-500">
													ID: {{ row.name }}
												</div>
											</div>
										</div>
									</template>
									<template
										v-else-if="
											column.key === 'status' ||
											column.type === 'Status' ||
											column.type === 'StatusBadge'
										"
									>
										<StatusBadge :status="getStatusText(row[column.key])" size="sm" />
									</template>
									<template v-else-if="column.type === 'Badge' || column.type === 'TagBadge'">
										<TagBadge :label="row[column.key]" />
									</template>
									<template v-else-if="column.type === 'ItemTitle'">
										<div class="flex items-center gap-3">
											<div
												class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl border-2 border-slate-200 font-sans text-sm font-bold text-white shadow-sm dark:border-slate-700"
												:style="{ background: getAvatarColor(row[column.key] || row.name || '') }"
											>
												{{ getInitials(row[column.key] || row.name || "") }}
											</div>
											<div class="flex flex-col gap-0.5">
												<div class="font-semibold text-slate-900 dark:text-white">
													{{ row[column.key] || row.name }}
												</div>
												<div class="text-xs text-slate-400 dark:text-slate-500">
													{{ row.name }}
												</div>
											</div>
										</div>
									</template>
									<template v-else-if="column.type === 'Check'">
										<Icon
											v-if="Number(row[column.key]) === 1"
											icon="check-circle"
											:size="16"
											class="text-emerald-500 dark:text-emerald-400"
										/>
										<Icon
											v-else
											icon="close-circle-outline"
											:size="16"
											class="text-slate-300 dark:text-slate-600"
										/>
									</template>
									<template
										v-else-if="
											row[column.key] === null ||
											row[column.key] === undefined ||
											row[column.key] === ''
										"
									>
										-
									</template>
									<template v-else-if="column.key === 'name'">
										<span class="font-bold text-primary dark:text-primary">{{
											row[column.key]
										}}</span>
									</template>
									<template v-else-if="column.type === 'Date'">
										<DateDisplay :date="row[column.key]" />
									</template>
									<template v-else-if="column.type === 'Datetime'">
										<DateTimeDisplay :datetime="row[column.key]" />
									</template>
									<template v-else-if="column.type === 'Time'">
										<TimeDisplay :time="row[column.key]" />
									</template>
									<template v-else-if="column.type === 'Currency'">
										<CurrencyDisplay :value="row[column.key]" />
									</template>
									<template v-else-if="column.type === 'Percent'">
										<PercentageDisplay :value="row[column.key]" />
									</template>
									<template v-else-if="column.type === 'Float'">
										<FloatDisplay :value="row[column.key]" />
									</template>
									<template v-else-if="column.type === 'Int'">
										{{ formatNumber(row[column.key], { maximumFractionDigits: 0 }) }}
									</template>
									<template v-else-if="column.type === 'Link'">
										<LinkDisplay
											:value="row[column.key]"
											:doctype="column.options"
											:show-info-icon="column.showInfoIcon ?? false"
										/>
									</template>
									<template v-else>
										{{ row[column.key] }}
									</template>
								</slot>
							</td>
						</tr>

						<!-- Empty state -->
						<tr v-if="hasFetched && !loading && data.length === 0">
							<td :colspan="filteredColumns.length" class="border-none px-6 py-16 text-center">
								<slot name="empty">
									<div class="flex flex-col items-center gap-4">
										<svg width="48" height="48" viewBox="0 0 48 48" fill="none">
											<rect
												width="48"
												height="48"
												rx="24"
												fill="#F1F5F9"
												class="dark:fill-slate-800"
											/>
											<path
												d="M24 20V28M20 24H28"
												stroke="#94A3B8"
												stroke-width="2"
												stroke-linecap="round"
												class="dark:stroke-slate-500"
											/>
										</svg>
										<p
											class="dark:text-slate-450 m-0 font-sans text-sm font-medium text-slate-500"
										>
											{{ emptyText }}
										</p>
									</div>
								</slot>
							</td>
						</tr>

						<!-- Loading-more sentinel row (shows while fetching next page) -->
						<tr v-if="loadingMore">
							<td :colspan="filteredColumns.length" class="border-none py-4 text-center">
								<div
									class="inline-flex items-center gap-2 text-sm text-slate-400 dark:text-slate-500"
								>
									<span
										class="h-4 w-4 animate-spin rounded-full border-2 border-slate-200 border-t-primary dark:border-slate-700 dark:border-t-primary-light"
									/>
									Loading more…
								</div>
							</td>
						</tr>
					</tbody>
				</table>
			</div>

			<!-- Initial load overlay -->
			<LoadingOverlay :active="loading || !hasFetched" text="Fetching records..." />

			<!-- Count bar at the bottom of the card -->
			<div
				v-if="hasFetched && totalCount !== null && data.length > 0"
				class="flex shrink-0 items-center justify-end border-t border-slate-100 px-5 py-2 dark:border-slate-700/60"
			>
				<span class="font-sans text-xs text-slate-400 dark:text-slate-500">
					<strong class="font-bold text-primary/70 dark:text-primary-light/70">{{
						data.length
					}}</strong>
					of
					<strong class="font-bold text-primary/70 dark:text-primary-light/70">{{
						totalCount
					}}</strong>
					{{ itemName }}
				</span>
			</div>
		</div>
	</div>
</template>

<script>
import { useResponsive } from "../../../composables/useResponsive"
import LoadingOverlay from "../LoadingOverlay.vue"
import Checkbox from "../../fields/Checkbox.vue"
import StatusBadge from "../StatusBadge.vue"
import TagBadge from "../TagBadge.vue"
import DateDisplay from "../../display_fields/DateDisplay.vue"
import DateTimeDisplay from "../../display_fields/DateTimeDisplay.vue"
import TimeDisplay from "../../display_fields/TimeDisplay.vue"
import CurrencyDisplay from "../../display_fields/CurrencyDisplay.vue"
import PercentageDisplay from "../../display_fields/PercentageDisplay.vue"
import FloatDisplay from "../../display_fields/FloatDisplay.vue"
import LinkDisplay from "../../display_fields/LinkDisplay.vue"
import { formatNumber } from "../../../utils/forms/formatters"

const SCROLL_THRESHOLD = 120

export default {
	name: "InfiniteDataTable",
	components: {
		LoadingOverlay,
		Checkbox,
		StatusBadge,
		TagBadge,
		DateDisplay,
		DateTimeDisplay,
		TimeDisplay,
		CurrencyDisplay,
		PercentageDisplay,
		FloatDisplay,
		LinkDisplay,
	},

	props: {
		loading: { type: Boolean, default: false },
		loadingMore: { type: Boolean, default: false },
		columns: { type: Array, required: true },
		data: { type: Array, required: true },
		rowKey: { type: String, default: "name" },
		hasMore: { type: Boolean, default: false },
		sortOrders: { type: Array, default: () => [] },
		totalCount: { type: Number, default: null },
		itemName: { type: String, default: "items" },
		emptyText: { type: String, default: "No data available" },
		visibleColumns: { type: Array, default: null },
		selectable: { type: Boolean, default: false },
	},

	emits: ["sort", "row-click", "load-more", "selection-change"],

	setup() {
		const { isMobile } = useResponsive()
		return { isMobile }
	},

	data() {
		return {
			selectedRowKeys: [],
			columnWidths: {},
			resizingColumn: null,
			startX: 0,
			startWidth: 0,
			hasFetched: false,
		}
	},

	computed: {
		filteredColumns() {
			if (!this.visibleColumns || !this.visibleColumns.length) return this.columns
			return this.columns.filter((c) => this.visibleColumns.includes(c.key))
		},
		isAllSelected() {
			return (
				this.data.length > 0 &&
				this.data.every((r) => this.selectedRowKeys.includes(r[this.rowKey]))
			)
		},
		isSomeSelected() {
			return this.selectedRowKeys.length > 0 && !this.isAllSelected
		},
		totalTableWidth() {
			let w = this.selectable ? 48 : 0
			this.filteredColumns.forEach((col) => {
				w += this.columnWidths[col.key] || 120
			})
			return Math.max(400, w)
		},
	},

	watch: {
		filteredColumns: {
			handler() {
				this.initializeColumnWidths()
			},
			immediate: true,
		},
		data(newVal, oldVal) {
			if (oldVal && oldVal.length === 0 && newVal.length > 0) {
				this.columnWidths = {}
				this.initializeColumnWidths()
			}
		},
		loading(newVal, oldVal) {
			if (oldVal === true && newVal === false) this.hasFetched = true
		},
	},

	mounted() {
		this.initializeColumnWidths()
	},

	methods: {
		formatNumber,

		// ── Scroll ────────────────────────────────────────────────────────
		onBodyScroll(event) {
			if (this.$refs.headerScroll) {
				this.$refs.headerScroll.scrollLeft = event.target.scrollLeft
			}
			const el = event.target
			const nearBottom = el.scrollTop + el.clientHeight >= el.scrollHeight - SCROLL_THRESHOLD
			if (nearBottom && !this.loading && !this.loadingMore && this.hasMore) {
				this.$emit("load-more")
			}
		},

		// ── Sort ──────────────────────────────────────────────────────────
		handleSort(key) {
			const existing = this.sortOrders.find((s) => s.key === key)
			const newOrders = existing
				? this.sortOrders.map((s) =>
						s.key === key ? { ...s, order: s.order === "asc" ? "desc" : "asc" } : s,
					)
				: [...this.sortOrders, { key, order: "asc" }]
			this.$emit("sort", newOrders)
		},

		// ── Row click ─────────────────────────────────────────────────────
		handleRowClick(row, event) {
			const interactive = ["INPUT", "A", "BUTTON", "LABEL"]
			if (
				interactive.includes(event.target.tagName) ||
				event.target.closest("a,button,input,label")
			)
				return
			this.$emit("row-click", row)
		},

		// ── Selection ─────────────────────────────────────────────────────
		isRowSelected(row) {
			return this.selectedRowKeys.includes(row[this.rowKey])
		},
		toggleSelectAll() {
			this.selectedRowKeys = this.isAllSelected ? [] : this.data.map((r) => r[this.rowKey])
			this.$emit("selection-change", [...this.selectedRowKeys])
		},
		toggleSelectRow(row) {
			const key = row[this.rowKey]
			const idx = this.selectedRowKeys.indexOf(key)
			idx === -1 ? this.selectedRowKeys.push(key) : this.selectedRowKeys.splice(idx, 1)
			this.$emit("selection-change", [...this.selectedRowKeys])
		},

		// ── Column widths ─────────────────────────────────────────────────
		initializeColumnWidths() {
			this.filteredColumns.forEach((col) => {
				if (!this.columnWidths[col.key]) {
					this.columnWidths[col.key] = col.width || this.calculateColumnWidth(col)
				}
			})
		},
		calculateColumnWidth(column) {
			const canvas = document.createElement("canvas")
			const ctx = canvas.getContext("2d")
			ctx.font = "11px Inter, system-ui, sans-serif"
			let max = ctx.measureText(column.label || "").width
			this.data.slice(0, 100).forEach((row) => {
				const v = row[column.key]
				const str = v == null ? "-" : Array.isArray(v) ? this.formatArrayValue(v) : String(v)
				const w = ctx.measureText(str).width
				if (w > max) max = w
			})
			const pad = 32,
				buf = 20,
				icon = column.sortable ? 20 : 0
			return Math.max(100, Math.min(400, Math.ceil(max) + pad + buf + icon))
		},

		// ── Column resize ─────────────────────────────────────────────────
		startResize(event, key) {
			event.preventDefault()
			event.stopPropagation()
			this.resizingColumn = key
			this.startX = event.clientX
			this.startWidth = this.columnWidths[key] || 150
			const move = (e) => {
				if (!this.resizingColumn) return
				this.columnWidths[this.resizingColumn] = Math.max(
					60,
					this.startWidth + e.clientX - this.startX,
				)
			}
			const up = () => {
				this.resizingColumn = null
				document.removeEventListener("mousemove", move)
				document.removeEventListener("mouseup", up)
				document.body.style.cursor = ""
				document.body.style.userSelect = ""
			}
			document.addEventListener("mousemove", move)
			document.addEventListener("mouseup", up)
			document.body.style.cursor = "col-resize"
			document.body.style.userSelect = "none"
		},

		// ── Helpers ───────────────────────────────────────────────────────
		formatArrayValue(arr) {
			if (!arr?.length) return "-"
			if (typeof arr[0] === "object" && arr[0] !== null) {
				return arr
					.map((item) => {
						const keys = Object.keys(item).filter((k) => k !== "name" && k !== "parent")
						return keys.length ? String(item[keys[0]] ?? "") : item.name || ""
					})
					.filter(Boolean)
					.join(", ")
			}
			return arr.join(", ")
		},
		getInitials(name) {
			return (name || "")
				.split(" ")
				.filter((n) => n)
				.map((n) => n[0])
				.join("")
				.substring(0, 2)
				.toUpperCase()
		},
		getAvatarColor(name) {
			const colors = [
				"linear-gradient(135deg,#1e3a8a,#1e40af)",
				"linear-gradient(135deg,#059669,#047857)",
				"linear-gradient(135deg,#dc2626,#b91c1c)",
				"linear-gradient(135deg,#7c3aed,#6d28d9)",
				"linear-gradient(135deg,#ea580c,#c2410c)",
				"linear-gradient(135deg,#0891b2,#0e7490)",
				"linear-gradient(135deg,#db2777,#be185d)",
				"linear-gradient(135deg,#ca8a04,#a16207)",
			]
			let h = 0
			for (let i = 0; i < (name || "").length; i++) h = name.charCodeAt(i) + ((h << 5) - h)
			return colors[Math.abs(h) % colors.length]
		},
		getStatusText(value) {
			if (typeof value === "boolean" || typeof value === "number")
				return value ? "Active" : "Inactive"
			return value || "Unknown"
		},
	},
}
</script>

<style scoped>
.resize-handle {
	z-index: 20;
}
.resize-handle:hover > div:first-child {
	background-color: rgb(255 255 255 / 50%);
}
.dark .resize-handle:hover > div:first-child {
	background-color: var(--color-primary, #6742cf);
}
</style>
