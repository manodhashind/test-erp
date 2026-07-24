<template>
	<div class="card-data-table-container">
		<div v-if="data.length > 0" class="card-list">
			<div
				v-for="(item, index) in data"
				:key="item.name || index"
				class="card-row"
				:class="['border-' + getStatusClass(item.status)]"
				@click="$emit('row-click', item)"
			>
				<!-- Left Section: Icon and Basic Info -->
				<div class="card-info-section">
					<div class="card-icon-wrapper" :class="getStatusClass(item.status)">
						<img src="@/assets/icons/order-management.svg" alt="Box" class="card-icon" />
					</div>
					<div class="card-primary-details">
						<div class="card-id">
							{{ item.name }}
						</div>
						<div class="card-customer">
							{{ item.customer_name || item.full_name || "N/A" }}
						</div>
						<div class="card-status-meta">
							<span class="status-badge" :class="getStatusClass(item.status)">
								{{ item.status || "N/A" }}
							</span>
							<span class="updated-time">Updated {{ formatRelativeTime(item.modified) }}</span>
						</div>
					</div>
				</div>

				<!-- Middle Section: Progress Stepper -->
				<div class="card-progress-section">
					<div class="stepper-container">
						<div class="stepper-line">
							<div class="line-fill" :style="{ width: getProgressWidth(item) }" />
						</div>
						<div class="stepper-steps">
							<div
								v-for="step in progressSteps"
								:key="step.key"
								class="step-item"
								:class="{
									active: isStepActive(item, step.key),
									completed: isStepCompleted(item, step.key),
								}"
							>
								<div class="step-circle">
									<div v-if="isStepCompleted(item, step.key)" class="check-icon">✓</div>
								</div>
								<div class="step-label">
									{{ step.label }}
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Right Section: Destination and Action -->
				<div class="card-action-section">
					<div class="destination-info">
						<span class="dest-label">DESTINATION</span>
						<span class="dest-value">{{ item.destination || "Not Set" }}</span>
					</div>
					<div class="action-chevron">
						<img src="@/assets/icons/chevron-right.svg" alt="Go" />
					</div>
				</div>
			</div>
		</div>

		<!-- Empty State -->
		<div v-else-if="!loading" class="empty-state">
			<img src="@/assets/icons/empty-state-icon.svg" alt="No data" />
			<p>No records found matching your criteria</p>
		</div>

		<!-- Loading Overlay (reuses common LoadingOverlay) -->
		<LoadingOverlay v-if="loading" :active="true" />
	</div>
</template>

<script setup>
import { computed } from "vue"
import LoadingOverlay from "../LoadingOverlay.vue"
import { formatRelativeTime } from "@/utils/helpers"

const props = defineProps({
	data: {
		type: Array,
		required: true,
		default: () => [],
	},
	loading: {
		type: Boolean,
		default: false,
	},
	progressSteps: {
		type: Array,
		default: () => [
			{ key: "Request", label: "Request" },
			{ key: "Order", label: "Order" },
			{ key: "Dispatch", label: "Dispatch" },
			{ key: "Trip", label: "Trip" },
			{ key: "Invoice", label: "Invoice" },
			{ key: "Payment", label: "Payment" },
		],
	},
})

defineEmits(["row-click"])

const getStatusClass = (status) => {
	if (!status) return "default"
	const s = status.toLowerCase()
	if (s.includes("paid") || s.includes("payment")) return "payment"
	if (s.includes("invoice")) return "invoice"
	if (s.includes("trip")) return "trip"
	if (s.includes("dispatch")) return "dispatch"
	if (s.includes("order")) return "order"
	if (s.includes("request")) return "request"
	return "default"
}

// Logic for progress
const getStatusLevel = (status) => {
	if (!status) return 1
	const s = status.toLowerCase()
	// Payment
	if (s === "fully paid" || s === "partially paid") return 6
	if (s === "payment in progress") return 5.5

	// Invoice
	if (s === "invoiced") return 5
	if (s === "invoice in progress") return 4.5

	// Trip
	if (s === "trip completed") return 4
	if (s === "trip in progress") return 3.5

	// Dispatch
	if (s === "dispatched") return 3
	if (s === "dispatch in progress") return 2.5

	// Order
	if (s === "order completed") return 2
	if (s === "order in progress") return 1.5

	// Request
	if (s === "requested") return 1

	// Fallbacks
	if (s.includes("payment") || s.includes("paid")) return 6
	if (s.includes("invoice")) return 5
	if (s.includes("trip")) return 4
	if (s.includes("dispatch")) return 3
	if (s.includes("order")) return 2
	if (s.includes("request")) return 1
	return 1
}

const isStepCompleted = (item, stepKey) => {
	const statusLevels = {
		Request: 1,
		Order: 2,
		Dispatch: 3,
		Trip: 4,
		Invoice: 5,
		Payment: 6,
	}
	const currentLevel = item.current_step || getStatusLevel(item.status)
	return statusLevels[stepKey] < currentLevel
}

const isStepActive = (item, stepKey) => {
	const statusLevels = {
		Request: 1,
		Order: 2,
		Dispatch: 3,
		Trip: 4,
		Invoice: 5,
		Payment: 6,
	}
	const currentLevel = item.current_step || getStatusLevel(item.status)
	return statusLevels[stepKey] === currentLevel
}

const getProgressWidth = (item) => {
	const currentLevel = item.current_step || getStatusLevel(item.status)
	return `${(currentLevel - 1) * 20}%`
}
</script>

<style scoped>
.card-data-table-container {
	position: relative;
	min-height: 200px;
}

.card-list {
	display: flex;
	flex-direction: column;
	gap: 16px;
}

