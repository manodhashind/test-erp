<template>
	<TableManager
		ref="tableManagerRef"
		title="Address & Location"
		:columns="columns"
		:items="addresses"
		:default-form-data="defaultFormData"
		empty-message="No addresses added yet"
		add-button-text="Add Address"
		add-another-button-text="Add Another Address"
		add-title="Add New Address"
		add-subtitle="Enter the location details"
		edit-title="Edit Address"
		edit-subtitle="Update the address details"
		delete-title="Delete Address"
		delete-message="You are about to delete:"
		delete-warning="This action cannot be undone."
		delete-button-text="Delete Address"
		modal-size="lg"
		:on-before-save="handleBeforeSave"
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
				<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
				<circle cx="12" cy="10" r="3" />
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
				<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
				<circle cx="12" cy="10" r="3" />
			</svg>
		</template>

		<!-- Custom cell for Type with badge -->
		<template #cell-type="{ value }">
			<span
				class="inline-flex rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-medium text-primary dark:bg-primary/20 dark:text-primary-light"
			>
				{{ value }}
			</span>
		</template>

		<!-- Form Fields -->
		<template #form="{ formData }">
			<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
				<TextField
					v-model="formData.address_title"
					label="Location Name"
					placeholder="e.g., Main Office, Warehouse 1"
					required
				/>

				<SelectField
					v-model="formData.address_type"
					label="Type"
					placeholder="Select type"
					:options="addressTypeOptions"
					required
				/>

				<TextField
					v-model="formData.address_line1"
					label="Address Line 1"
					placeholder="Street address"
					required
					custom-class="md:col-span-2"
				/>

				<AsyncLookupField
					v-model="formData.city"
					label="City"
					placeholder="Search city..."
					:fetch-function="fetchCities"
					:display-label="formData.cityLabel || ''"
					label-key="label"
					value-key="value"
					meta-key="meta"
					required
					@select="(item) => onCitySelect(item, formData)"
				/>

				<AsyncLookupField
					v-model="formData.state"
					label="State/Province"
					placeholder="Search state..."
					:fetch-function="fetchStates"
					:display-label="formData.stateLabel || ''"
					label-key="label"
					value-key="value"
					meta-key="meta"
					required
				/>

				<AsyncLookupField
					v-model="formData.country"
					label="Country"
					placeholder="Search country..."
					:fetch-function="fetchCountries"
					:display-label="formData.countryLabel || ''"
					label-key="label"
					value-key="value"
					meta-key="meta"
					required
				/>

				<TextField
					v-model="formData.pincode"
					label="Pincode"
					placeholder="Enter pincode"
					type="text"
					required
				/>
			</div>
		</template>

		<!-- Delete Preview -->
		<template #delete-preview="{ item }">
			<p class="mb-1 font-semibold text-slate-900 dark:text-white">
				{{ item.address_title }}
			</p>
			<p class="text-sm text-slate-600 dark:text-slate-400">
				{{ item.address_line1 }}
			</p>
			<p class="text-sm text-slate-600 dark:text-slate-400">
				{{ item.cityLabel || item.city }}, {{ item.stateLabel || item.state }},
				{{ item.countryLabel || item.country }}
			</p>
		</template>
	</TableManager>
</template>

<script setup>
import { ref } from "vue"
import TableManager from "./TableManager.vue"
import { TextField, SelectField, AsyncLookupField } from "../fields"
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

const addresses = ref(props.modelValue || [])

const defaultFormData = {
	address_title: "",
	address_type: "",
	address_line1: "",
	city: "",
	state: "",
	country: "",
	pincode: "",
}

const addressTypeOptions = ref([
	{ label: "Billing", value: "Billing" },
	{ label: "Pickup", value: "Pickup" },
	{ label: "Delivery", value: "Delivery" },
	{ label: "Branch", value: "Branch" },
	{ label: "Office", value: "Office" },
])

const columns = [
	{ key: "address_title", label: "Location Name" },
	{ key: "address_type", label: "Type" },
	{ key: "address_line1", label: "Address" },
	{
		key: "city",
		label: "City",
		formatter: (value, item) => item.cityLabel || value || "-",
	},
	{
		key: "state",
		label: "State",
		formatter: (value, item) => item.stateLabel || value || "-",
	},
	{
		key: "country",
		label: "Country",
		formatter: (value, item) => item.countryLabel || value || "-",
	},
	{ key: "pincode", label: "Pincode" },
]

