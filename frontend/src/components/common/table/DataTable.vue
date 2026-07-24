<template>
	<div class="flex min-h-0 flex-1 flex-col overflow-hidden">
		<div
			class="relative flex min-h-0 flex-1 flex-col overflow-hidden rounded-2xl border border-card-border bg-white shadow-card transition-all duration-300 dark:bg-sidebar-bg-dark"
		>
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
						<col
							v-if="showActionsColumn"
							:style="{ width: ((60 / totalTableWidth) * 100).toFixed(3) + '%' }"
						/>
						<col
							v-if="showTimeColumn"
							:style="{ width: ((timeColumnWidth / totalTableWidth) * 100).toFixed(3) + '%' }"
						/>
					</colgroup>
					<thead class="border-b border-card-border bg-table-header">
						<!-- Skeleton header: no columns loaded yet -->
						<tr v-if="!hasFetched && filteredColumns.length === 0">
							<th v-if="selectable" class="w-12 bg-table-header pl-6">
								<div class="skeleton-header-cell h-4 w-4 rounded bg-slate-200 dark:bg-slate-700" />
							</th>
							<th
								v-for="i in skeletonColumnCount"
								:key="i"
								class="bg-table-header px-4 py-3 first:pl-6"
							>
								<div
									class="skeleton-header-cell h-2.5 rounded-full bg-slate-200 dark:bg-slate-700"
									:style="{ width: skeletonHeaderWidths[(i - 1) % skeletonHeaderWidths.length] }"
								/>
							</th>
						</tr>
						<tr v-else>
							<th v-if="selectable" class="w-12 bg-table-header pr-0 text-center first:pl-6">
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
									'group select-none bg-table-header py-2.5 text-left font-sans text-[11px] font-black uppercase tracking-wider text-primary/70 dark:text-primary',
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
									<!-- Skeleton pill while data hasn't loaded yet -->
									<div
										v-if="!hasFetched"
										class="skeleton-header-cell h-2.5 rounded-full bg-slate-200 dark:bg-slate-700"
										:style="{
											width:
												skeletonHeaderWidths[
													filteredColumns.indexOf(column) % skeletonHeaderWidths.length
												],
										}"
									/>
									<span v-else class="inline-flex min-w-0 flex-1 items-center gap-1.5">
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
							<th v-if="showActionsColumn" class="bg-table-header px-4 py-2.5" />
							<th
								v-if="showTimeColumn"
								class="sticky right-0 isolate z-10 select-none whitespace-nowrap bg-table-header py-2.5 pr-6 pl-4 text-right font-sans text-[11px] font-black uppercase tracking-wider text-primary/70 will-change-transform dark:text-primary"
								:style="{ width: `${timeColumnWidth}px`, minWidth: `${timeColumnWidth}px` }"
							>
								<button
									v-if="hasFetched"
									type="button"
									class="inline-flex cursor-pointer items-center gap-1 bg-transparent p-0 font-sans text-[11px] font-black uppercase tracking-wider text-primary/70 transition-colors hover:text-primary dark:text-primary dark:hover:text-primary-light"
									:title="`Showing ${timeColumnLabel} time — click to switch`"
									@click="toggleTimeColumnMode"
								>
									{{ timeColumnLabel }}
									<Icon icon="swap-horizontal" :size="12" />
								</button>
								<div
									v-else
									class="skeleton-header-cell ml-auto h-2.5 w-14 rounded-full bg-slate-200 dark:bg-slate-700"
								/>
							</th>
						</tr>
					</thead>
				</table>
			</div>
			<div
				ref="bodyScroll"
				class="scrolling-touch table-scroll min-h-0 w-full flex-1"
				:class="hasFetched ? 'overflow-x-auto overflow-y-auto' : 'overflow-hidden'"
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
						<col
							v-if="showActionsColumn"
							:style="{ width: ((60 / totalTableWidth) * 100).toFixed(3) + '%' }"
						/>
						<col
							v-if="showTimeColumn"
							:style="{ width: ((timeColumnWidth / totalTableWidth) * 100).toFixed(3) + '%' }"
						/>
					</colgroup>
					<tbody class="divide-y divide-slate-200/70 dark:divide-slate-700/60">
						<TableSkeletonLoader
							v-if="!hasFetched"
							:rows="entriesPerPage"
							:column-count="filteredColumns.length + (showActionsColumn ? 1 : 0)"
							:selectable="selectable"
						/>
						<template v-else>
							<tr
								v-for="(row, index) in data"
								:key="row[rowKey] || index"
								class="group cursor-pointer border-b border-slate-200/70 transition-all duration-200 last:border-b-0 hover:bg-primary/[0.02] hover:shadow-[inset_3px_0_0_0_var(--color-primary,#6742CF)] dark:border-slate-700/60 dark:hover:bg-primary/[0.06] dark:hover:shadow-[inset_3px_0_0_0_var(--color-primary-light,#C4B4FF)]"
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
													class="avatar-badge flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full font-sans text-sm font-bold"
													:class="`avatar-color-${getAvatarColorIndex(
														row[column.displayKey || column.key] || row.name || '',
													)}`"
												>
													{{ getInitials(row[column.displayKey || column.key] || row.name || "") }}
												</div>
												<div class="flex flex-col gap-0.5">
													<div class="font-semibold text-slate-900 dark:text-white">
														{{ row[column.displayKey || column.key] || row.name }}
													</div>
													<div class="text-xs text-slate-400 dark:text-slate-500">
														{{ column.subKey ? row[column.subKey] : row.name }}
													</div>
												</div>
											</div>
										</template>
										<template v-else-if="column.type === 'ItemTitle'">
											<div class="flex items-center gap-3">
												<div
													class="avatar-badge flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl font-sans text-sm font-bold"
													:class="`avatar-color-${getAvatarColorIndex(row[column.key] || row.name || '')}`"
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
								<td v-if="showActionsColumn" class="w-[60px] pr-6 text-right">
									<slot name="actions" :row="row" />
								</td>
								<td
									v-if="showTimeColumn"
									class="sticky right-0 isolate z-10 whitespace-nowrap bg-white pr-6 pl-4 text-right font-sans text-sm text-slate-500 transition-all duration-200 will-change-transform group-hover:bg-[#fafcff] dark:bg-sidebar-bg-dark dark:text-slate-400 dark:group-hover:bg-slate-800/60"
									:class="{
										'!bg-primary/5 dark:!bg-primary/10': isRowSelected(row),
									}"
									:style="{
										width: `${timeColumnWidth}px`,
										minWidth: `${timeColumnWidth}px`,
										maxWidth: `${timeColumnWidth}px`,
									}"
									:title="row[timeColumnField] ? formatDateTime(row[timeColumnField]) : ''"
								>
									{{ (nowTick && formatRelativeTime(row[timeColumnField])) || "-" }}
								</td>
							</tr>
							<tr v-if="!loading && data.length === 0">
								<td
									:colspan="
										filteredColumns.length + (showActionsColumn ? 1 : 0) + (showTimeColumn ? 1 : 0)
									"
									class="border-none py-16 px-6 text-center"
								>
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
						</template>
					</tbody>
				</table>
			</div>

			<!-- Re-fetch overlay (only after initial load is done) -->
			<LoadingOverlay :active="loading && hasFetched" text="Fetching records..." />
		</div>

		<!-- Bottom bar — below the table card -->
		<div v-if="showFooter && hasFetched" class="mt-2 grid shrink-0 grid-cols-3 items-center px-1">
			<slot name="footer">
				<!-- Left: Show N entries -->
				<div class="flex items-center gap-2">
					<span class="font-sans text-sm font-medium text-primary/70 dark:text-primary-light/70"
						>Show</span
					>
					<div
						class="flex overflow-hidden rounded-lg border border-primary/25 dark:border-primary/30"
					>
						<button
							v-for="(n, i) in [10, 20, 50, 100]"
							:key="n"
							:class="[
								'cursor-pointer px-3 py-1.5 font-sans text-sm font-semibold transition-all',
								i > 0 ? 'border-l border-primary/25 dark:border-primary/25' : '',
								entriesPerPage === n
									? 'bg-primary dark:bg-primary'
									: 'bg-white text-primary hover:bg-primary/5 dark:bg-primary/10 dark:text-primary dark:hover:bg-primary/20',
							]"
							:style="
								entriesPerPage === n ? { color: isDark ? darkPrimaryOnColor : '#ffffff' } : {}
							"
							@click="$emit('update:entriesPerPage', n)"
						>
							{{ n }}
						</button>
					</div>
				</div>

				<!-- Center: reserved (kept for grid symmetry with the left column) -->
				<div />

				<!-- Right: count + load more -->
				<div class="flex items-center justify-end gap-4">
					<span
						v-if="totalCount && data.length > 0"
						class="font-sans text-sm font-medium text-slate-500 dark:text-slate-400"
					>
						Showing
						<strong class="font-bold text-primary dark:text-primary-light">{{
							data.length
						}}</strong>
						of
						<strong class="font-bold text-primary dark:text-primary-light">{{
							totalCount
						}}</strong>
						{{ itemName }}
					</span>
					<PrimaryButton
						v-if="showLoadMore && data.length > 0"
						label="Load More"
						icon="arrow-down"
						size="sm"
						@click="$emit('load-more')"
					/>
				</div>
			</slot>
		</div>
	</div>
	<!-- end outer wrapper -->
</template>

<script>
import { useResponsive } from "../../../composables/useResponsive"
import { useTheme } from "../../../composables/useTheme"
import LoadingOverlay from "../LoadingOverlay.vue"
import Checkbox from "../../fields/Checkbox.vue"
import StatusBadge from "../StatusBadge.vue"
import TagBadge from "../TagBadge.vue"
import TableSkeletonLoader from "../../skeleton/TableSkeletonLoader.vue"
import DateDisplay from "../../display_fields/DateDisplay.vue"
import DateTimeDisplay from "../../display_fields/DateTimeDisplay.vue"
import TimeDisplay from "../../display_fields/TimeDisplay.vue"
import CurrencyDisplay from "../../display_fields/CurrencyDisplay.vue"
import PercentageDisplay from "../../display_fields/PercentageDisplay.vue"
import FloatDisplay from "../../display_fields/FloatDisplay.vue"
import LinkDisplay from "../../display_fields/LinkDisplay.vue"
import PrimaryButton from "../../buttons/PrimaryButton.vue"
import { formatNumber, formatRelativeTime, formatDateTime } from "../../../utils/forms/formatters"
import { getInitials, getAvatarColorIndex } from "../../../utils/avatarColor"

export default {
	name: "DataTable",
	components: {
		LoadingOverlay,
		Checkbox,
		StatusBadge,
		TagBadge,
		TableSkeletonLoader,
		DateDisplay,
		DateTimeDisplay,
		TimeDisplay,
		CurrencyDisplay,
		PercentageDisplay,
		FloatDisplay,
		LinkDisplay,
		PrimaryButton,
	},
	props: {
		loading: {
			type: Boolean,
			default: false,
		},
		columns: {
			type: Array,
			required: true,
		},
		data: {
			type: Array,
			required: true,
		},
		rowKey: {
			type: String,
			default: "id",
		},
		hasActions: {
			type: Boolean,
			default: true,
		},
		sortOrders: {
			type: Array,
			default: () => [],
		},
		entriesPerPage: {
			type: Number,
			default: 20,
		},
		showFooter: {
			type: Boolean,
			default: true,
		},
		showLoadMore: {
			type: Boolean,
			default: true,
		},
		loadMoreText: {
			type: String,
			default: "Load More",
		},
		totalCount: {
			type: Number,
			default: null,
		},
		itemName: {
			type: String,
			default: "items",
		},
		emptyText: {
			type: String,
			default: "No data available",
		},
		searchQuery: {
			type: String,
			default: "",
		},
		searchPlaceholder: {
			type: String,
			default: "Search...",
		},
		visibleColumns: {
			type: Array,
			default: null,
		},
		selectable: {
			type: Boolean,
			default: false,
		},
		showTimeColumn: {
			type: Boolean,
			default: true,
		},
	},
	emits: [
		"sort",
		"row-click",
		"action-click",
		"load-more",
		"selection-change",
		"update:entriesPerPage",
		"update:searchQuery",
		"search",
	],
	setup() {
		const { isMobile, isTablet, isDesktop } = useResponsive()
		const { isDark, darkPrimaryOnColor } = useTheme()
		return { isMobile, isTablet, isDesktop, isDark, darkPrimaryOnColor }
	},
	data() {
		return {
			selectedRowKeys: [],
			columnWidths: {},
			resizingColumn: null,
			startX: 0,
			startWidth: 0,
			hasFetched: false,
			skeletonColumnCount: 5,
			skeletonHeaderWidths: ["56px", "80px", "64px", "96px", "72px", "48px", "88px"],
			timeColumnMode: "modified",
			timeColumnWidth: 110,
			nowTick: Date.now(),
			timeTickInterval: null,
		}
	},
	computed: {
		// No page currently passes an #actions slot — rendering the column anyway
		// left a permanently empty 60px gap before the last column.
		showActionsColumn() {
			return this.hasActions && !!this.$slots.actions
		},
		filteredColumns() {
			if (!this.visibleColumns || this.visibleColumns.length === 0) {
				return this.columns
			}
			// Maintain order from this.columns array (which respects drag-and-drop)
			return this.columns.filter((col) => this.visibleColumns.includes(col.key))
		},
		isAllSelected() {
			if (this.data.length === 0) return false
			return this.data.every((row) => this.selectedRowKeys.includes(row.name || row.id))
		},
		isSomeSelected() {
			const selectedCount = this.selectedRowKeys.length
			return selectedCount > 0 && !this.isAllSelected
		},
		// Frappe's standard fieldname for creation time is "creation", not "created"
		timeColumnField() {
			return this.timeColumnMode === "created" ? "creation" : "modified"
		},
		timeColumnLabel() {
			return this.timeColumnMode === "created" ? "Created" : "Modified"
		},
		totalTableWidth() {
			let w = this.selectable ? 48 : 0
			this.filteredColumns.forEach((col) => {
				w += this.columnWidths[col.key] || 120
			})
			if (this.showActionsColumn) w += 60
			if (this.showTimeColumn) w += this.timeColumnWidth
			return Math.max(600, w)
		},
	},
	watch: {
		filteredColumns: {
			handler() {
				this.initializeColumnWidths()
			},
			immediate: true,
		},
		data: {
			handler(newData, oldData) {
				// Recalculate widths when data changes (only if data was empty before)
				if (oldData && oldData.length === 0 && newData.length > 0) {
					this.columnWidths = {}
					this.initializeColumnWidths()
				}
			},
		},
		loading(newVal, oldVal) {
			if (oldVal === true && newVal === false) {
				this.hasFetched = true
			}
		},
	},
	mounted() {
		this.initializeColumnWidths()
		// Keep relative timestamps ("now" -> "1 min" -> "2 mins"...) fresh without a full refetch
		this.timeTickInterval = setInterval(() => {
			this.nowTick = Date.now()
		}, 60000)
	},
	beforeUnmount() {
		if (this.timeTickInterval) clearInterval(this.timeTickInterval)
	},
	methods: {
		formatNumber,
		formatRelativeTime,
		formatDateTime,
		toggleTimeColumnMode() {
			this.timeColumnMode = this.timeColumnMode === "modified" ? "created" : "modified"
		},
		isRowSelected(row) {
			return this.selectedRowKeys.includes(row[this.rowKey])
		},
		toggleSelectAll() {
			if (this.isAllSelected) {
				this.selectedRowKeys = []
			} else {
				this.selectedRowKeys = this.data.map((r) => r[this.rowKey])
			}
			this.$emit("selection-change", [...this.selectedRowKeys])
		},
		toggleSelectRow(row) {
			const key = row[this.rowKey]
			const index = this.selectedRowKeys.indexOf(key)
			if (index === -1) {
				this.selectedRowKeys.push(key)
			} else {
				this.selectedRowKeys.splice(index, 1)
			}
			this.$emit("selection-change", [...this.selectedRowKeys])
		},
		handleRowClick(row, event) {
			// Don't trigger if clicking on interactive elements
			const interactiveTags = ["INPUT", "A", "BUTTON", "LABEL"]
			if (
				interactiveTags.includes(event.target.tagName) ||
				event.target.closest("a, button, input, label")
			) {
				return
			}
			this.$emit("row-click", row)
		},
		onBodyScroll(event) {
			if (this.$refs.headerScroll) {
				this.$refs.headerScroll.scrollLeft = event.target.scrollLeft
			}
		},
		handleSort(key) {
			const existing = this.sortOrders.find((s) => s.key === key)
			const newOrders = existing
				? this.sortOrders.map((s) =>
						s.key === key ? { ...s, order: s.order === "asc" ? "desc" : "asc" } : s,
					)
				: [...this.sortOrders, { key, order: "asc" }]
			this.$emit("sort", newOrders)
		},
		initializeColumnWidths() {
			this.filteredColumns.forEach((col) => {
				if (!this.columnWidths[col.key]) {
					// Calculate width based on content
					const calculatedWidth = this.calculateColumnWidth(col)
					this.columnWidths[col.key] = col.width || calculatedWidth
				}
			})
		},
		calculateColumnWidth(column) {
			// Create a temporary element to measure text width
			const canvas = document.createElement("canvas")
			const context = canvas.getContext("2d")
			context.font = "11px Inter, system-ui, -apple-system, sans-serif" // Match header font

			// Measure header text
			const headerWidth = context.measureText(column.label || "").width

			// Measure content in data rows
			let maxContentWidth = headerWidth

			this.data.slice(0, 100).forEach((row) => {
				const value = row[column.key]
				let displayValue

				if (value === null || value === undefined) {
					displayValue = "-"
				} else if (Array.isArray(value)) {
					displayValue = this.formatArrayValue(value)
				} else if (typeof value === "object") {
					displayValue = JSON.stringify(value)
				} else {
					displayValue = String(value)
				}

				const width = context.measureText(displayValue).width
				if (width > maxContentWidth) {
					maxContentWidth = width
				}
			})

			// Add padding (left + right padding = 32px) + some buffer (20px) + sort icon space (20px if sortable)
			const padding = 32
			const buffer = 20
			const iconSpace = column.sortable ? 20 : 0
			const totalWidth = Math.ceil(maxContentWidth) + padding + buffer + iconSpace

			// Constrain between min (120px) and max (400px)
			return Math.max(120, Math.min(400, totalWidth))
		},
		startResize(event, columnKey) {
			console.log("Start resize:", columnKey, event)
			event.preventDefault()
			event.stopPropagation()

			this.resizingColumn = columnKey
			this.startX = event.clientX
			this.startWidth = this.columnWidths[columnKey] || 150

			const onMouseMove = (e) => {
				if (!this.resizingColumn) return
				const diff = e.clientX - this.startX
				const newWidth = Math.max(80, this.startWidth + diff)
				this.columnWidths[this.resizingColumn] = newWidth
			}

			const onMouseUp = () => {
				console.log("Stop resize")
				this.resizingColumn = null
				document.removeEventListener("mousemove", onMouseMove)
				document.removeEventListener("mouseup", onMouseUp)
				document.body.style.cursor = ""
				document.body.style.userSelect = ""
			}

			document.addEventListener("mousemove", onMouseMove)
			document.addEventListener("mouseup", onMouseUp)
			document.body.style.cursor = "col-resize"
			document.body.style.userSelect = "none"
		},
		onSearchInput(e) {
			const val = e.target.value
			this.$emit("update:searchQuery", val)
			clearTimeout(this._searchTimer)
			this._searchTimer = setTimeout(() => {
				this.$emit("search", val)
			}, 300)
		},
		clearSearch() {
			this.$emit("update:searchQuery", "")
			this.$emit("search", "")
		},
		formatArrayValue(arr) {
			if (!arr || !arr.length) return "-"

			// Handle array of objects (child table data)
			if (typeof arr[0] === "object" && arr[0] !== null) {
				return arr
					.map((item) => {
						// Skip the 'name' field (row identifier) and get the actual value
						const keys = Object.keys(item).filter((k) => k !== "name" && k !== "parent")
						if (keys.length > 0) {
							// Get the first non-system field value
							const value = item[keys[0]]
							return value !== null && value !== undefined ? String(value) : ""
						}
						// Fallback to common label fields
						const labelFields = [
							"label",
							"title",
							"company_name",
							"branch_name",
							"company",
							"branch",
						]
						for (const field of labelFields) {
							if (item[field]) return String(item[field])
						}
						// Last resort: use 'name' field
						return item.name || ""
					})
					.filter(Boolean)
					.join(", ")
			}

			// Handle array of primitives
			return arr.join(", ")
		},
		getInitials,
		getAvatarColorIndex,
		getStatusText(value) {
			if (typeof value === "boolean" || typeof value === "number") {
				return value ? "Active" : "Inactive"
			}
			return value || "Unknown"
		},
	},
}
</script>

<style scoped>
/* Thin, brand-colored scrollbar (the `scrollbar-thin`/`scrollbar-thumb-*`
   Tailwind classes previously used here don't exist without the
   tailwind-scrollbar plugin, which isn't installed — they were no-ops). */
.table-scroll {
	scrollbar-width: thin;
	scrollbar-color: rgb(var(--color-primary-rgb, 103, 66, 207), 0.45) transparent;
}

.table-scroll::-webkit-scrollbar {
	width: 6px;
	height: 6px;
}

.table-scroll::-webkit-scrollbar-track {
	background: transparent;
}

.table-scroll::-webkit-scrollbar-thumb {
	background-color: rgb(var(--color-primary-rgb, 103, 66, 207), 0.45);
	border-radius: 9999px;
}

.table-scroll::-webkit-scrollbar-thumb:hover {
	background-color: rgb(var(--color-primary-rgb, 103, 66, 207), 0.65);
}

.skeleton-header-cell {
	animation: skeleton-shimmer 1.6s ease-in-out infinite;
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
