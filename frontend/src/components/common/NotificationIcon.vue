<template>
	<div class="relative">
		<button
			class="relative flex h-10 w-10 cursor-pointer items-center justify-center rounded-lg border-0 bg-slate-100 text-slate-600 transition-all duration-200 hover:bg-slate-200 focus:outline-none active:scale-95 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700"
			:class="{ '!text-primary dark:!text-primary-light': hasNotifications }"
			aria-label="Notifications"
			@click="handleClick"
		>
			<svg
				width="20"
				height="20"
				viewBox="0 0 20 20"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					d="M15 6.66667C15 5.34058 14.4732 4.06881 13.5355 3.13113C12.5979 2.19345 11.3261 1.66667 10 1.66667C8.67392 1.66667 7.40215 2.19345 6.46447 3.13113C5.52678 4.06881 5 5.34058 5 6.66667C5 12.5 2.5 14.1667 2.5 14.1667H17.5C17.5 14.1667 15 12.5 15 6.66667Z"
					stroke="currentColor"
					stroke-width="1.5"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
				<path
					d="M11.4417 17.5C11.2952 17.7526 11.0849 17.9622 10.8319 18.1079C10.5789 18.2537 10.292 18.3304 10 18.3304C9.70802 18.3304 9.42116 18.2537 9.16816 18.1079C8.91516 17.9622 8.70484 17.7526 8.55835 17.5"
					stroke="currentColor"
					stroke-width="1.5"
					stroke-linecap="round"
					stroke-linejoin="round"
				/>
			</svg>
			<span
				v-if="hasNotifications && count > 0"
				class="absolute -top-0.5 -right-0.5 min-w-[18px] rounded-full border-2 border-white bg-red-500 px-1.5 py-0.5 text-center text-[10px] font-semibold leading-none text-white dark:border-slate-800"
			>
				{{ count > 99 ? "99+" : count }}
			</span>
		</button>

		<!-- Notification dropdown -->
		<transition name="dropdown">
			<div
				v-if="showDropdown"
				class="absolute top-[calc(100%+8px)] right-0 z-[1000] max-h-[480px] w-[360px] overflow-hidden rounded-xl border border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900"
			>
				<div
					class="flex items-center justify-between border-b border-slate-100 p-4 dark:border-slate-800"
				>
					<h3 class="m-0 text-base font-semibold text-slate-900 dark:text-slate-100">
						Notifications
					</h3>
					<button
						class="cursor-pointer rounded border-0 bg-transparent p-1 px-2 text-xs font-medium text-primary transition-colors hover:bg-slate-50 dark:text-primary-light dark:hover:bg-slate-800"
						@click="markAllAsRead"
					>
						Mark all as read
					</button>
				</div>
				<div class="max-h-[400px] overflow-y-auto">
					<div
						v-for="notification in notifications"
						:key="notification.id"
						class="flex cursor-pointer flex-col gap-1 border-b border-slate-50 p-4 transition-colors duration-200 dark:border-slate-800/50"
						:class="[
							notification.read
								? 'hover:bg-slate-50 dark:hover:bg-slate-800/40'
								: 'dark:hover:bg-primary/15 bg-primary/5 hover:bg-primary/10 dark:bg-primary/10',
						]"
						@click="handleNotificationClick(notification)"
					>
						<div class="flex flex-col gap-1">
							<p class="m-0 text-sm font-semibold text-slate-900 dark:text-slate-100">
								{{ notification.title }}
							</p>
							<p class="m-0 text-xs leading-normal text-slate-500 dark:text-slate-400">
								{{ notification.message }}
							</p>
							<span class="mt-1 text-[10px] text-slate-400 dark:text-slate-500">{{
								notification.time
							}}</span>
						</div>
					</div>
					<div
						v-if="notifications.length === 0"
						class="py-12 text-center text-sm text-slate-400 dark:text-slate-500"
					>
						No new notifications
					</div>
				</div>
			</div>
		</transition>
	</div>
</template>

<script>
export default {
	name: "NotificationIcon",
	props: {
		count: {
			type: Number,
			default: 0,
		},
		notifications: {
			type: Array,
			default: () => [],
		},
	},
	emits: ["click", "notification-click", "mark-all-read"],
	data() {
		return {
			showDropdown: false,
		}
	},
	computed: {
		hasNotifications() {
			return this.count > 0
		},
	},
	mounted() {
		document.addEventListener("click", this.handleOutsideClick)
	},
	beforeUnmount() {
		document.removeEventListener("click", this.handleOutsideClick)
	},
	methods: {
		handleClick() {
			this.showDropdown = !this.showDropdown
			this.$emit("click")
		},
		handleNotificationClick(notification) {
			this.$emit("notification-click", notification)
			this.showDropdown = false
		},
		markAllAsRead() {
			this.$emit("mark-all-read")
		},
		closeDropdown() {
			this.showDropdown = false
		},
	},
}
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
