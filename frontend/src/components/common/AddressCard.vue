<template>
	<div
		class="rounded-xl border border-outline-variant bg-surface-container p-4 dark:border-slate-700 dark:bg-slate-800/60"
	>
		<!-- Header row: icon + title + edit -->
		<div class="flex items-start justify-between gap-2">
			<div class="flex min-w-0 flex-1 items-start gap-3">
				<!-- Icon badge -->
				<div
					class="flex h-9 w-9 shrink-0 items-center justify-center rounded-[10px] bg-green-100 dark:bg-green-900/30"
				>
					<Icon icon="map-marker" :size="17" class="text-green-600 dark:text-green-400" />
				</div>
				<!-- Title + type + primary badges -->
				<div class="min-w-0 flex-1">
					<p class="truncate text-sm font-bold text-on-surface dark:text-slate-100">
						{{ address.address_title }}
					</p>
					<div class="mt-0.5 flex flex-wrap gap-1">
						<span
							v-if="address.is_primary_address === 1 || address.is_primary_address === true"
							class="rounded-full bg-primary/10 px-1.5 py-0.5 text-[10px] font-bold text-primary dark:bg-primary/20"
						>
							Primary
						</span>
						<span
							v-if="address.address_type"
							class="rounded-full bg-surface-container px-1.5 py-0.5 text-[10px] font-semibold text-on-surface-variant dark:bg-slate-700 dark:text-slate-400"
						>
							{{ address.address_type }}
						</span>
					</div>
				</div>
			</div>

			<!-- Edit button -->
			<button
				v-if="canEdit"
				class="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg text-on-surface-variant transition-colors hover:bg-surface-container hover:text-on-surface dark:text-slate-500 dark:hover:bg-slate-700 dark:hover:text-slate-300"
				title="Edit address"
				@click="$emit('edit', address)"
			>
				<Icon icon="pencil" :size="14" />
			</button>
		</div>

		<!-- Address details -->
		<div class="mt-3 space-y-1.5 border-t border-outline-variant pt-3 dark:border-slate-700">
			<div v-if="address.address_line1 || cityLine" class="flex min-w-0 items-start gap-2">
				<Icon
					icon="map-marker-outline"
					:size="12"
					class="mt-0.5 shrink-0 text-on-surface-variant dark:text-slate-500"
				/>
				<div
					class="min-w-0 flex-1 break-words text-xs leading-relaxed text-on-surface-variant dark:text-slate-300"
				>
					<p v-if="address.address_line1">{{ address.address_line1 }}</p>
					<p v-if="address.address_line2" class="text-on-surface-variant/70 dark:text-slate-400">
						{{ address.address_line2 }}
					</p>
					<p v-if="resolving" class="mt-0.5 flex gap-2">
						<span class="h-3 w-16 animate-pulse rounded bg-outline-variant dark:bg-slate-700" />
						<span class="h-3 w-10 animate-pulse rounded bg-outline-variant dark:bg-slate-700" />
					</p>
					<p v-else-if="cityLine" class="font-medium">{{ cityLine }}</p>
					<p
						v-if="address.country"
						class="text-[11px] text-on-surface-variant/60 dark:text-slate-500"
					>
						{{ address.country }}
					</p>
				</div>
			</div>

			<div v-if="address.email_id" class="flex min-w-0 items-center gap-2">
				<Icon
					icon="email-outline"
					:size="12"
					class="shrink-0 text-on-surface-variant dark:text-slate-500"
				/>
				<a
					:href="`mailto:${address.email_id}`"
					class="min-w-0 flex-1 truncate text-xs font-medium text-primary transition-colors hover:underline"
					:title="address.email_id"
				>
					{{ address.email_id }}
				</a>
			</div>

			<div v-if="address.phone" class="flex min-w-0 items-center gap-2">
				<Icon
					icon="phone-outline"
					:size="12"
					class="shrink-0 text-on-surface-variant dark:text-slate-500"
				/>
				<span
					class="min-w-0 flex-1 truncate text-xs text-on-surface-variant dark:text-slate-300"
					:title="address.phone"
					>{{ address.phone }}</span
				>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue"
import Icon from "../Icon.vue"
import { ApiService } from "../../services/api"

const props = defineProps({
	address: {
		type: Object,
		required: true,
	},
	canEdit: {
		type: Boolean,
		default: false,
	},
})

defineEmits(["edit"])

const resolving = ref(false)
const cityName = ref("")
const stateName = ref("")

async function resolveField(doctype, id, field) {
	if (!id) return ""
	try {
		const res = await ApiService.get("frappe.client.get_value", {
			doctype,
			fieldname: field,
			filters: JSON.stringify({ name: id }),
		})
		return (res.message ?? res)?.[field] ?? id
	} catch {
		return id
	}
}

async function resolve() {
	resolving.value = true
	try {
		const [city, state] = await Promise.all([
			resolveField("City", props.address.city, "city"),
			resolveField("State", props.address.state, "state"),
		])
		cityName.value = city
		stateName.value = state
	} finally {
		resolving.value = false
	}
}

const cityLine = computed(() => {
	const city = cityName.value
	const state = stateName.value
	const pin = props.address.pincode
	const left = [city, state].filter(Boolean).join(", ")
	return pin ? `${left} – ${pin}` : left
})

onMounted(resolve)
watch(() => `${props.address.city}|${props.address.state}`, resolve)
</script>