// Fetch functions for async lookups
const fetchCities = async ({ query, page, pageSize }) => {
	try {
		const response = await ApiService.get("tms.api.meta.lookup.city_options", {
			query: query || "",
			limit_start: (page - 1) * pageSize,
			limit_page_length: pageSize,
		})

		const data = response.message || []

		return {
			items: data,
			total: data.length,
			page,
			pageSize,
			hasMore: data.length === pageSize,
		}
	} catch (error) {
		console.error("Error fetching cities:", error)
		return { items: [], total: 0, page, pageSize, hasMore: false }
	}
}

const onCitySelect = (item, formData) => {
	if (item?.state_id) {
		formData.state = item.state_id
		formData.stateLabel = item.state_label || ""
	}
	if (item?.country_id) {
		formData.country = item.country_id
		formData.countryLabel = item.country_id
	}
}

const fetchStates = async ({ query, page, pageSize }) => {
	try {
		const response = await ApiService.get("tms.api.meta.lookup.state_options", {
			query: query || "",
			limit_start: (page - 1) * pageSize,
			limit_page_length: pageSize,
		})

		const data = response.message || []

		return {
			items: data,
			total: data.length,
			page,
			pageSize,
			hasMore: data.length === pageSize,
		}
	} catch (error) {
		console.error("Error fetching states:", error)
		return { items: [], total: 0, page, pageSize, hasMore: false }
	}
}

const fetchCountries = async ({ query, page, pageSize }) => {
	try {
		const response = await ApiService.get("tms.api.meta.lookup.country_options", {
			query: query || "",
			limit_start: (page - 1) * pageSize,
			limit_page_length: pageSize,
		})

		const data = response.message || []

		return {
			items: data,
			total: data.length,
			page,
			pageSize,
			hasMore: data.length === pageSize,
		}
	} catch (error) {
		console.error("Error fetching countries:", error)
		return { items: [], total: 0, page, pageSize, hasMore: false }
	}
}

// Helper to get label from value
const getLabelFromValue = async (fieldType, value) => {
	if (!value) return ""

	try {
		let response
		if (fieldType === "city") {
			response = await ApiService.get("tms.api.meta.lookup.city_options", {
				query: "",
				limit_start: 0,
				limit_page_length: 1000,
			})
			const item = response.message?.find((c) => c.value === value)
			return item?.label || value
		} else if (fieldType === "state") {
			response = await ApiService.get("tms.api.meta.lookup.state_options", {
				query: "",
				limit_start: 0,
				limit_page_length: 1000,
			})
			const item = response.message?.find((s) => s.value === value)
			return item?.label || value
		} else if (fieldType === "country") {
			response = await ApiService.get("tms.api.meta.lookup.country_options", {
				query: "",
				limit_start: 0,
				limit_page_length: 1000,
			})
			const item = response.message?.find((c) => c.value === value)
			return item?.label || value
		}
	} catch (error) {
		console.error(`Error fetching label for ${fieldType}:`, error)
		return value
	}
	return value
}

// Lifecycle hooks
const handleBeforeSave = async (formData) => {
	// Fetch and store labels for display
	const addressData = {
		...formData,
		cityLabel: await getLabelFromValue("city", formData.city),
		stateLabel: await getLabelFromValue("state", formData.state),
		countryLabel: await getLabelFromValue("country", formData.country),
	}

	return addressData
}

const handleAdd = (data) => {
	addresses.value.push(data)
	emit("update:modelValue", addresses.value)
	toast.success("Address added successfully")
}

const handleUpdate = (index, data) => {
	addresses.value[index] = data
	emit("update:modelValue", addresses.value)
	toast.success("Address updated successfully")
}

const handleDelete = (index) => {
	addresses.value.splice(index, 1)
	emit("update:modelValue", addresses.value)
	toast.success("Address deleted successfully")
}

// Watch for external changes
watch(
	() => props.modelValue,
	(newValue) => {
		addresses.value = newValue || []
	},
	{ deep: true },
)

defineExpose({
	addresses,
	tableManagerRef,
})
</script>

<script>
import { watch } from "vue"

export default {
	name: "AddressManager",
}
</script>
