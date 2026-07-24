<template>
	<Teleport to="body">
		<transition name="sidepanel">
			<div
				v-if="isOpen || hashOpen"
				class="sidepanel-overlay dark:bg-slate-950/60 fixed inset-0 z-[9999] flex h-screen justify-end bg-slate-900/40 backdrop-blur-sm"
				role="dialog"
				:aria-labelledby="titleId"
				aria-modal="true"
				@click.self="closeOnOverlay && close()"
			>
				<aside
					class="sidepanel-aside flex h-screen w-full min-w-[340px] flex-col overflow-hidden border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-app-bg-dark tablet:w-1/2"
					:class="[widthClass, customClass]"
				>
					<!-- Header -->
					<div
						v-if="showHeader"
						class="flex shrink-0 items-center justify-between gap-3 border-b border-slate-200 px-5 py-4 dark:border-slate-800"
					>
						<slot name="header">
							<h3
								:id="titleId"
								class="m-0 truncate font-sans text-base font-bold text-on-surface dark:text-white"
							>
								{{ title }}
							</h3>
							<button
								v-if="showCloseButton"
								type="button"
								class="-mr-1 flex shrink-0 cursor-pointer items-center justify-center rounded-lg border-none bg-transparent p-2 text-slate-400 transition-all hover:bg-slate-100 hover:text-slate-600 dark:text-slate-500 dark:hover:bg-slate-800 dark:hover:text-slate-300"
								aria-label="Close panel"
								@click="close"
							>
								<Icon icon="close" :size="20" color="currentColor" />
							</button>
						</slot>
					</div>

					<!-- Body -->
					<div class="flex-1 overflow-y-auto p-5 text-on-surface dark:text-slate-300">
						<slot />
					</div>

					<!-- Footer -->
					<div
						v-if="$slots.footer"
						class="flex shrink-0 justify-end gap-3 border-t border-slate-200 bg-slate-50/60 px-5 py-4 dark:border-slate-800 dark:bg-slate-900/30"
					>
						<slot name="footer" />
					</div>
				</aside>
			</div>
		</transition>
	</Teleport>
</template>

<script setup>
import { computed, onMounted, onUnmounted, watch } from "vue"
import Icon from "../Icon.vue"
import { useModalHashRoute } from "@/composables/useModalHashRoute"

const props = defineProps({
	isOpen: { type: Boolean, required: true },
	title: { type: String, default: "" },
	showHeader: { type: Boolean, default: true },
	showCloseButton: { type: Boolean, default: true },
	closeOnOverlay: { type: Boolean, default: true },
	customClass: { type: String, default: "" },
	// URL hash fragment to use when open; falls back to the title.
	hashId: { type: String, default: "" },
	// Opt out of URL hash routing for this panel.
	noHash: { type: Boolean, default: false },
	// Desktop width of the panel as a fraction of the page
	width: {
		type: String,
		default: "half",
		validator: (v) => ["quarter", "third", "half"].includes(v),
	},
})

const WIDTH_CLASSES = {
	quarter: "desktop:w-1/4",
	third: "desktop:w-1/3",
	half: "desktop:w-1/2",
}
const widthClass = computed(() => WIDTH_CLASSES[props.width] ?? WIDTH_CLASSES.quarter)

const emit = defineEmits(["close"])

const titleId = `sidepanel-title-${Math.random().toString(36).substr(2, 9)}`

const { hashOpen, close } = useModalHashRoute({
	isOpen: () => props.isOpen,
	close: () => emit("close"),
	hashId: () => props.hashId || props.title,
	enabled: () => !props.noHash,
})

const handleEsc = (e) => {
	if (e.key === "Escape" && (props.isOpen || hashOpen.value)) close()
}

onMounted(() => document.addEventListener("keydown", handleEsc))
onUnmounted(() => {
	document.removeEventListener("keydown", handleEsc)
	document.body.style.overflow = ""
})

watch(
	() => props.isOpen || hashOpen.value,
	(open) => {
		document.body.style.overflow = open ? "hidden" : ""
	},
	{ immediate: true },
)
</script>

<script>
export default { name: "SidePanel" }
</script>

<style scoped>
/* Backdrop fade (overlay is the transition root) */
.sidepanel-enter-active,
.sidepanel-leave-active {
	transition: opacity 0.25s ease;
}
.sidepanel-enter-from,
.sidepanel-leave-to {
	opacity: 0;
}

/* Panel slide — runs in parallel with the backdrop fade */
.sidepanel-enter-active .sidepanel-aside,
.sidepanel-leave-active .sidepanel-aside {
	transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.sidepanel-enter-from .sidepanel-aside,
.sidepanel-leave-to .sidepanel-aside {
	transform: translateX(100%);
}
</style>
