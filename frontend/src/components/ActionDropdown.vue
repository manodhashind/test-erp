<template>
	<div ref="wrapperRef" class="relative inline-block">
		<Button
			ref="buttonRef"
			:variant="variant"
			:disabled="buttonDisabled"
			class="inline-flex min-w-[120px] items-center justify-between gap-2 px-3 py-2.5 text-xs font-semibold sm:min-w-[140px] sm:px-4 sm:text-sm"
			aria-haspopup="menu"
			:aria-expanded="dropdownOpen.toString()"
			:aria-disabled="buttonDisabled ? 'true' : 'false'"
			@click="toggleDropdown"
		>
			<span class="truncate">{{ label }}</span>
			<Icon icon="chevron-down" size="18" />
		</Button>

		<transition name="dropdown">
			<div
				v-if="dropdownOpen && hasVisibleActions"
				ref="menuRef"
				role="menu"
				:class="[
					'absolute z-[1000] mt-2 max-h-[min(400px,calc(100vh-120px))] overflow-y-auto rounded-xl border border-slate-200 bg-white shadow-2xl ring-1 ring-slate-100 transition-all duration-200 dark:border-slate-800 dark:bg-slate-900',
					'min-w-[200px] max-w-[calc(100vw-2rem)] sm:max-w-[320px] lg:max-w-[420px]',
					positionClass,
				]"
			>
				<div class="flex flex-col gap-1 p-1 sm:p-2">
					<button
						v-for="item in visibleActions"
						:key="item.action || item.label"
						type="button"
						role="menuitem"
						:class="[
							'dark:focus-visible:ring-offset-slate-950 flex w-full items-center gap-2 rounded-lg px-2 py-2.5 text-left text-xs font-medium transition-colors duration-150 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-white sm:gap-3 sm:px-3 sm:py-3 sm:text-sm',
							item.danger
								? 'dark:hover:bg-red-950/60 text-red-600 hover:bg-red-50 dark:text-red-300'
								: 'text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-800',
							item.disabled
								? 'cursor-not-allowed opacity-60 hover:bg-transparent'
								: 'cursor-pointer',
						]"
						:disabled="item.disabled"
						:aria-disabled="item.disabled ? 'true' : 'false'"
						@click="() => handleActionSelect(item)"
					>
						<Icon
							v-if="item.icon"
							:icon="item.icon"
							size="16"
							class="hidden flex-shrink-0 sm:flex"
						/>
						<span class="whitespace-normal break-words">{{ item.label }}</span>
					</button>
				</div>
			</div>
		</transition>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"
import Button from "./common/Button.vue"
import Icon from "./Icon.vue"
import { useUIPermissions } from "@/composables/useUIPermissions"

const props = defineProps({
	label: {
		type: String,
		default: "Actions",
	},
	actions: {
		type: Array,
		required: true,
	},
	variant: {
		type: String,
		default: "primary",
	},
	disabled: {
		type: Boolean,
		default: false,
	},
	position: {
		type: String,
		default: "right",
	},
})

const emit = defineEmits(["select", "open", "close"])
const router = useRouter()
const { can } = useUIPermissions()

const dropdownOpen = ref(false)
const wrapperRef = ref(null)
const buttonRef = ref(null)
const menuRef = ref(null)

const normalizeLabel = (value) => {
	if (!value || typeof value !== "string") return "Unnamed action"
	return value
		.replace(/[_-]+/g, " ")
		.replace(/\b\w/g, (char) => char.toUpperCase())
		.trim()
}

const visibleActions = computed(() => {
	if (!Array.isArray(props.actions)) return []

	return props.actions
		.map((action) => ({
			type: action.type || "event",
			label: action.label || normalizeLabel(action.action),
			icon: action.icon || null,
			action: action.action,
			to: action.to,
			href: action.href,
			disabled: !!action.disabled,
			hidden: !!action.hidden,
			danger: !!action.danger,
			permission: action.permission || null,
		}))
		.filter((item) => {
			if (item.hidden) return false
			if (!item.permission) return true
			const { resourceType, resourceName, action } = item.permission
			return !!resourceType && !!resourceName && can(resourceType, resourceName, action || "read")
		})
})

const hasVisibleActions = computed(() => visibleActions.value.length > 0)
const buttonDisabled = computed(() => props.disabled || !hasVisibleActions.value)

const positionClass = computed(() => {
	const placement = (props.position || "right").toLowerCase()

	// Mobile: keep the menu inside the viewport regardless of trigger position.
	// We center the menu and let its max-width clamp it.
	if (placement === "center") return "left-1/2 -translate-x-1/2"

	if (placement === "left") {
		return "left-1/2 -translate-x-1/2 sm:left-0 sm:translate-x-0"
	}

	// default/right
	return "left-1/2 -translate-x-1/2 sm:right-0 sm:left-auto sm:translate-x-0"
})

const toggleDropdown = () => {
	if (buttonDisabled.value) return

	dropdownOpen.value = !dropdownOpen.value
	emit(dropdownOpen.value ? "open" : "close")
}

const closeDropdown = () => {
	if (!dropdownOpen.value) return
	dropdownOpen.value = false
	emit("close")
}

const handleActionSelect = (item) => {
	if (item.disabled) return

	if (item.type === "route" && item.to) {
		router.push(item.to)
	} else if (item.type === "link" && item.href) {
		window.open(item.href, "_blank")
	} else {
		emit("select", item)
	}

	closeDropdown()
}

const handleDocumentClick = (event) => {
	const target = event.target
	if (!dropdownOpen.value) return
	if (wrapperRef.value?.contains(target)) return
	closeDropdown()
}

const handleDocumentKeydown = (event) => {
	if (!dropdownOpen.value) return
	if (event.key === "Escape") {
		closeDropdown()
	}
}

onMounted(() => {
	document.addEventListener("click", handleDocumentClick)
	document.addEventListener("keydown", handleDocumentKeydown)
})

onUnmounted(() => {
	document.removeEventListener("click", handleDocumentClick)
	document.removeEventListener("keydown", handleDocumentKeydown)
})
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
	transition:
		opacity 0.18s ease,
		transform 0.18s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
	opacity: 0;
	transform: translateY(-8px);
}
</style>
