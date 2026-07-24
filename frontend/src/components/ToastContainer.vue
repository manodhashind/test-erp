<template>
	<div class="pointer-events-none fixed bottom-6 right-6 z-[99999] flex flex-col-reverse gap-3">
		<TransitionGroup name="toast">
			<Toast
				v-for="toast in toasts"
				:key="toast.id"
				v-bind="toast"
				@close="removeToast(toast.id)"
			/>
		</TransitionGroup>
	</div>
</template>

<script setup>
import { useToast } from "../services/toastService"
import Toast from "./Toast.vue"

const { toasts, removeToast } = useToast()
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
	transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.toast-enter-from {
	opacity: 0;
	transform: translateX(30px) scale(0.9);
}

.toast-leave-to {
	opacity: 0;
	transform: translateX(30px) scale(0.9);
}

.toast-move {
	transition: transform 0.4s ease;
}
</style>
