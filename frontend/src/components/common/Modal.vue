<template>
	<Teleport to="body">
		<transition name="modal-fade">
			<div
				v-if="isOpen || hashOpen"
				class="dark:bg-slate-950/60 fixed inset-0 z-[9999] flex items-center justify-center bg-slate-900/40 p-5 backdrop-blur-sm"
				role="dialog"
				:aria-labelledby="titleId"
				aria-modal="true"
			>
				<div
					class="relative flex max-h-[90vh] w-full scale-100 transform flex-col overflow-hidden rounded-2xl border border-slate-100 bg-white opacity-100 shadow-2xl transition-all duration-300 dark:border-slate-800 dark:bg-app-bg-dark"
					:class="[sizeClass, customClass]"
				>
					<!-- Header -->
					<div
						v-if="showHeader"
						class="flex shrink-0 items-center justify-between border-b border-slate-100 px-5 py-3.5 dark:border-slate-800"
					>
						<slot name="header">
							<h3
								:id="titleId"
								class="m-0 font-sans text-lg font-bold text-slate-900 dark:text-white"
							>
								{{ title }}
							</h3>
							<IconOnlyButton v-if="showCloseButton" icon="close" size="sm" @click="close" />
						</slot>
					</div>

					<!-- Body -->
					<div class="flex-1 overflow-y-auto px-5 py-4 text-slate-700 dark:text-slate-300">
						<slot />
					</div>

					<!-- Footer -->
					<div
						v-if="showFooter"
						class="flex shrink-0 justify-end gap-3 border-t border-slate-100 bg-slate-50/50 px-5 py-3 dark:border-slate-800 dark:bg-slate-900/30"
					>
						<slot name="footer">
							<ActionButton variant="secondary" label="Cancel" @click="close" />
							<PrimaryButton label="Confirm" @click="$emit('confirm')" />
						</slot>
					</div>
				</div>
			</div>
		</transition>
	</Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from "vue"
import { useModalHashRoute } from "@/composables/useModalHashRoute"

const props = defineProps({
	isOpen: {
		type: Boolean,
		required: true,
	},
	title: {
		type: String,
		default: "",
	},
	// URL hash fragment to use when the modal is open; falls back to the title.
	hashId: {
		type: String,
		default: "",
	},
	// Opt out of URL hash routing for this modal.
	noHash: {
		type: Boolean,
		default: false,
	},
	size: {
		type: String,
		default: "md", // sm, md, lg, xl
		validator: (value) => ["sm", "md", "lg", "xl"].includes(value),
	},
	showHeader: {
		type: Boolean,
		default: true,
	},
	showFooter: {
		type: Boolean,
		default: true,
	},
	showCloseButton: {
		type: Boolean,
		default: true,
	},
	closeOnOverlay: {
		type: Boolean,
		default: true,
	},
	customClass: {
		type: String,
		default: "",
	},
})

const emit = defineEmits(["close", "confirm"])

const titleId = `modal-title-${Math.random().toString(36).substr(2, 9)}`

const { hashOpen, close } = useModalHashRoute({
	isOpen: () => props.isOpen,
	close: () => emit("close"),
	hashId: () => props.hashId || props.title,
	enabled: () => !props.noHash,
})

const sizeClass = computed(() => {
	return {
		"max-w-[400px]": props.size === "sm",
		"max-w-[560px]": props.size === "md",
		"max-w-[800px]": props.size === "lg",
		"max-w-[1140px]": props.size === "xl",
	}
})

// Handle ESC key
const handleEsc = (e) => {
	if (e.key === "Escape" && (props.isOpen || hashOpen.value)) {
		close()
	}
}

onMounted(() => {
	document.addEventListener("keydown", handleEsc)
})

onUnmounted(() => {
	document.removeEventListener("keydown", handleEsc)
	document.body.style.overflow = ""
})

// Body scroll lock
watch(
	() => props.isOpen || hashOpen.value,
	(open) => {
		document.body.style.overflow = open ? "hidden" : ""
	},
	{ immediate: true },
)
</script>

<style scoped>
/* Modal Transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
	transition: opacity 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
	opacity: 0;
}
</style>
