<template>
	<div
		:class="[
			'pointer-events-auto relative flex w-[360px] items-start gap-3 overflow-hidden rounded-xl border p-4 shadow-xl ring-1 ring-black/5 transition-all duration-300 dark:shadow-black/40 dark:ring-white/10',
			containerClass,
			route ? 'cursor-pointer hover:translate-y-[-1px] hover:shadow-2xl' : '',
		]"
		@click="handleClick"
	>
		<!-- Accent bar -->
		<!-- <div :class="['absolute left-0 top-0 h-full w-1.5', accentClass]" /> -->

		<!-- Progress Bar Animation - counts down the toast's remaining lifetime -->
		<div
			v-if="duration > 0"
			:class="[
				'toast-progress absolute bottom-0 left-0 h-1 w-full origin-left opacity-80',
				accentClass,
			]"
			:style="{ '--toast-duration': `${duration}ms` }"
		/>

		<!-- Icon - Normalized size -->
		<div :class="['flex-shrink-0 rounded-full p-2', iconChipClass]">
			<Icon :icon="iconName" :class="iconColorClass" size="md" />
		</div>

		<!-- Content -->
		<div class="min-w-0 flex-1 pr-4">
			<p :class="['mb-0.5 text-[13px] font-bold capitalize leading-tight', titleColorClass]">
				{{ type === "error" ? "Critical" : type }}
			</p>
			<p class="text-[12px] font-semibold leading-relaxed text-slate-700 dark:text-slate-300">
				<template v-for="(segment, i) in messageSegments" :key="i"
					><strong v-if="segment.bold" class="font-extrabold">{{ segment.text }}</strong
					><template v-else>{{ segment.text }}</template></template
				>
			</p>
		</div>

		<!-- Close Button - Top Right Absolute -->
		<button
			v-if="closable"
			class="group absolute top-2.5 right-2.5 flex-shrink-0 rounded-full p-1 transition-colors hover:bg-slate-100 dark:hover:bg-slate-800"
			@click.stop="$emit('close')"
		>
			<Icon
				icon="close"
				size="sm"
				class="text-slate-400 group-hover:text-slate-600 dark:text-slate-500 dark:group-hover:text-slate-300"
			/>
		</button>
	</div>
</template>

<script setup>
import { computed } from "vue"
import { useRouter } from "vue-router"
import Icon from "./AppIcon.vue"

const props = defineProps({
	id: Number,
	message: String,
	type: {
		type: String,
		default: "info", // info, success, warning, error
	},
	route: String,
	closable: {
		type: Boolean,
		default: true,
	},
	duration: {
		type: Number,
		default: 5000,
	},
})

const emit = defineEmits(["close"])
const router = useRouter()

// Lightweight **bold** markdown support — parsed into plain text segments and
// rendered via text interpolation (never v-html), so arbitrary HTML in a
// message (e.g. a user-entered role name) can never be interpreted as markup.
const messageSegments = computed(() => {
	const msg = props.message || ""
	return msg
		.split(/\*\*(.+?)\*\*/g)
		.map((text, i) => ({ text, bold: i % 2 === 1 }))
		.filter((segment) => segment.text !== "")
})

const containerClass = computed(() => {
	switch (props.type) {
		case "success":
			return "bg-emerald-50 border-emerald-300 shadow-emerald-900/10 dark:bg-emerald-900/90 dark:border-emerald-800"
		case "warning":
			return "bg-amber-50 border-amber-300 shadow-amber-900/10 dark:bg-amber-900/90 dark:border-amber-800"
		case "error":
			return "bg-red-50 border-red-300 shadow-red-900/10 dark:bg-red-900/90 dark:border-red-800"
		default:
			return "bg-blue-50 border-blue-300 shadow-blue-900/10 dark:bg-blue-900/90 dark:border-blue-800"
	}
})

const accentClass = computed(() => {
	switch (props.type) {
		case "success":
			return "bg-emerald-500"
		case "warning":
			return "bg-amber-500"
		case "error":
			return "bg-red-500"
		default:
			return "bg-blue-500"
	}
})

const iconChipClass = computed(() => {
	switch (props.type) {
		case "success":
			return "bg-emerald-100 dark:bg-white/10"
		case "warning":
			return "bg-amber-100 dark:bg-white/10"
		case "error":
			return "bg-red-100 dark:bg-white/10"
		default:
			return "bg-blue-100 dark:bg-white/10"
	}
})

const iconColorClass = computed(() => {
	switch (props.type) {
		case "success":
			return "text-emerald-600 dark:text-emerald-400"
		case "warning":
			return "text-amber-600 dark:text-amber-400"
		case "error":
			return "text-red-600 dark:text-red-400"
		default:
			return "text-blue-600 dark:text-blue-400"
	}
})

const titleColorClass = computed(() => {
	switch (props.type) {
		case "success":
			return "text-emerald-700 dark:text-emerald-400"
		case "warning":
			return "text-amber-700 dark:text-amber-400"
		case "error":
			return "text-red-700 dark:text-red-400"
		default:
			return "text-blue-700 dark:text-blue-400"
	}
})

const iconName = computed(() => {
	switch (props.type) {
		case "success":
			return "check_circle"
		case "warning":
			return "report_problem"
		case "error":
			return "dangerous"
		default:
			return "info"
	}
})

const handleClick = () => {
	if (props.route) {
		router.push(props.route)
		emit("close")
	}
}
</script>

<style scoped>
.toast-progress {
	animation: shrink var(--toast-duration, 5000ms) linear forwards;
}

@keyframes shrink {
	from {
		transform: scaleX(1);
	}
	to {
		transform: scaleX(0);
	}
}
</style>
