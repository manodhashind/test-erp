<template>
	<div ref="profileWrapper" class="relative w-full">
		<button
			class="flex w-full cursor-pointer items-center gap-3 rounded-lg border-0 bg-transparent p-1 transition-all duration-200 hover:bg-primary/[0.06] focus:outline-none dark:hover:bg-primary-light/10"
			:class="[
				showDropdown ? 'bg-primary/10 dark:bg-primary-light/10' : '',
				compact ? 'justify-center' : 'justify-start',
			]"
			@click="toggleDropdown"
		>
			<img
				:src="avatarUrl"
				:alt="userName"
				class="h-10 w-10 shrink-0 rounded-full border-2 border-primary object-cover shadow-sm dark:border-primary-light"
				@error="handleImageError"
			/>
			<div
				class="flex min-w-0 flex-col gap-0.5 overflow-hidden text-left transition-all duration-300 mobile:hidden tablet:hidden"
				:class="compact ? 'max-w-0 opacity-0' : 'max-w-[160px] flex-1 opacity-100'"
			>
				<div
					class="truncate font-sans text-sm font-semibold leading-snug text-primary dark:text-white"
				>
					{{ userName }}
				</div>
				<div
					class="truncate font-sans text-xs font-normal leading-snug text-primary/60 dark:text-slate-400"
				>
					{{ userRole }}
				</div>
			</div>
		</button>

		<!-- User dropdown menu -->
		<transition name="dropdown">
			<div
				v-if="showDropdown"
				:class="[
					'absolute z-[9999] max-h-[80vh] w-[280px] overflow-y-auto rounded-xl border border-primary/20 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900',
					dropdownPlacement === 'top' ? 'bottom-[calc(100%+8px)]' : 'top-[calc(100%+8px)]',
					align === 'left' ? 'left-0' : 'right-0',
				]"
			>
				<div class="dark:bg-slate-950 flex items-center gap-3 bg-slate-50 p-4">
					<img
						:src="avatarUrl"
						:alt="userName"
						class="h-12 w-12 shrink-0 rounded-full object-cover"
					/>
					<div class="min-w-0 flex-1">
						<div
							class="truncate text-sm font-semibold leading-snug text-slate-900 dark:text-slate-100"
						>
							{{ userName }}
						</div>
						<div class="truncate text-xs leading-snug text-slate-500 dark:text-slate-400">
							{{ userEmail }}
						</div>
					</div>
				</div>

				<div class="h-px bg-slate-100 dark:bg-slate-800" />

				<slot name="extra-items" />

				<div class="flex flex-col gap-0.5 p-2">
					<a
						v-for="item in menuItems"
						:key="item.id"
						class="flex cursor-pointer items-center gap-3 rounded-lg p-2.5 px-3 text-sm font-medium text-slate-600 transition-colors duration-200 hover:bg-primary/[0.04] hover:text-primary dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-primary-light"
						:class="{
							'dark:hover:!bg-red-950/20 !text-red-500 hover:!bg-red-50/50 hover:!text-red-600 dark:!text-red-400 dark:hover:!text-red-300':
								item.danger,
						}"
						@click="handleMenuClick(item)"
					>
						<component :is="item.icon" class="h-4 w-4 shrink-0" />
						<span>{{ item.label }}</span>
					</a>
				</div>
			</div>
		</transition>

		<!-- Logout Confirmation Modal -->
		<Modal
			:is-open="showLogoutModal"
			title="Confirm Logout"
			size="sm"
			:show-footer="true"
			@close="closeLogoutModal"
		>
			<div class="flex flex-col items-center gap-5 p-4 text-center">
				<div class="flex items-center justify-center">
					<svg width="48" height="48" viewBox="0 0 48 48" fill="none">
						<circle cx="24" cy="24" r="20" fill="#FEE2E2" />
						<path
							d="M18 30H15C13.8954 30 13 29.1046 13 28V16C13 14.8954 13.8954 14 15 14H18M26 34L35 24M35 24L26 14M35 24H18"
							stroke="#DC2626"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						/>
					</svg>
				</div>

				<p class="m-0 font-sans text-sm leading-relaxed text-slate-500 dark:text-slate-400">
					{{ logoutMessage }}
				</p>

				<div
					v-if="userFullName"
					class="dark:bg-slate-950 flex w-full flex-col items-center gap-1 rounded-lg bg-slate-50 p-3 px-4"
				>
					<span
						class="font-sans text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500"
						>Logged in as</span
					>
					<span class="font-sans text-sm font-bold text-slate-900 dark:text-slate-100">{{
						userFullName
					}}</span>
				</div>
			</div>

			<template #footer>
				<button
					class="cursor-pointer rounded-lg border border-slate-200 bg-transparent px-5 py-2.5 text-sm font-semibold text-slate-600 transition-colors hover:bg-slate-50 focus:outline-none active:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800/80 dark:active:bg-slate-800"
					:disabled="isLoggingOut"
					@click="closeLogoutModal"
				>
					Cancel
				</button>
				<button
					class="flex cursor-pointer items-center gap-2 rounded-lg border-0 bg-red-600 px-5 py-2.5 text-sm font-semibold text-white transition-all hover:-translate-y-[1px] hover:bg-red-700 focus:outline-none active:translate-y-0 active:bg-red-800 disabled:cursor-not-allowed disabled:opacity-50"
					:disabled="isLoggingOut"
					@click="handleLogoutConfirm"
				>
					<span
						v-if="isLoggingOut"
						class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
					/>
					{{ isLoggingOut ? "Logging out..." : "Logout" }}
				</button>
			</template>
		</Modal>
	</div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from "vue"
