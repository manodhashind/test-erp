<template>
	<TableManager
		ref="tableManagerRef"
		title="Contacts"
		:columns="columns"
		:items="contacts"
		:default-form-data="defaultFormData"
		empty-message="No contacts added yet"
		add-button-text="Add Contact"
		add-another-button-text="Add Another Contact"
		add-title="Add New Contact"
		add-subtitle="Enter the contact details"
		edit-title="Edit Contact"
		edit-subtitle="Update the contact details"
		delete-title="Delete Contact"
		delete-message="You are about to delete:"
		delete-warning="This action cannot be undone."
		delete-button-text="Delete Contact"
		modal-size="lg"
		@add="handleAdd"
		@update="handleUpdate"
		@delete="handleDelete"
	>
		<!-- Icon -->
		<template #icon>
			<svg
				width="18"
				height="18"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
			>
				<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
				<circle cx="9" cy="7" r="4" />
				<path d="M23 21v-2a4 4 0 0 0-3-3.87" />
				<path d="M16 3.13a4 4 0 0 1 0 7.75" />
			</svg>
		</template>

		<!-- Empty Icon -->
		<template #empty-icon>
			<svg
				width="28"
				height="28"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				class="text-slate-400 dark:text-slate-500"
			>
				<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
				<circle cx="9" cy="7" r="4" />
				<path d="M23 21v-2a4 4 0 0 0-3-3.87" />
				<path d="M16 3.13a4 4 0 0 1 0 7.75" />
			</svg>
		</template>

		<!-- Custom cell for phone numbers -->
		<template #cell-phone_numbers="{ value }">
			<div class="flex flex-wrap gap-1.5">
				<span
					v-for="(phone, index) in value"
					:key="index"
					class="dark:bg-primary/15 inline-flex items-center gap-1 rounded-full bg-primary/10 px-2.5 py-1 text-xs font-medium text-primary dark:text-primary-light"
				>
					<svg
						width="12"
						height="12"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						class="flex-shrink-0"
					>
						<path
							d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"
						/>
					</svg>
					<PhoneDisplay :phone="phone" />
				</span>
			</div>
		</template>

		<!-- Custom cell for emails -->
		<template #cell-emails="{ value }">
			<div class="flex flex-wrap gap-1.5">
				<span
					v-for="(email, index) in value"
					:key="index"
					class="inline-flex items-center gap-1 rounded-full bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700 dark:bg-green-900/20 dark:text-green-400"
				>
					<svg
						width="12"
						height="12"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						class="flex-shrink-0"
					>
						<path
							d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
						/>
						<polyline points="22,6 12,13 2,6" />
					</svg>
					{{ email }}
				</span>
			</div>
		</template>

		<!-- Form Fields -->
		<template #form="{ formData }">
			<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
				<TextField
					v-model="formData.first_name"
					label="First Name"
					placeholder="Enter first name"
					required
				/>

				<TextField
					v-model="formData.last_name"
					label="Last Name"
					placeholder="Enter last name"
					required
				/>

				<AsyncLookupField
					v-model="formData.designation"
					label="Designation"
					placeholder="Search designation..."
					:fetch-function="fetchDesignations"
					:display-label="formData.designationLabel || ''"
					label-key="label"
					value-key="value"
					custom-class="md:col-span-2"
				/>

				<MultiPhoneField
					v-model="formData.phone_numbers"
					label="Phone Numbers"
					placeholder="Enter phone number"
					required
					custom-class="md:col-span-2"
				/>

				<MultiEmailField
					v-model="formData.emails"
					label="Email Addresses"
					placeholder="Enter email address"
					required
					custom-class="md:col-span-2"
				/>
			</div>
		</template>

		<!-- Delete Preview -->
		<template #delete-preview="{ item }">
			<div class="space-y-2">
				<p class="font-semibold text-slate-900 dark:text-white">
					{{ item.first_name }} {{ item.last_name }}
				</p>
				<p
					v-if="item.designationLabel || item.designation"
					class="text-sm text-slate-600 dark:text-slate-400"
				>
					{{ item.designationLabel || item.designation }}
				</p>
				<div class="text-sm text-slate-600 dark:text-slate-400">
					<p v-for="(phone, index) in item.phone_numbers" :key="`phone-${index}`">
						📞 {{ phone }}
					</p>
					<p v-for="(email, index) in item.emails" :key="`email-${index}`">✉️ {{ email }}</p>
				</div>
			</div>
		</template>
	</TableManager>
