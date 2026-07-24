<template>
	<Teleport to="body">
		<Transition name="modal">
			<!--
				Scrolling lives here (the backdrop), NOT inside the modal body.
				This means dropdowns / date-pickers / autocompletes can overflow freely
				beyond the modal card — they are never clipped by an inner overflow container.
			-->
			<div
				v-if="modelValue || hashOpen"
				class="dark:bg-slate-950/60 fixed inset-0 z-[9999] overflow-y-auto bg-slate-900/40 backdrop-blur-sm"
				@click.self="handleCancel"
			>
				<!-- Vertical centering wrapper -->
				<div class="flex min-h-full items-center justify-center p-5">
					<div
						class="relative flex max-h-[90vh] w-full flex-col rounded-2xl border border-slate-200 bg-app-bg-secondary shadow-2xl dark:border-slate-700 dark:bg-app-bg-dark"
						:class="sizeClass"
					>
						<!-- Header -->
						<div
							class="flex shrink-0 justify-between rounded-t-2xl border-b border-slate-200 bg-app-bg-secondary px-5 dark:border-slate-700 dark:bg-app-bg-dark"
							:class="subtitle || icon ? 'items-start py-4' : 'items-center py-3'"
						>
							<div
								class="flex flex-1 gap-4"
								:class="subtitle || icon ? 'items-start' : 'items-center'"
							>
								<div
									v-if="icon"
									class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary/70"
								>
									<img
										:src="icon"
										:alt="title"
										class="h-7 w-7 object-contain brightness-0 invert"
									/>
								</div>
								<div class="flex-1">
									<h2 class="m-0 font-sans text-lg font-bold text-slate-900 dark:text-white">
										{{ title }}
									</h2>
									<p
										v-if="subtitle"
										class="m-0 mt-1 font-sans text-sm text-slate-500 dark:text-slate-400"
									>
										{{ subtitle }}
									</p>
								</div>
							</div>
							<button
								class="flex shrink-0 cursor-pointer items-center justify-center rounded-lg border-none bg-transparent p-2 text-slate-400 transition-all hover:bg-slate-100 hover:text-slate-600 dark:text-slate-500 dark:hover:bg-slate-800 dark:hover:text-slate-300"
								:disabled="loading"
								@click="handleCancel"
							>
								<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
									<path
										d="M15 5L5 15M5 5L15 15"
										stroke="currentColor"
										stroke-width="2"
										stroke-linecap="round"
									/>
								</svg>
							</button>
						</div>

						<!-- Body – scrolls internally so header and footer stay pinned -->
						<div
							class="flex-1 overflow-y-auto bg-app-bg-secondary px-4 pb-4 pt-3 text-slate-700 dark:bg-app-bg-dark dark:text-slate-300"
						>
							<form class="pb-2" @submit.prevent="handleSubmit">
								<slot name="form" :form-data="formData">
									<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
										<div
											v-for="field in fields"
											:key="field.name"
											class="flex flex-col gap-1.5"
											:class="{ 'md:col-span-2': field.fullWidth }"
										>
											<label
												:for="field.name"
												class="font-sans text-sm font-semibold text-slate-700 dark:text-slate-200"
											>
												{{ field.label }}
												<span v-if="field.required" class="ml-0.5 text-red-500">*</span>
											</label>

											<FieldRenderer
												v-if="field.type"
												v-model="formData[field.name]"
												:field="{
													type: field.type,
													label: '',
													placeholder: field.placeholder,
													required: field.required,
													options: field.options,
													...field.props,
												}"
											/>

											<slot
												:name="`field-${field.name}`"
												:field="field"
												:value="formData[field.name]"
											/>

											<span
												v-if="errors[field.name]"
												class="mt-1 font-sans text-xs text-red-500"
												>{{ errors[field.name] }}</span
											>
											<span
												v-if="field.hint"
												class="mt-1 font-sans text-xs text-slate-500 dark:text-slate-400"
												>{{ field.hint }}</span
											>
										</div>
									</div>
								</slot>

								<slot :form-data="formData" />
							</form>
						</div>

						<!-- Footer – sticky at the bottom of the backdrop scroll area -->
						<div
							class="flex shrink-0 items-center justify-between gap-4 rounded-b-2xl border-t border-slate-200 bg-app-bg-secondary px-5 py-3 dark:border-slate-700 dark:bg-app-bg-dark"
						>
							<div class="flex-1 font-sans text-sm text-slate-500 dark:text-slate-400">
								<slot name="footer-info" />
							</div>
							<div class="flex gap-3">
								<button
									type="button"
									class="cursor-pointer rounded-lg border border-slate-200 bg-white px-5 py-2.5 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700/80"
									:disabled="loading"
									@click="handleCancel"
								>
									{{ cancelText }}
								</button>
								<button
									type="button"
									class="flex cursor-pointer items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-50"
									:disabled="loading || !isValid"
									@click="handleSubmit"
								>
									<span
										v-if="loading"
										class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"
									/>
									{{ loading ? loadingText : submitText }}
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</Transition>
	</Teleport>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from "vue"