import { useRoute } from "vue-router"
import Modal from "./Modal.vue"
import { ApiService } from "../../services/api.js"
import { useToast } from "../../services/toastService"

const props = defineProps({
	userName: {
		type: String,
		default: "Alex Rivera",
	},
	userRole: {
		type: String,
		default: "Fleet Admin",
	},
	userEmail: {
		type: String,
		default: "alex@truckblue.com",
	},
	avatarUrl: {
		type: String,
		default: "",
	},
	compact: {
		type: Boolean,
		default: false,
	},
	dropdownPlacement: {
		type: String,
		default: "bottom", // 'bottom' | 'top'
	},
	align: {
		type: String,
		default: "right", // 'right' | 'left'
	},
})

const emit = defineEmits(["menu-click", "profile-click"])

// Icons as components
const ProfileIcon = {
	template: `
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M13.3333 14V12.6667C13.3333 11.9594 13.0524 11.2811 12.5523 10.781C12.0522 10.281 11.3739 10 10.6667 10H5.33333C4.62609 10 3.94781 10.281 3.44772 10.781C2.94762 11.2811 2.66667 11.9594 2.66667 12.6667V14M10.6667 4.66667C10.6667 6.13943 9.47276 7.33333 8 7.33333C6.52724 7.33333 5.33333 6.13943 5.33333 4.66667C5.33333 3.19391 6.52724 2 8 2C9.47276 2 10.6667 3.19391 10.6667 4.66667Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `,
}
const HelpIcon = {
	template: `
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M8 14.6667C11.6819 14.6667 14.6667 11.6819 14.6667 8C14.6667 4.3181 11.6819 1.33333 8 1.33333C4.3181 1.33333 1.33333 4.3181 1.33333 8C1.33333 11.6819 4.3181 14.6667 8 14.6667Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M6.06 6.00001C6.21674 5.55446 6.52609 5.17875 6.93329 4.93944C7.34049 4.70012 7.81926 4.61264 8.28479 4.69249C8.75031 4.77234 9.17255 5.01436 9.47672 5.37569C9.78089 5.73702 9.94737 6.19436 9.94667 6.66668C9.94667 8.00001 7.94667 8.66668 7.94667 8.66668M8 11.3333H8.00667" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `,
}
const LogoutIcon = {
	template: `
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M6 14 H3.33333C2.97971 14 2.64057 13.8595 2.39052 13.6095C2.14048 13.3594 2 13.0203 2 12.6667V3.33333C2 2.97971 2.14048 2.64057 2.39052 2.39052C2.64057 2.14048 2.97971 2 3.33333 2H6M10.6667 11.3333L14 8M14 8L10.6667 4.66667M14 8H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `,
}

// State
const route = useRoute()
const showDropdown = ref(false)
const showLogoutModal = ref(false)
const isLoggingOut = ref(false)
const toast = useToast()

// Close the dropdown on any navigation, including links placed in the
// `extra-items` slot (e.g. Developer Settings) that don't go through handleMenuClick.
watch(
	() => route.fullPath,
	() => {
		showDropdown.value = false
	},
)

const logoutMessage =
	"Are you sure you want to logout? You'll need to log in again to access your dashboard."

const userFullName = computed(() => {
	return localStorage.getItem("full_name") || props.userName
})

const menuItems = [
	{ id: "profile", label: "My Profile", icon: ProfileIcon, action: "profile" },
	{ id: "help", label: "Help & Support", icon: HelpIcon, action: "help" },
	{ id: "logout", label: "Logout", icon: LogoutIcon, action: "logout", danger: true },
]

// Methods
const generateInitialsAvatar = () => {
	const initials = props.userName
		.split(" ")
		.map((n) => n[0])
		.join("")
		.toUpperCase()
		.substring(0, 2)

	const primaryColor =
		getComputedStyle(document.documentElement).getPropertyValue("--color-primary").trim() ||
		"#6742CF"

	const svg = `
    <svg width="40" height="40" xmlns="http://www.w3.org/2000/svg">
      <rect width="40" height="40" fill="${primaryColor}"/>
      <text x="50%" y="50%" font-family="Inter, sans-serif" font-size="14" font-weight="600" fill="white" text-anchor="middle" dy=".3em">${initials}</text>
    </svg>
  `
	return "data:image/svg+xml;base64," + btoa(svg)
}

const toggleDropdown = () => {
	showDropdown.value = !showDropdown.value
	emit("profile-click")
}

const handleMenuClick = (item) => {
	if (item.action === "logout") {
		showLogoutModal.value = true
	} else {
		emit("menu-click", item.action)
	}
	showDropdown.value = false
}

const closeLogoutModal = () => {
	if (!isLoggingOut.value) {
		showLogoutModal.value = false
	}
}

const handleLogoutConfirm = async () => {
	isLoggingOut.value = true
	try {
		await ApiService.logout()
		showLogoutModal.value = false
		emit("menu-click", "logout")
	} catch (error) {
		toast.error("Logout Failed", {
			message: error.message || "Could not logout. Please try again.",
		})
		isLoggingOut.value = false
	}
}

const handleImageError = (e) => {
	e.target.src = generateInitialsAvatar()
}

const profileWrapper = ref(null)
const handleClickOutside = (e) => {
	if (profileWrapper.value && !profileWrapper.value.contains(e.target)) {
		showDropdown.value = false
	}
}

onMounted(() => {
	document.addEventListener("click", handleClickOutside)
	if (!props.avatarUrl) {
		nextTick(() => {
			const img = document.querySelector(".user-avatar")
			if (img) img.src = generateInitialsAvatar()
		})
	}
})

onUnmounted(() => {
	document.removeEventListener("click", handleClickOutside)
})
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
	transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
	opacity: 0;
	transform: translateY(-10px);
}
</style>
