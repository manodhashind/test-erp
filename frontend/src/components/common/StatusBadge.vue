<template>
	<span class="status-badge" :class="[`scheme-${scheme}`, `size-${size}`]">
		<span class="status-dot" />
		<span class="status-label">{{ status }}</span>
	</span>
</template>

<script setup>
import { computed } from "vue"
import { getStatusScheme } from "../../utils/statusScheme.js"

const props = defineProps({
	status: {
		type: String,
		default: "",
	},
	size: {
		type: String,
		default: "md",
		validator: (v) => ["sm", "md", "lg"].includes(v),
	},
})

const scheme = computed(() => getStatusScheme(props.status))
</script>

<style scoped>
/* ── Base layout ──────────────────────────────────────────────────────────────── */

.status-badge {
	display: inline-flex;
	align-items: center;
	gap: 6px;
	border-radius: 9999px;
	font-family: Inter, sans-serif;
	font-weight: 600;
	white-space: nowrap;
	border-width: 1px;
	border-style: solid;
}

.status-label {
	line-height: 1;
}

.status-dot {
	border-radius: 50%;
	flex-shrink: 0;
}

/* ── Sizes ────────────────────────────────────────────────────────────────────── */

.size-sm {
	padding: 2px 8px;
	font-size: 11px;
	letter-spacing: 0.02em;
}
.size-sm .status-dot {
	width: 5px;
	height: 5px;
}

.size-md {
	padding: 3px 10px;
	font-size: 12px;
	letter-spacing: 0.03em;
}
.size-md .status-dot {
	width: 6px;
	height: 6px;
}

.size-lg {
	padding: 5px 14px;
	font-size: 13px;
	letter-spacing: 0.03em;
}
.size-lg .status-dot {
	width: 7px;
	height: 7px;
}

/* ── Color schemes ────────────────────────────────────────────────────────────── */

.scheme-green {
	background: #ecfdf5;
	color: #059669;
	border-color: #10b98126;
}
.scheme-green .status-dot {
	background: #10b981;
	box-shadow: 0 0 6px #10b98166;
}
:global(.dark) .scheme-green {
	background: #064e3b26;
	color: #34d399;
	border-color: #10b98126;
}
:global(.dark) .scheme-green .status-dot {
	background: #34d399;
	box-shadow: 0 0 6px #34d39966;
}

.scheme-red {
	background: #fef2f2;
	color: #dc2626;
	border-color: #ef444426;
}
.scheme-red .status-dot {
	background: #ef4444;
	box-shadow: 0 0 6px #ef444466;
}
:global(.dark) .scheme-red {
	background: #7f1d1d26;
	color: #f87171;
	border-color: #ef444426;
}
:global(.dark) .scheme-red .status-dot {
	background: #f87171;
	box-shadow: 0 0 6px #f8717166;
}

.scheme-amber {
	background: #fffbeb;
	color: #d97706;
	border-color: #f59e0b26;
}
.scheme-amber .status-dot {
	background: #f59e0b;
	box-shadow: 0 0 6px #f59e0b66;
}
:global(.dark) .scheme-amber {
	background: #78350f26;
	color: #fbbf24;
	border-color: #f59e0b26;
}
:global(.dark) .scheme-amber .status-dot {
	background: #fbbf24;
	box-shadow: 0 0 6px #fbbf2466;
}

.scheme-blue {
	background: #eff6ff;
	color: #2563eb;
	border-color: #3b82f626;
}
.scheme-blue .status-dot {
	background: #3b82f6;
	box-shadow: 0 0 6px #3b82f666;
}
:global(.dark) .scheme-blue {
	background: #1e3a8a26;
	color: #60a5fa;
	border-color: #3b82f626;
}
:global(.dark) .scheme-blue .status-dot {
	background: #60a5fa;
	box-shadow: 0 0 6px #60a5fa66;
}

.scheme-purple {
	background: #f5f3ff;
	color: #7c3aed;
	border-color: #8b5cf626;
}
.scheme-purple .status-dot {
	background: #8b5cf6;
	box-shadow: 0 0 6px #8b5cf666;
}
:global(.dark) .scheme-purple {
	background: #4c1d9526;
	color: #a78bfa;
	border-color: #8b5cf626;
}
:global(.dark) .scheme-purple .status-dot {
	background: #a78bfa;
	box-shadow: 0 0 6px #a78bfa66;
}

.scheme-gray {
	background: #f8fafc;
	color: #64748b;
	border-color: #94a3b826;
}
.scheme-gray .status-dot {
	background: #94a3b8;
}
:global(.dark) .scheme-gray {
	background: #1e293b26;
	color: #94a3b8;
	border-color: #47556926;
}
:global(.dark) .scheme-gray .status-dot {
	background: #64748b;
}
</style>
