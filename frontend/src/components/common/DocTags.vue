<template>
	<div
		class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-700 dark:bg-slate-800"
	>
		<div class="mb-3 flex items-center gap-2 text-primary dark:text-on-primary-container">
			<Icon icon="tag-multiple-outline" :background="true" :size="18" />
			<h3 class="m-0 text-sm font-bold">Tags</h3>
		</div>

		<!-- Current tags -->
		<div class="mb-3 flex flex-wrap gap-1.5">
			<span v-for="tag in tags" :key="tag" class="selected-tag">
				{{ tag }}
				<button type="button" class="tag-remove" :disabled="loading" @click="removeTag(tag)">
					<svg class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
						<path
							fill-rule="evenodd"
							d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
							clip-rule="evenodd"
						/>
					</svg>
				</button>
			</span>
			<span v-if="tags.length === 0" class="text-xs text-slate-400 dark:text-slate-500"
				>No tags yet</span
			>
		</div>

		<!-- Add tag input -->
		<div class="relative">
			<div class="flex gap-2">
				<input
					ref="inputRef"
					v-model="newTag"
					type="text"
					class="min-w-0 flex-1 rounded-lg border border-slate-200 px-3 py-1.5 text-sm focus:border-primary focus:outline-none dark:border-slate-600 dark:bg-slate-700 dark:text-white dark:placeholder-slate-400"
					placeholder="Add a tag…"
					:disabled="loading"
					@keydown="
						(e) => {
							if (e.key === 'Enter' || e.key === ',') {
								e.preventDefault()
								submitNewTag()
							}
						}
					"
					@input="onInput"
					@focus="onFocus"
					@blur="hideSuggestions"
				/>
				<button
					type="button"
					class="rounded-lg bg-primary px-3 py-1.5 text-xs font-semibold text-on-primary hover:bg-primary-600 disabled:opacity-50"
					:disabled="loading || !newTag.trim()"
					@click="submitNewTag"
				>
					Add
				</button>
			</div>

			<!-- Suggestions dropdown -->
			<div
				v-if="showSuggestions && suggestions.length > 0"
				class="absolute left-0 right-0 top-full z-20 mt-1 max-h-40 overflow-y-auto rounded-lg border border-slate-200 bg-white shadow-md dark:border-slate-600 dark:bg-slate-800"
			>
				<button
					v-for="s in suggestions"
					:key="s"
					type="button"
					class="block w-full px-3 py-1.5 text-left text-sm text-slate-700 hover:bg-slate-50 dark:text-slate-300 dark:hover:bg-slate-700"
					@mousedown.prevent="addTag(s)"
				>
					{{ s }}
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue"
import { ApiService } from "../../services/api"
import Icon from "../Icon.vue"

const TAG_API = "frappe.desk.doctype.tag.tag"

const props = defineProps({
	doctype: { type: String, required: true },
	docname: { type: String, required: true },
})

const emit = defineEmits(["change"])

const tags = ref([])
const newTag = ref("")
const suggestions = ref([])
const showSuggestions = ref(false)
const loading = ref(false)
const inputRef = ref(null)
let debounceTimer = null

const fetchTags = async () => {
	if (!props.docname) return
	try {
		const res = await ApiService.get("frappe.client.get_list", {
			doctype: "Tag Link",
			filters: JSON.stringify([
				["document_type", "=", props.doctype],
				["document_name", "=", props.docname],
			]),
			fields: JSON.stringify(["tag"]),
			limit: 100,
		})
		const list = res?.message ?? res ?? []
		tags.value = Array.isArray(list) ? list.map((r) => r.tag).filter(Boolean) : []
	} catch (e) {
		console.error("[DocTags] fetch failed:", e)
	}
}

// Bypass global axios error interceptor for non-critical calls
const silentGet = async (method, params) => {
	try {
		const qs = new URLSearchParams(params).toString()
		const res = await fetch(`/api/method/${method}?${qs}`, { credentials: "include" })
		if (!res.ok) return null
		return await res.json()
	} catch {
		return null
	}
}

const fetchSuggestions = async (txt) => {
	const res = await silentGet(`${TAG_API}.get_tags`, {
		doctype: props.doctype,
		txt: txt ?? "",
	})
	const list = res?.message ?? []
	suggestions.value = Array.isArray(list) ? list.filter((s) => !tags.value.includes(s)) : []
}

const onInput = () => {
	showSuggestions.value = true
	clearTimeout(debounceTimer)
	debounceTimer = setTimeout(() => fetchSuggestions(newTag.value), 250)
}

const onFocus = () => {
	showSuggestions.value = true
	fetchSuggestions(newTag.value)
}

const hideSuggestions = () => {
	setTimeout(() => {
		showSuggestions.value = false
	}, 150)
}

const addTag = async (tag) => {
	const t = tag.trim()
	if (!t || tags.value.includes(t)) {
		newTag.value = ""
		showSuggestions.value = false
		return
	}
	loading.value = true
	try {
		await ApiService.post(`${TAG_API}.add_tag`, {
			tag: t,
			dt: props.doctype,
			dn: props.docname,
		})
		tags.value = [...tags.value, t]
		emit("change", tags.value)
	} catch (e) {
		console.error("[DocTags] add failed:", e)
	} finally {
		loading.value = false
		newTag.value = ""
		showSuggestions.value = false
	}
}

const removeTag = async (tag) => {
	loading.value = true
	try {
		await ApiService.post(`${TAG_API}.remove_tag`, {
			tag,
			dt: props.doctype,
			dn: props.docname,
		})
		tags.value = tags.value.filter((t) => t !== tag)
		emit("change", tags.value)
	} catch (e) {
		console.error("[DocTags] remove failed:", e)
	} finally {
		loading.value = false
	}
}

const submitNewTag = () => {
	if (newTag.value.trim()) addTag(newTag.value)
}

watch(() => props.docname, fetchTags, { immediate: false })

onMounted(fetchTags)
</script>