</template>

<script setup>
import { ref, watch } from "vue"
import TableManager from "./TableManager.vue"
import PhoneDisplay from "../display_fields/PhoneDisplay.vue"
import { TextField, AsyncLookupField } from "../fields"
import MultiPhoneField from "../fields/advanced/MultiPhoneField.vue"
import MultiEmailField from "../fields/advanced/MultiEmailField.vue"
import { ApiService } from "../../services/api"
import { useToast } from "../../services/toastService"

const props = defineProps({
	modelValue: {
		type: Array,
		default: () => [],
	},
})

const emit = defineEmits(["update:modelValue"])

const toast = useToast()
const tableManagerRef = ref(null)

const contacts = ref(props.modelValue || [])

const defaultFormData = {
	first_name: "",
	last_name: "",
	designation: "",
	phone_numbers: [""],
	emails: [""],
}

const columns = [
	{
		key: "first_name",
		label: "First Name",
		formatter: (value, item) => value || "-",
	},
	{
		key: "last_name",
		label: "Last Name",
		formatter: (value, item) => value || "-",
	},
	{
		key: "designation",
		label: "Designation",
		formatter: (value, item) => item.designationLabel || value || "-",
	},
	{ key: "phone_numbers", label: "Phone Numbers" },
	{ key: "emails", label: "Email Addresses" },
]

// Fetch designations
const fetchDesignations = async ({ query, page, pageSize }) => {
	try {
		const filters = query ? [["name", "like", `%${query}%`]] : []
		const response = await ApiService.get("frappe.client.get_list", {
			doctype: "Designation",
			fields: JSON.stringify(["name"]),
			filters: JSON.stringify(filters),
			limit_start: (page - 1) * pageSize,
			limit_page_length: pageSize,
		})

		const data = response.message || []

		return {
			items: data.map((d) => ({ label: d.name, value: d.name })),
			total: data.length,
			page,
			pageSize,
			hasMore: data.length === pageSize,
		}
	} catch (error) {
		console.error("Error fetching designations:", error)
		return { items: [], total: 0, page, pageSize, hasMore: false }
	}
}

// Helper to get designation label
const getDesignationLabel = async (value) => {
	if (!value) return ""

	try {
		const response = await ApiService.get("frappe.client.get_list", {
			doctype: "Designation",
			fields: JSON.stringify(["name"]),
			filters: JSON.stringify([["name", "=", value]]),
			limit_start: 0,
			limit_page_length: 1,
		})

		return response.message?.[0]?.name || value
	} catch (error) {
		console.error("Error fetching designation label:", error)
		return value
	}
}

const handleAdd = async (data) => {
	// Fetch designation label
	const contactData = {
		...data,
		designationLabel: await getDesignationLabel(data.designation),
	}

	contacts.value.push(contactData)
	emit("update:modelValue", contacts.value)
	toast.success("Contact added successfully")
}

const handleUpdate = async (index, data) => {
	// Fetch designation label
	const contactData = {
		...data,
		designationLabel: await getDesignationLabel(data.designation),
	}

	contacts.value[index] = contactData
	emit("update:modelValue", contacts.value)
	toast.success("Contact updated successfully")
}

const handleDelete = (index) => {
	contacts.value.splice(index, 1)
	emit("update:modelValue", contacts.value)
	toast.success("Contact deleted successfully")
}

// Watch for external changes
watch(
	() => props.modelValue,
	(newValue) => {
		contacts.value = newValue || []
	},
	{ deep: true },
)

defineExpose({
	contacts,
	tableManagerRef,
})
</script>

<script>
export default {
	name: "ContactManager",
}
</script>