.card-row {
	background: white;
	border-radius: 16px;
	padding: 24px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	transition: all 0.2s ease;
	cursor: pointer;
	border-left-width: 4px;
	border-left-style: solid;
	box-shadow:
		0 0 0 1px rgb(0 40 142 / 6%),
		0 4px 8px rgb(0 40 142 / 6%),
		0 2px 4px rgb(0 40 142 / 4%),
		0 1px 2px rgb(0 40 142 / 3%);
}

.card-row.border-request {
	border-left-color: #3b82f6;
}
.card-row.border-order {
	border-left-color: #a855f7;
}
.card-row.border-dispatch {
	border-left-color: #f97316;
}
.card-row.border-trip {
	border-left-color: #14b8a6;
}
.card-row.border-invoice {
	border-left-color: #f59e0b;
}
.card-row.border-payment {
	border-left-color: #22c55e;
}
.card-row.border-default {
	border-left-color: #cbd5e1;
}

.card-row:hover {
	transform: translateY(-2px);
	box-shadow:
		0 0 0 1px rgb(0 40 142 / 8%),
		0 12px 20px rgb(0 40 142 / 12%),
		0 8px 12px rgb(0 40 142 / 8%),
		0 4px 6px rgb(0 40 142 / 6%);
}

/* Info Section */
.card-info-section {
	display: flex;
	align-items: center;
	gap: 16px;
	flex: 0 0 250px;
}

.card-icon-wrapper {
	width: 56px;
	height: 56px;
	border-radius: 12px;
	display: flex;
	align-items: center;
	justify-content: center;
}

.card-icon-wrapper.request {
	background-color: #eff6ff;
}
.card-icon-wrapper.order {
	background-color: #f3e8ff;
}
.card-icon-wrapper.dispatch {
	background-color: #fff7ed;
}
.card-icon-wrapper.trip {
	background-color: #ecfeff;
}
.card-icon-wrapper.invoice {
	background-color: #fffbeb;
}
.card-icon-wrapper.payment {
	background-color: #f0fdf4;
}
.card-icon-wrapper.default {
	background-color: #f8fafc;
}

.card-icon {
	width: 28px;
	height: 28px;
}

.card-id {
	font-size: 1.1rem;
	font-weight: 700;
	color: #1e293b;
}

.card-customer {
	color: #64748b;
	font-size: 0.95rem;
	margin-bottom: 8px;
}

.card-status-meta {
	display: flex;
	align-items: center;
	gap: 12px;
}

.status-badge {
	padding: 4px 12px;
	border-radius: 9999px;
	font-size: 0.75rem;
	font-weight: 700;
	text-transform: uppercase;
}

.status-badge.request {
	background: #dbeafe;
	color: #1e40af;
}
.status-badge.order {
	background: #f3e8ff;
	color: #7e22ce;
}
.status-badge.dispatch {
	background: #ffedd5;
	color: #c2410c;
}
.status-badge.trip {
	background: #cffafe;
	color: #0e7490;
}
.status-badge.invoice {
	background: #fef3c7;
	color: #92400e;
}
.status-badge.payment {
	background: #dcfce7;
	color: #166534;
}
.status-badge.default {
	background: #f1f5f9;
	color: #475569;
}

.updated-time {
	font-size: 0.75rem;
	color: #94a3b8;
}

/* Progress Section */
.card-progress-section {
	flex: 1;
	max-width: 600px;
	padding: 0 40px;
}

.stepper-container {
	position: relative;
	padding-top: 10px;
}

.stepper-line {
	position: absolute;
	top: 24px;
	left: 0;
	right: 0;
	height: 4px;
	background: #f1f5f9;
	z-index: 1;
}

.line-fill {
	height: 100%;
	background: var(--color-primary);
	transition: width 0.5s ease;
}

.stepper-steps {
	position: relative;
	display: flex;
	justify-content: space-between;
	z-index: 2;
}

.step-item {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 12px;
}

.step-circle {
	width: 28px;
	height: 28px;
	border-radius: 50%;
	background: white;
	border: 4px solid #f1f5f9;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: all 0.3s ease;
}

.check-icon {
	color: white;
	font-size: 14px;
	font-weight: bold;
}

.step-item.completed .step-circle {
	background: var(--color-primary);
	border-color: var(--color-primary);
}

.step-item.active .step-circle {
	background: var(--color-primary);
	border-color: rgb(var(--color-primary-rgb, 103, 66, 207), 0.2);
	box-shadow: 0 0 0 4px rgb(var(--color-primary-rgb, 103, 66, 207), 0.1);
}

.step-label {
	font-size: 0.7rem;
	font-weight: 700;
	color: #94a3b8;
	white-space: nowrap;
}

.step-item.active .step-label,
.step-item.completed .step-label {
	color: #1e293b;
}

/* Action Section */
.card-action-section {
	display: flex;
	align-items: center;
	gap: 40px;
	flex: 0 0 200px;
	justify-content: flex-end;
}

.destination-info {
	display: flex;
	flex-direction: column;
	align-items: flex-end;
}

.dest-label {
	font-size: 0.65rem;
	font-weight: 700;
	color: #94a3b8;
	letter-spacing: 0.05em;
}

.dest-value {
	font-size: 1rem;
	font-weight: 700;
	color: #1e293b;
}

.action-chevron img {
	width: 20px;
	height: 20px;
	opacity: 0.3;
}

.card-row:hover .action-chevron img {
	opacity: 1;
	transform: translateX(4px);
}

.empty-state {
	text-align: center;
	padding: 60px;
	color: #64748b;
}

.empty-state img {
	width: 80px;
	margin-bottom: 16px;
	opacity: 0.5;
}
</style>
