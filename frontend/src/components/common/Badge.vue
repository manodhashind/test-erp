<template>
	<div
		class="kinetic-badge"
		:class="[`badge-${variant}`, `badge-${size}`, { 'badge-pill': pill }]"
	>
		<span v-if="showDot" class="status-dot" />
		<span class="badge-label">
			<slot>{{ label }}</slot>
		</span>
	</div>
</template>

<script setup>
defineProps({
	label: {
		type: String,
		default: "",
	},
	variant: {
		type: String,
		default: "primary",
		validator: (value) =>
			["primary", "secondary", "success", "danger", "warning", "info", "ghost"].includes(value),
	},
	size: {
		type: String,
		default: "md",
		validator: (value) => ["sm", "md", "lg"].includes(value),
	},
	pill: {
		type: Boolean,
		default: true,
	},
	showDot: {
		type: Boolean,
		default: false,
	},
})
</script>

<style scoped>
.kinetic-badge {
	display: inline-flex;
	align-items: center;
	gap: 6px;
	font-family: Inter, sans-serif;
	font-weight: 700;
	white-space: nowrap;
	transition: all 0.2s ease;
}

.badge-label {
	line-height: 1;
}

/* Sizes */
.badge-sm {
	padding: 2px 8px;
	font-size: 10px;
	letter-spacing: 0.03em;
}

.badge-md {
	padding: 4px 12px;
	font-size: 11px;
	letter-spacing: 0.05em;
}

.badge-lg {
	padding: 6px 16px;
	font-size: 12px;
	letter-spacing: 0.06em;
}

.badge-pill {
	border-radius: 9999px;
}

/* Dot Indicator */
.status-dot {
	width: 6px;
	height: 6px;
	border-radius: 50%;
	flex-shrink: 0;
}

/* Variants */
.badge-success {
	background: #ecfdf5;
	color: #059669;
	border: 1px solid #10b98133;
}
.badge-success .status-dot {
	background: #10b981;
	box-shadow: 0 0 8px #10b98166;
}

.badge-danger {
	background: #fef2f2;
	color: #dc2626;
	border: 1px solid #ef444433;
}
.badge-danger .status-dot {
	background: #ef4444;
	box-shadow: 0 0 8px #ef444466;
}

.badge-warning {
	background: #fffbeb;
	color: #d97706;
	border: 1px solid #f59e0b33;
}
.badge-warning .status-dot {
	background: #f59e0b;
	box-shadow: 0 0 8px #f59e0b66;
}

.badge-primary {
	background: #eff6ff;
	color: #2563eb;
	border: 1px solid #3b82f633;
}
.badge-primary .status-dot {
	background: #3b82f6;
	box-shadow: 0 0 8px #3b82f666;
}

.badge-secondary {
	background: #f8fafc;
	color: #475569;
	border: 1px solid #94a3b833;
}
.badge-secondary .status-dot {
	background: #94a3b8;
}

.badge-info {
	background: #f0f9ff;
	color: #0891b2;
	border: 1px solid #06b6d433;
}
.badge-info .status-dot {
	background: #06b6d4;
	box-shadow: 0 0 8px #06b6d466;
}

.badge-ghost {
	background: rgb(255 255 255 / 10%);
	backdrop-filter: blur(4px);
	color: white;
	border: 1px solid rgb(255 255 255 / 20%);
}

/* Text Transform */
.badge-label {
	text-transform: uppercase;
}
</style>