import { FieldRenderer } from "../fields"
import { useModalHashRoute } from "@/composables/useModalHashRoute"

const props = defineProps({
	modelValue: {
		type: Boolean,
		default: false,
	},
	title: {
		type: String,
		required: true,
	},
	subtitle: {
		type: String,
		default: "",
	},
	icon: {
		type: String,
		default: null,
	},
	fields: {
		type: Array,
		default: () => [],
	},
	initialData: {
		type: Object,
		default: () => ({}),
	},
	submitText: {
		type: String,
		default: "Submit",
	},
	cancelText: {
		type: String,
		default: "Cancel",
	},
	loadingText: {
		type: String,
		default: "Saving...",
	},
	loading: {
		type: Boolean,
		default: false,
	},
	size: {
		type: String,
		default: "md",
		validator: (value) => ["sm", "md", "lg", "xl", "2xl"].includes(value),
	},
	validateOnChange: {
		type: Boolean,
		default: true,
	},
	// URL hash fragment to use when open; falls back to the title.
	hashId: {
		type: String,
		default: "",
	},
	// Opt out of URL hash routing for this modal.
	noHash: {
		type: Boolean,
		default: false,
	},
})

const emit = defineEmits(["update:modelValue", "submit", "cancel", "update:formData"])

const formData = ref({})
const errors = ref({})

const notifyParentClose = () => {
	if (!props.loading) {
		emit("update:modelValue", false)
		emit("cancel")
	}
}

// `handleCancel` (used by the close button / overlay / cancel button) also
// clears the hash-restored open state, then notifies the parent.
const { hashOpen, close: handleCancel } = useModalHashRoute({
	isOpen: () => props.modelValue,
	close: notifyParentClose,
	hashId: () => props.hashId || props.title,
	enabled: () => !props.noHash,
})

const sizeClass = computed(() => {
	return {
		"max-w-[400px]": props.size === "sm",
		"max-w-[600px]": props.size === "md",
		"max-w-[800px]": props.size === "lg",
		"max-w-[1000px]": props.size === "xl",
		"max-w-[1200px]": props.size === "2xl",
	}
})

const isValid = computed(() => {
	if (props.fields.length === 0) return true

	return props.fields.every((field) => {
		if (!field.required) return true
		const value = formData.value[field.name]
		return value !== null && value !== undefined && value !== ""
	})
})

// Initialize form data
watch(
	() => props.modelValue || hashOpen.value,
	(newVal) => {
		if (newVal) {
			formData.value = { ...props.initialData }
			errors.value = {}

			// Initialize empty fields
			props.fields.forEach((field) => {
				if (!(field.name in formData.value)) {
					formData.value[field.name] = field.default ?? null
				}
			})
		}
	},
	{ immediate: true },
)

// Validate field
const validateField = (field) => {
	if (!props.validateOnChange) return true

	const value = formData.value[field.name]

	if (field.required && (value === null || value === undefined || value === "")) {
		errors.value[field.name] = `${field.label} is required`
		return false
	}

	if (field.validate && typeof field.validate === "function") {
		const error = field.validate(value, formData.value)
		if (error) {
			errors.value[field.name] = error
			return false
		}
	}

	delete errors.value[field.name]
	return true
}

// Watch form data changes
watch(
	formData,
	(newData) => {
		emit("update:formData", newData)

		if (props.validateOnChange) {
			props.fields.forEach((field) => {
				if (field.name in newData) {
					validateField(field)
				}
			})
		}
	},
	{ deep: true },
)

const handleSubmit = () => {
	// Validate all fields
	let allValid = true
	props.fields.forEach((field) => {
		if (!validateField(field)) {
			allValid = false
		}
	})

	if (allValid) {
		emit("submit", formData.value)
	}
}

function onKeydown(e) {
	if ((e.ctrlKey || e.metaKey) && e.key === "s") {
		e.preventDefault()
		handleSubmit()
	}
}

watch(
	() => props.modelValue || hashOpen.value,
	(isOpen) => {
		if (isOpen) {
			window.addEventListener("keydown", onKeydown)
		} else {
			window.removeEventListener("keydown", onKeydown)
		}
	},
)
onUnmounted(() => window.removeEventListener("keydown", onKeydown))
</script>

<script>
export default {
	name: "FormModal",
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
	transition: opacity 0.25s ease;
}

.modal-enter-from,
.modal-leave-to {
	opacity: 0;
}
</style>
