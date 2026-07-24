<template>
	<div
		class="rounded-xl border border-outline-variant bg-surface-container p-4 dark:border-slate-700 dark:bg-slate-800/60"
	>
		<!-- Header row: avatar + name + edit -->
		<div class="flex items-start justify-between gap-2">
			<div class="flex min-w-0 flex-1 items-start gap-3">
				<!-- Initials avatar -->
				<div
					class="flex h-9 w-9 shrink-0 items-center justify-center rounded-[10px] bg-primary/10 text-sm font-extrabold text-primary dark:bg-primary/20"
				>
					{{ initials }}
				</div>
				<!-- Name + designation + primary badge -->
				<div class="min-w-0 flex-1">
					<div class="flex min-w-0 flex-wrap items-center gap-1.5">
						<p class="truncate text-sm font-bold text-on-surface dark:text-slate-100">
							{{ fullName }}
						</p>
						<span
							v-if="contact.is_primary_contact === 1 || contact.is_primary_contact === true"
							class="shrink-0 rounded-full bg-primary/10 px-1.5 py-0.5 text-[10px] font-bold text-primary dark:bg-primary/20"
						>
							Primary
						</span>
					</div>
					<p
						v-if="contact.designation"
						class="text-xs text-on-surface-variant dark:text-slate-400"
					>
						{{ contact.designation }}
					</p>
				</div>
			</div>

			<!-- Edit button -->
			<button
				v-if="canEdit"
				class="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg text-on-surface-variant transition-colors hover:bg-surface-container hover:text-on-surface dark:text-slate-500 dark:hover:bg-slate-700 dark:hover:text-slate-300"
				title="Edit contact"
				@click="$emit('edit', contact)"
			>
				<Icon icon="pencil" :size="14" />
			</button>
		</div>

		<!-- Contact info rows -->
		<div class="mt-3 space-y-2 border-t border-outline-variant pt-3 dark:border-slate-700">
			<div v-if="email" class="flex min-w-0 items-center gap-2.5">
				<div
					class="flex h-5 w-5 shrink-0 items-center justify-center rounded-md bg-primary/10 dark:bg-primary/20"
				>
					<Icon icon="email-outline" :size="11" class="text-primary" />
				</div>
				<a
					:href="`mailto:${email}`"
					class="min-w-0 flex-1 truncate text-xs font-medium text-primary transition-colors hover:underline dark:text-primary"
					:title="email"
					>{{ email }}</a
				>
			</div>

			<template v-if="phoneList.length">
				<div
					v-for="(p, i) in phoneList"
					:key="'ph-' + i"
					class="flex min-w-0 items-center gap-2.5"
				>
					<div
						class="flex h-5 w-5 shrink-0 items-center justify-center rounded-md bg-primary/10 dark:bg-primary/20"
					>
						<Icon icon="phone-outline" :size="11" class="text-primary" />
					</div>
					<span
						class="min-w-0 flex-1 truncate text-xs text-slate-600 dark:text-slate-300"
						:title="p.phone"
					>
						{{ p.phone }}
						<span v-if="p.type" class="text-[10px] text-slate-400">({{ p.type }})</span>
					</span>
				</div>
			</template>

			<div v-if="contact.department" class="flex min-w-0 items-center gap-2.5">
				<div
					class="flex h-5 w-5 shrink-0 items-center justify-center rounded-md bg-slate-100 dark:bg-slate-700"
				>
					<Icon icon="domain" :size="11" class="text-slate-500 dark:text-slate-400" />
				</div>
				<span
					class="min-w-0 flex-1 truncate text-xs text-slate-500 dark:text-slate-400"
					:title="contact.department"
					>{{ contact.department }}</span
				>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from "vue"
import Icon from "../Icon.vue"

const props = defineProps({
	contact: {
		type: Object,
		required: true,
	},
	canEdit: {
		type: Boolean,
		default: false,
	},
})

defineEmits(["edit"])

const fullName = computed(() =>
	[props.contact.first_name, props.contact.middle_name, props.contact.last_name]
		.filter(Boolean)
		.join(" "),
)

const initials = computed(() => {
	const f = props.contact.first_name?.[0] ?? ""
	const l = props.contact.last_name?.[0] ?? ""
	return (f + l).toUpperCase() || "?"
})

const email = computed(() => {
	if (props.contact.email_ids?.length) return props.contact.email_ids[0].email_id
	return props.contact.email_id || ""
})

const phoneList = computed(() => {
	const list = []
	if (props.contact.phone_nos?.length) {
		props.contact.phone_nos.forEach((p) => {
			if (p.phone)
				list.push({
					phone: p.phone,
					type:
						p.contact_type ||
						(p.is_primary_mobile_no ? "Mobile" : p.is_primary_phone ? "Office" : "Phone"),
				})
		})
	} else if (props.contact.phone_numbers?.length) {
		props.contact.phone_numbers.forEach((p) => {
			if (p.phone)
				list.push({
					phone: p.phone,
					type:
						p.contact_type ||
						(p.is_primary_mobile_no ? "Mobile" : p.is_primary_phone ? "Office" : "Phone"),
				})
		})
	} else if (props.contact.phone) {
		list.push({ phone: props.contact.phone, type: "Phone" })
	}
	return list
})
</script>
