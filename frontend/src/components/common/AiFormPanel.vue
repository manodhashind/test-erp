<template>
	<div class="w-full">
		<div
			class="rounded-2xl bg-white p-4 shadow-xl shadow-black/10 ring-1 ring-black/[0.06] dark:bg-slate-800 dark:shadow-black/40 dark:ring-white/[0.06]"
		>
			<!-- Header -->
			<div class="mb-3 flex items-center gap-2">
				<AiIconBadge size="xs" rounded="rounded-lg" />
				<h3 class="flex-1 text-sm font-bold tracking-tight text-on-surface dark:text-slate-100">
					AI Agent
				</h3>
				<button
					v-if="activeTab === 'voice'"
					type="button"
					title="Reset conversation"
					@click="resetVoiceAgent"
				>
					<Icon icon="refresh" :size="14" />
				</button>
			</div>

			<!-- Tab switcher -->
			<div class="mb-4 flex gap-1 rounded-lg bg-black/5 p-1 dark:bg-black/30">
				<button
					class="flex flex-1 items-center justify-center gap-1.5 rounded-md py-1.5 text-xs font-semibold transition-all duration-200"
					:class="
						activeTab === 'voice'
							? 'bg-surface text-primary shadow-sm ring-1 ring-primary/20 dark:bg-slate-700 dark:text-primary dark:ring-primary/30'
							: 'text-on-surface-variant hover:text-on-surface dark:hover:text-slate-300'
					"
					@click="activeTab = 'voice'"
				>
					<Icon icon="microphone-outline" :size="13" />
					Form Agent
				</button>
				<button
					class="flex flex-1 items-center justify-center gap-1.5 rounded-md py-1.5 text-xs font-semibold transition-all duration-200"
					:class="
						activeTab === 'scanner'
							? 'bg-surface text-primary shadow-sm ring-1 ring-primary/20 dark:bg-slate-700 dark:text-primary dark:ring-primary/30'
							: 'text-on-surface-variant hover:text-on-surface dark:hover:text-slate-300'
					"
					@click="activeTab = 'scanner'"
				>
					<Icon icon="scan-helper" :size="13" />
					Scanner
				</button>
			</div>

			<!-- ░░ Document Scanner Tab ░░ -->
			<div v-if="activeTab === 'scanner'">
				<!-- Drop Zone -->
				<div
					class="relative cursor-pointer rounded-lg border-2 border-dashed transition-all duration-200"
					:class="
						isDragging
							? 'border-primary bg-primary/5 dark:bg-primary/10'
							: scanFile || scanText
								? 'border-outline-variant bg-surface dark:border-slate-600 dark:bg-slate-700/30'
								: 'border-outline-variant bg-surface hover:border-primary/50 hover:bg-primary/5 dark:border-slate-600 dark:bg-slate-700/30'
					"
					@click="fileInputRef.click()"
					@dragover.prevent="isDragging = true"
					@dragleave.self="isDragging = false"
					@drop.prevent="handleFileDrop"
				>
					<input
						ref="fileInputRef"
						type="file"
						accept="image/jpeg,image/png,image/webp,image/gif,application/pdf"
						class="hidden"
						@change="handleFileChange"
					/>

					<!-- Empty state -->
					<div
						v-if="!scanFile && !scanText"
						class="flex flex-col items-center gap-2 py-7 text-center"
					>
						<div
							class="flex h-10 w-10 items-center justify-center rounded-full transition-colors"
							:class="isDragging ? 'bg-primary/10' : 'bg-surface-container dark:bg-slate-700'"
						>
							<Icon
								icon="upload"
								:size="20"
								:class="isDragging ? 'text-primary' : 'text-on-surface-variant'"
							/>
						</div>
						<div>
							<p class="text-xs font-medium text-on-surface dark:text-slate-300">
								{{ isDragging ? "Drop to upload" : "Drop or click to upload" }}
							</p>
							<p class="mt-0.5 text-xs text-on-surface-variant">
								JPG, PNG, WebP, PDF (Max 5 pages)
							</p>
						</div>
					</div>

					<!-- Document or Text preview -->
					<div v-else class="p-3">
						<!-- Text preview -->
						<div
							v-if="scanText"
							class="max-h-32 overflow-y-auto rounded-md bg-surface-container p-3 text-xs text-on-surface dark:bg-slate-700/50 dark:text-slate-300"
						>
							<p class="whitespace-pre-wrap">{{ scanText }}</p>
						</div>
						<img
							v-else-if="scanPreview"
							:src="scanPreview"
							alt="Document preview"
							class="mx-auto max-h-32 rounded-md object-contain"
						/>
						<div
							v-else
							class="flex items-center gap-2 rounded-md bg-surface-container px-3 py-2.5 dark:bg-slate-700"
						>
							<div class="relative shrink-0">
								<Icon icon="file-document" :size="20" class="text-on-surface-variant" />
								<span
									v-if="scanFile && scanFile.type === 'application/pdf'"
									class="absolute -bottom-1 -right-1 rounded bg-red-500 px-0.5 text-[8px] font-bold leading-tight text-white"
									>PDF</span
								>
							</div>
							<span class="truncate text-xs text-on-surface dark:text-slate-300">{{
								scanFile?.name
							}}</span>
						</div>
					</div>
				</div>

				<!-- Actions -->
				<div v-if="scanFile || scanText" class="mt-2 flex gap-2">
					<AiButton
						:label="scanLoading ? 'Scanning…' : 'Extract & Fill'"
						icon="chart-timeline-variant-shimmer"
						:loading="scanLoading"
						loading-label="Scanning…"
						class="flex-1"
						@click="scanText ? extractFromText(scanText) : extractFromDocument()"
					/>
					<ClearButton size="sm" @click="clearScan" />
				</div>
				<p
					v-if="scanFile && scanFile.type === 'application/pdf'"
					class="mt-1.5 text-center text-[10px] text-on-surface-variant"
				>
					Note: Only the first 5 pages of the PDF will be scanned.
				</p>

				<!-- Error -->
				<div
					v-if="scanError"
					class="mt-3 flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-600 dark:border-red-800 dark:bg-red-900/20 dark:text-red-400"
				>
					<Icon icon="alert-circle" :size="13" class="mt-0.5 shrink-0" />
					{{ scanError }}
				</div>

				<!-- Warnings -->
				<div
					v-if="scanWarnings && scanWarnings.length"
					class="mt-3 rounded-lg border border-yellow-200 bg-yellow-50 p-3 dark:border-yellow-800 dark:bg-yellow-900/20"
				>
					<p
						class="mb-2 flex items-center gap-1.5 text-xs font-semibold text-yellow-700 dark:text-yellow-400"
					>
						<Icon icon="alert" :size="13" />
						Records not found in system
					</p>
					<p class="mb-2 text-xs text-yellow-700 dark:text-yellow-400">
						We found the following details in your document, but they don't exist in the system
						yet. Please create them first to successfully fill these fields:
					</p>
					<ul class="list-inside list-disc space-y-1 text-xs text-yellow-700 dark:text-yellow-400">
						<li v-for="(warn, i) in scanWarnings" :key="i">
							<span class="font-bold">{{ warn.split(":")[0] }}:</span>{{ warn.split(":")[1] }}
						</li>
					</ul>
				</div>

				<!-- Missing Mandatory Fields -->
				<div
					v-if="scanMissingMandatory && scanMissingMandatory.length"
					class="mt-3 rounded-lg border border-blue-200 bg-blue-50 p-3 dark:border-blue-800 dark:bg-blue-900/20"
				>
					<p
						class="mb-2 flex items-center gap-1.5 text-xs font-semibold text-blue-700 dark:text-blue-400"
					>
						<Icon icon="alert-circle-outline" :size="13" />
						Missing Mandatory Fields
					</p>
					<p class="mb-2 text-xs text-blue-700 dark:text-blue-400">
						These mandatory fields were not found in the document. Please fill them manually or use
						the Form Agent to provide them:
					</p>
					<div class="flex flex-wrap gap-1">
						<span
							v-for="f in scanMissingMandatory"
							:key="f.fieldname"
							class="rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-700 dark:bg-blue-800/50 dark:text-blue-300"
						>
							{{ f.label }}
						</span>
					</div>
				</div>

				<!-- Success -->
				<div
					v-if="scanAppliedFields.length || scanAppliedChildSummary.length"
					class="mt-3 rounded-lg border border-green-200 bg-green-50 p-3 dark:border-green-800 dark:bg-green-900/20"
				>
					<p
						class="mb-2 flex items-center gap-1.5 text-xs font-semibold text-green-700 dark:text-green-400"
					>
						<Icon icon="check" :size="13" />
						{{ scanAppliedFields.length }} fields filled
						<template v-if="scanAppliedChildSummary.length"
							>· {{ scanAppliedChildSummary.join(", ") }}</template
						>
					</p>
					<div class="flex flex-wrap gap-1">
						<span
							v-for="f in scanAppliedFields"
							:key="f"
							class="rounded-full bg-green-100 px-2 py-0.5 text-xs text-green-700 dark:bg-green-800/50 dark:text-green-300"
						>
							{{ fieldLabels[f] || f }}
						</span>
					</div>
				</div>
			</div>

			<!-- ░░ Voice Agent Tab — Conversational ░░ -->
			<div v-else class="flex flex-col" style="height: 520px">
				<!-- ── Chat messages ── -->
				<div
					ref="chatScrollRef"
					class="flex-1 space-y-2.5 overflow-y-auto rounded-xl border border-outline-variant bg-white px-3 py-3 dark:border-slate-700 dark:bg-black"
					style="min-height: 0"
				>
					<!-- Empty / loading state -->
					<div
						v-if="!voiceChatMessages.length"
						class="flex h-full flex-col items-center justify-center gap-3 py-6"
					>
						<div
							class="dark:bg-primary/15 relative flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 ring-1 ring-primary/20 dark:ring-primary/25"
						>
							<span
								class="bg-primary/15 absolute inset-0 animate-ping rounded-full"
								style="animation-duration: 2.5s"
							/>
							<Icon icon="microphone-outline" :size="20" class="relative text-primary" />
						</div>
						<p class="text-center text-[11.5px] text-on-surface-variant dark:text-slate-400">
							Tap the microphone to start a<br />voice conversation
						</p>
					</div>

					<!-- Message bubbles -->
					<template v-for="(msg, i) in voiceChatMessages" :key="i">
						<!-- AI message (left) -->
						<div v-if="msg.role === 'ai'" class="flex items-end gap-2">
							<div
								class="dark:bg-primary/15 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 ring-1 ring-primary/20 dark:ring-primary/25"
							>
								<Icon icon="creation" :size="11" class="text-primary" />
							</div>
							<div
								class="max-w-[86%] rounded-2xl rounded-bl-sm bg-white px-3 py-2 shadow-sm ring-1 ring-primary/10 dark:bg-slate-700 dark:ring-primary/20"
							>
								<div
									class="ai-md space-y-1 text-[12px] leading-relaxed text-on-surface dark:text-slate-100"
									v-html="_renderMarkdown(msg.text)"
								/>
							</div>
						</div>

						<!-- User message (right) -->
						<div v-else class="flex items-end justify-end gap-2">
							<div class="max-w-[82%] rounded-2xl rounded-br-sm bg-primary px-3 py-2">
								<p class="text-[12px] leading-relaxed text-white">{{ msg.text }}</p>
							</div>
						</div>
					</template>

					<!-- AI thinking bubble -->
					<div v-if="voiceState === 'thinking'" class="flex items-end gap-2">
						<div
							class="dark:bg-primary/15 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 ring-1 ring-primary/20 dark:ring-primary/25"
						>
							<Icon icon="creation" :size="11" class="text-primary" />
						</div>
						<div
							class="rounded-2xl rounded-bl-sm bg-white px-3.5 py-2.5 shadow-sm ring-1 ring-primary/10 dark:bg-slate-700 dark:ring-primary/20"
						>
							<span class="flex items-center gap-1">
								<span
									v-for="j in 3"
									:key="j"
									class="inline-block h-1.5 w-1.5 animate-bounce rounded-full bg-primary/40 dark:bg-primary/50"
									:style="{ animationDelay: (j - 1) * 140 + 'ms' }"
								/>
							</span>
						</div>
					</div>

					<!-- Live transcript bubble (user is speaking) -->
					<div
						v-if="voiceState === 'listening' && voiceTranscript"
						class="flex items-end justify-end gap-2 opacity-70"
					>
						<div class="max-w-[82%] rounded-2xl rounded-br-sm bg-primary/60 px-3 py-2">
							<p class="text-[12px] leading-relaxed text-white">
								{{ voiceTranscript
								}}<span
									class="ml-0.5 inline-block h-3 w-0.5 animate-pulse rounded-sm bg-white align-baseline"
								/>
							</p>
						</div>
					</div>
				</div>

				<!-- ── Waveform ── -->
				<div
					v-show="voiceState === 'listening'"
					class="relative mt-2 overflow-hidden rounded-xl border border-red-200/50 bg-red-50/40 dark:border-red-700/20 dark:bg-red-900/10"
					style="height: 44px"
				>
					<canvas ref="waveCanvasRef" class="absolute inset-0 h-full w-full" />
				</div>

				<!-- ── Status line (error) ── -->
				<div
					v-if="voiceAgentError"
					class="mt-2 flex items-center gap-1.5 rounded-lg border border-amber-200 bg-amber-50 px-2.5 py-1.5 text-[11px] text-amber-700 dark:border-amber-700/40 dark:bg-amber-900/20 dark:text-amber-400"
				>
					<Icon icon="alert" :size="11" class="shrink-0" />
					{{ voiceAgentError }}
				</div>

				<!-- ── Voice-mode status + End button ── -->
				<div v-else-if="voiceMode" class="mt-2 flex items-center justify-between gap-2 px-1">
					<span class="flex items-center gap-1.5 text-[11px] font-semibold">
						<template v-if="voiceState === 'listening'">
							<span class="h-2 w-2 animate-pulse rounded-full bg-red-500" />
							<span class="text-red-500 dark:text-red-400"
								>Listening… {{ voiceDurationLabel }}</span
							>
						</template>
						<template v-else-if="voiceState === 'thinking'">
							<Icon icon="loading" :size="12" class="animate-spin text-on-surface-variant" />
							<span class="text-on-surface-variant dark:text-slate-400">Thinking…</span>
						</template>
						<template v-else-if="voiceState === 'speaking'">
							<Icon icon="volume-high" :size="12" class="text-primary" />
							<span class="text-primary">Speaking…</span>
						</template>
						<template v-else>
							<Icon icon="microphone" :size="12" class="text-primary" />
							<span class="text-on-surface-variant dark:text-slate-400">Voice mode on</span>
						</template>
					</span>
					<button
						type="button"
						class="flex items-center gap-1 rounded-full border border-outline-variant px-2.5 py-1 text-[11px] font-semibold text-on-surface-variant transition-colors hover:border-red-200 hover:bg-red-50 hover:text-red-500 dark:border-slate-600 dark:hover:bg-red-900/20"
						@click="endVoiceConversation"
					>
						<Icon icon="close" :size="11" /> End
					</button>
				</div>

				<!-- ── Thinking (typed mode) ── -->
				<div
					v-else-if="voiceState === 'thinking'"
					class="mt-2 flex items-center gap-1.5 px-1 text-[11px] font-medium text-on-surface-variant dark:text-slate-400"
				>
					<Icon icon="loading" :size="12" class="animate-spin" /> Thinking…
				</div>

				<!-- ── Composer ── -->
				<div
					class="mt-2 flex items-end gap-1 rounded-2xl border border-outline-variant bg-surface py-1 pl-3 pr-1 transition-colors focus-within:border-primary focus-within:ring-2 focus-within:ring-primary/20 dark:border-slate-600 dark:bg-slate-700/50"
				>
					<textarea
						v-model="voiceTextInput"
						:disabled="voiceState === 'thinking'"
						placeholder="Type a message, or tap the mic…"
						rows="1"
						class="flex-1 resize-none overflow-hidden border-none bg-transparent p-0 py-2 text-[12px] text-on-surface placeholder-slate-400 focus:outline-none focus:ring-0 dark:text-slate-200 dark:placeholder-slate-500"
						@keydown.enter.exact.prevent="_sendTypedMessage"
					/>

					<!-- Mic button -->
					<button
						type="button"
						class="relative flex h-9 w-9 shrink-0 items-center justify-center rounded-full transition-all"
						:class="
							voiceState === 'listening'
								? 'bg-red-500 text-white hover:bg-red-600'
								: voiceState === 'thinking'
									? 'cursor-not-allowed text-slate-300 dark:text-slate-600'
									: 'text-primary hover:bg-primary/10'
						"
						:disabled="voiceState === 'thinking'"
						@click="toggleVoice"
					>
						<span
							v-if="voiceState === 'listening'"
							class="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-30"
						/>
						<Icon
							:icon="
								voiceState === 'listening'
									? 'stop'
									: voiceState === 'speaking'
										? 'volume-high'
										: 'microphone'
							"
							:size="18"
							class="relative z-10"
						/>
					</button>

					<!-- Send button -->
					<button
						type="button"
						class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary text-white transition-all hover:brightness-110 active:scale-95 disabled:cursor-not-allowed disabled:opacity-40"
						:disabled="voiceState === 'thinking' || !voiceTextInput.trim()"
						@click="_sendTypedMessage"
					>
						<Icon icon="send" :size="16" />
					</button>
				</div>

				<!-- ── Collected fields progress strip ── -->
				<div v-if="voiceCollectedKeys.length" class="mt-2 flex flex-wrap gap-1">
					<span
						v-for="k in voiceCollectedKeys"
						:key="k"
						class="inline-flex items-center gap-1 rounded-full border border-green-200 bg-green-50 px-2 py-0.5 text-[10px] font-semibold text-green-700 dark:border-green-700/40 dark:bg-green-900/20 dark:text-green-400"
					>
						<Icon icon="check" :size="8" />
						{{ fieldLabels[k] || k }}
					</span>
					<template v-if="voiceChildSummary.length">
						<span
							v-for="s in voiceChildSummary"
							:key="s"
							class="inline-flex items-center gap-1 rounded-full border border-green-200 bg-green-50 px-2 py-0.5 text-[10px] font-semibold text-green-700 dark:border-green-700/40 dark:bg-green-900/20 dark:text-green-400"
						>
							<Icon icon="check" :size="8" />
							{{ s }}
						</span>
					</template>
				</div>

				<!-- Completion banner -->
				<div
					v-if="voiceState === 'complete'"
					class="mt-2 flex items-center gap-2 rounded-xl border border-green-200 bg-green-50 px-3 py-2.5 dark:border-green-700/40 dark:bg-green-900/20"
				>
					<Icon
						icon="check-circle"
						:size="16"
						class="shrink-0 text-green-600 dark:text-green-400"
					/>
					<p class="text-[11.5px] font-semibold text-green-700 dark:text-green-400">
						Form filled! Review the fields above.
					</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onUnmounted } from "vue"
import { ApiService } from "../../services/api"
import AiButton from "../buttons/AiButton.vue"
import ClearButton from "../buttons/ClearButton.vue"
import AiIconBadge from "../buttons/AiIconBadge.vue"

const props = defineProps({
	modelValue: { type: Object, default: () => ({}) },
	fieldLabels: { type: Object, default: () => ({}) },
	doctype: { type: String, default: "" },
	childTableValues: { type: Object, default: () => ({}) },
	aiPlaceholder: {
		type: String,
		default: "Describe the record in natural language and AI will fill the form fields...",
	},
	sample: { type: String, default: "" },
	initialScanFile: { type: Object, default: null },
	initialExtractText: { type: String, default: null },
})

const emit = defineEmits(["update:modelValue", "update:childTables", "voice-save"])

// ── Session memory ────────────────────────────────────────────────────────────
// One UUID per component instance. Both tabs share it so a scanned doc and a
// follow-up voice correction are part of the same AI conversation.
const sessionId = crypto.randomUUID()

// ── Tab ───────────────────────────────────────────────────────────────────────
const activeTab = ref("voice")

// ── Shared helper ─────────────────────────────────────────────────────────────
// Accumulates all AI-filled main fields so they survive intermediate
// DynamicForm re-emissions that may carry a stale snapshot.
const aiFilledData = ref({})

function applyFields(fields) {
	const applied = []
	for (const [key, value] of Object.entries(fields)) {
		if (value !== null && value !== undefined && value !== "") {
			aiFilledData.value[key] = value
			applied.push(key)
		}
	}
	// props.modelValue first (preserves user manual edits), ai cache wins on top
	emit("update:modelValue", { ...props.modelValue, ...aiFilledData.value })
	return applied
}

// Returns a key for a child table row using only its string/text identifier fields
// (Link, Data, Small Text). Numeric/boolean fields are intentionally excluded so
// a partial update row {item:"X", qty:10} matches the full row {item:"X", weight:5, qty:2}.
const _ROW_SKIP = new Set([
	"name",
	"idx",
	"doctype",
	"parent",
	"parentfield",
	"parenttype",
	"owner",
])
const _ROW_NUMERIC = new Set(["number", "boolean"])
function _rowKey(row) {
	const parts = Object.entries(row)
		.filter(([k, v]) => {
			if (_ROW_SKIP.has(k)) return false
			if (v === null || v === undefined || v === "") return false
			if (_ROW_NUMERIC.has(typeof v)) return false // skip numbers & booleans
			return true
		})
		.sort(([a], [b]) => a.localeCompare(b))
		.map(([k, v]) => `${k}:${v}`)
	return parts.length ? parts.join("|") : JSON.stringify(row)
}

function applyChildTables(childTables) {
	if (!childTables || !Object.keys(childTables).length) return []
	const summary = []
	const toEmit = {}
	for (const [key, rows] of Object.entries(childTables)) {
		if (!Array.isArray(rows) || !rows.length) continue
		const merged = [...(props.childTableValues[key] || [])]
		let added = 0,
			updated = 0
		for (const newRow of rows) {
			const rk = _rowKey(newRow)
			const idx = merged.findIndex((e) => _rowKey(e) === rk)
			if (idx >= 0) {
				merged[idx] = { ...merged[idx], ...newRow }
				updated++
			} else {
				merged.push(newRow)
				added++
			}
		}
		if (added || updated) {
			toEmit[key] = merged
			if (added) summary.push(`${added} ${added === 1 ? "row" : "rows"} added`)
			if (updated) summary.push(`${updated} ${updated === 1 ? "row" : "rows"} updated`)
		}
	}
	if (Object.keys(toEmit).length) emit("update:childTables", toEmit)
	return summary
}

// ── Document Scanner ──────────────────────────────────────────────────────────
const fileInputRef = ref(null)
const scanFile = ref(null)
const scanText = ref(null)
const scanPreview = ref(null)
const scanLoading = ref(false)
const scanAppliedFields = ref([])
const scanAppliedChildSummary = ref([])
const scanWarnings = ref([])
const scanMandatoryFields = ref([])
const scanError = ref(null)
const isDragging = ref(false)

const scanMissingMandatory = computed(() => {
	return scanMandatoryFields.value.filter((f) => {
		const val = props.modelValue[f.fieldname]
		return val === null || val === undefined || val === ""
	})
})

function handleFileChange(event) {
	const file = event.target.files[0]
	if (file) loadScanFile(file)
}

function handleFileDrop(event) {
	isDragging.value = false
	const file = event.dataTransfer.files[0]
	if (file) loadScanFile(file)
}

function loadScanFile(file) {
	scanFile.value = file
	scanAppliedFields.value = []
	scanMandatoryFields.value = []
	scanError.value = null
	if (file.type.startsWith("image/")) {
		const reader = new FileReader()
		reader.onload = (e) => {
			scanPreview.value = e.target.result
		}
		reader.readAsDataURL(file)
	} else {
		scanPreview.value = null
	}
}

watch(
	() => props.initialScanFile,
	(file) => {
		if (file) {
			activeTab.value = "scanner"
			loadScanFile(file)
			// trigger extraction
			extractFromDocument()
		}
	},
	{ immediate: true },
)

watch(
	() => props.initialExtractText,
	(text) => {
		if (text) {
			activeTab.value = "scanner"
			scanText.value = text
			extractFromText(text)
		}
	},
	{ immediate: true },
)

function clearScan() {
	scanFile.value = null
	scanText.value = null
	scanPreview.value = null
	scanAppliedFields.value = []
	scanMandatoryFields.value = []
	scanWarnings.value = []
	scanError.value = null
	isDragging.value = false
	if (fileInputRef.value) fileInputRef.value.value = ""
}

async function extractFromDocument() {
	if (!scanFile.value) return
	scanLoading.value = true
	scanError.value = null
	scanAppliedFields.value = []
	scanAppliedChildSummary.value = []
	scanMandatoryFields.value = []
	try {
		const base64 = await new Promise((resolve, reject) => {
			const reader = new FileReader()
			reader.onload = (e) => resolve(e.target.result.split(",")[1])
			reader.onerror = reject
			reader.readAsDataURL(scanFile.value)
		})
		const collected = {
			...props.modelValue,
			...props.childTableValues,
		}
		const res = await ApiService.post("tms.ai.endpoints.engine.fill_from_document", {
			file_data: base64,
			file_type: scanFile.value.type,
			doctype: props.doctype,
			session_id: sessionId,
			collected: JSON.stringify(collected),
		})
		if (res.status && res.data) {
			if (res.data.is_invalid) {
				scanError.value =
					"This document doesn't seem to match a Shipment Request. Please upload a relevant document."
				return
			}
			scanWarnings.value = res.data.warnings || []
			scanMandatoryFields.value = res.data.mandatory_fields || []
			scanAppliedFields.value = applyFields(res.data.fields || {})
			scanAppliedChildSummary.value = applyChildTables(res.data.child_tables)
			if (!scanAppliedFields.value.length && !scanAppliedChildSummary.value.length) {
				scanError.value = "No fields could be filled from this document."
			}
		} else {
			scanError.value = res.message || "Failed to extract data from document"
		}
	} catch (e) {
		scanError.value = e.message || "Document extraction failed"
	} finally {
		scanLoading.value = false
	}
}

async function extractFromText(text) {
	if (!text) return
	scanLoading.value = true
	scanError.value = null
	scanAppliedFields.value = []
	scanAppliedChildSummary.value = []
	scanMandatoryFields.value = []

	try {
		const res = await ApiService.post("tms.ai.endpoints.engine.fill_from_description", {
			description: text,
			doctype: props.doctype,
			session_id: sessionId,
		})

		if (res.status && res.data) {
			if (res.data.is_invalid) {
				scanError.value =
					"This text doesn't seem to match a Shipment Request. Please provide relevant text."
				return
			}
			scanWarnings.value = res.data.warnings || []
			scanMandatoryFields.value = res.data.mandatory_fields || []
			scanAppliedFields.value = applyFields(res.data.fields || {})
			scanAppliedChildSummary.value = applyChildTables(res.data.child_tables)
			if (!scanAppliedFields.value.length && !scanAppliedChildSummary.value.length) {
				scanError.value = "No fields could be filled from this text."
			}
		} else {
			scanError.value = res.message || "Failed to extract data from text"
		}
	} catch (e) {
		scanError.value = e.message || "Text extraction failed"
	} finally {
		scanLoading.value = false
	}
}

// ── Voice Agent (Conversational) ─────────────────────────────────────────────
// States: 'idle' | 'listening' | 'thinking' | 'speaking' | 'complete'
const voiceState = ref("idle")
const voiceTranscript = ref("") // current interim transcript
const voiceTextInput = ref("") // typed message (text alternative to speaking)
const voiceMode = ref(false) // true when conversing by voice → auto-reopen mic after replies
const voiceDurationLabel = ref("0:00")
const voiceAgentError = ref(null)
const voiceChatMessages = ref([]) // [{ role: 'ai'|'user', text }]
const voiceCollectedFields = ref({}) // accumulated main fields
const voiceCollectedChildTables = ref({})
const voiceCollectedKeys = ref([]) // field keys shown as green chips
const voiceChildSummary = ref([])
const chatScrollRef = ref(null)
const waveCanvasRef = ref(null)

let _voiceAnimFrame = null
let _voiceSpeech = null
let _voiceDurationTimer = null
let _voiceDurationSecs = 0
let _voiceWavePhase = 0
let _ttsUtterance = null
let _silenceTimer = null
// How long to wait after you STOP talking before the agent takes your turn.
// Raise this if it cuts you off mid-thought; lower it for snappier turns.
const VOICE_SILENCE_MS = 2000

// ── TTS (AI speaks back) ──────────────────────────────────────────────────────
let _ttsTimeoutId = null

// Strip markdown so the voice reads naturally (no "asterisk", no "1 dot")
function _stripMarkdown(text) {
	return String(text || "")
		.replace(/\*\*(.+?)\*\*/g, "$1")
		.replace(/[*_`#]/g, "")
		.replace(/^\s*[-•]\s+/gm, "")
		.replace(/^\s*\d+\.\s+/gm, "")
		.replace(/\n+/g, ". ")
		.trim()
}

function _speak(text, onEnd) {
	if (!window.speechSynthesis) {
		onEnd?.()
		return
	}
	window.speechSynthesis.cancel()
	clearTimeout(_ttsTimeoutId)

	_ttsUtterance = new SpeechSynthesisUtterance(_stripMarkdown(text))
	_ttsUtterance.rate = 1.05
	_ttsUtterance.pitch = 1.0
	_ttsUtterance.volume = 1.0

	// Guard against double-fire and Chrome's onend-never-fires bug
	let _fired = false
	const _done = (via) => {
		if (_fired) return
		_fired = true
		clearTimeout(_ttsTimeoutId)
		console.log(`[Voice] TTS done via=${via} → calling onEnd, state will go to idle`)
		onEnd?.()
	}
	_ttsUtterance.onend = () => _done("onend")
	_ttsUtterance.onerror = (ev) => {
		console.warn("[Voice] TTS onerror:", ev.error)
		_done("onerror")
	}

	// Chrome sometimes never fires onend — force resolve after estimated duration
	const estimatedMs = Math.max(6000, text.split(" ").length * 420)
	console.log(`[Voice] TTS starting — ${text.split(" ").length} words, timeout=${estimatedMs}ms`)
	_ttsTimeoutId = setTimeout(() => _done("timeout"), estimatedMs)

	voiceState.value = "speaking"
	window.speechSynthesis.speak(_ttsUtterance)
}

function _stopSpeaking() {
	clearTimeout(_ttsTimeoutId)
	// Null handlers BEFORE cancel() — otherwise cancel() fires onend/onerror
	// asynchronously, which calls the onEnd callback and resets voiceState to
	// 'idle', overwriting the 'listening' state set by _startVoiceRecording().
	if (_ttsUtterance) {
		_ttsUtterance.onend = null
		_ttsUtterance.onerror = null
		_ttsUtterance = null
	}
	if (window.speechSynthesis) window.speechSynthesis.cancel()
}

// ── Duration timer ────────────────────────────────────────────────────────────
function _startDurationTimer() {
	_voiceDurationSecs = 0
	voiceDurationLabel.value = "0:00"
	_voiceDurationTimer = setInterval(() => {
		_voiceDurationSecs++
		const m = Math.floor(_voiceDurationSecs / 60)
		const s = String(_voiceDurationSecs % 60).padStart(2, "0")
		voiceDurationLabel.value = `${m}:${s}`
	}, 1000)
}

function _stopDurationTimer() {
	clearInterval(_voiceDurationTimer)
}

// ── Waveform ──────────────────────────────────────────────────────────────────
function _drawWaveform(active) {
	const canvas = waveCanvasRef.value
	if (!canvas) return
	const ctx = canvas.getContext("2d")
	const dpr = window.devicePixelRatio || 1
	const rect = canvas.getBoundingClientRect()
	if (canvas.width !== Math.round(rect.width * dpr)) {
		canvas.width = Math.round(rect.width * dpr)
		canvas.height = Math.round(rect.height * dpr)
	}
	const W = canvas.width,
		H = canvas.height
	ctx.clearRect(0, 0, W, H)
	const NUM_BARS = 32
	const barW = (W / NUM_BARS) * 0.55
	const gap = (W / NUM_BARS) * 0.45
	const cy = H / 2
	for (let i = 0; i < NUM_BARS; i++) {
		const x = i * (barW + gap) + gap / 2
		let amp
		if (active) {
			amp = (Math.sin(i * 0.45 + _voiceWavePhase) * 0.35 + 0.5 + Math.random() * 0.3) * H * 0.38
		} else {
			amp = (Math.sin(i * 0.4 + _voiceWavePhase * 0.25) * 0.2 + 0.28) * H * 0.22
		}
		ctx.fillStyle = active ? `rgba(239,68,68,0.7)` : `rgba(99,102,241,0.35)`
		ctx.beginPath()
		const bh = Math.max(amp * 2, 2 * dpr)
		if (ctx.roundRect) ctx.roundRect(x, cy - amp, barW, bh, barW / 2)
		else ctx.rect(x, cy - amp, barW, bh)
		ctx.fill()
	}
}

function _startWaveLoop() {
	function loop() {
		_voiceWavePhase += voiceState.value === "listening" ? 0.11 : 0.022
		_drawWaveform(voiceState.value === "listening")
		_voiceAnimFrame = requestAnimationFrame(loop)
	}
	if (_voiceAnimFrame) cancelAnimationFrame(_voiceAnimFrame)
	loop()
}

function _stopWaveLoop() {
	if (_voiceAnimFrame) {
		cancelAnimationFrame(_voiceAnimFrame)
		_voiceAnimFrame = null
	}
}

function _stopSpeechRecognition() {
	clearTimeout(_silenceTimer)
	if (_voiceSpeech) {
		try {
			_voiceSpeech.stop()
		} catch (_e) {
			// ignore stop errors
		}
		_voiceSpeech = null
	}
}

// ── Scroll chat to bottom ─────────────────────────────────────────────────────
function _scrollChat() {
	nextTick(() => {
		const el = chatScrollRef.value
		if (el) el.scrollTop = el.scrollHeight
	})
}

// ── Minimal, safe markdown → HTML for AI bubbles (bold, bullets, numbered lists) ──
function _escapeHtml(s) {
	return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
}
function _renderMarkdown(text) {
	const lines = String(text || "").split("\n")
	let html = ""
	let listType = null // 'ul' | 'ol'
	const closeList = () => {
		if (listType) {
			html += `</${listType}>`
			listType = null
		}
	}
	const inline = (s) => _escapeHtml(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
	for (const raw of lines) {
		const line = raw.trim()
		const ol = line.match(/^\d+\.\s+(.*)$/)
		const ul = line.match(/^[-•]\s+(.*)$/)
		if (ol) {
			if (listType !== "ol") {
				closeList()
				html += '<ol class="ml-4 list-decimal space-y-0.5">'
				listType = "ol"
			}
			html += `<li>${inline(ol[1])}</li>`
		} else if (ul) {
			if (listType !== "ul") {
				closeList()
				html += '<ul class="ml-4 list-disc space-y-0.5">'
				listType = "ul"
			}
			html += `<li>${inline(ul[1])}</li>`
		} else {
			closeList()
			if (line) html += `<p>${inline(line)}</p>`
		}
	}
	closeList()
	return html
}

// ── Add a message bubble ──────────────────────────────────────────────────────
function _addMessage(role, text) {
	voiceChatMessages.value.push({ role, text })
	_scrollChat()
}

// ── Apply AI response state into the form ─────────────────────────────────────
// The backend is the single source of truth: when child_tables carries _replace,
// the payload is the COMPLETE authoritative state, so we replace rather than merge.
function _mergeVoiceFields(fields, childTables) {
	const authoritative = childTables?._replace === true

	// Main fields — backend always sends the full confirmed set; replace wholesale
	// when authoritative, otherwise fall back to a merge (older greet payloads).
	if (authoritative) {
		voiceCollectedFields.value = { ...(fields || {}) }
	} else {
		for (const [k, v] of Object.entries(fields || {})) {
			if (v !== null && v !== undefined && v !== "") voiceCollectedFields.value[k] = v
		}
	}
	voiceCollectedKeys.value = Object.keys(voiceCollectedFields.value)

	// Child tables — replace each provided table with the authoritative list
	for (const [key, rows] of Object.entries(childTables || {})) {
		if (key === "_replace" || key === "_stops_replaced") continue
		if (!Array.isArray(rows)) continue
		voiceCollectedChildTables.value[key] = [...rows]
	}

	// Refresh the summary chips (Stops / Items)
	voiceChildSummary.value = []
	if (voiceCollectedChildTables.value.request_stops?.length) voiceChildSummary.value.push("Stops")
	if (
		voiceCollectedChildTables.value.item?.length ||
		voiceCollectedChildTables.value.request_items?.length
	)
		voiceChildSummary.value.push("Items")

	// Emit to parent form
	emit("update:modelValue", { ...props.modelValue, ...voiceCollectedFields.value })
	if (Object.keys(voiceCollectedChildTables.value).length) {
		emit("update:childTables", { ...voiceCollectedChildTables.value })
	}
}

// ── Send a typed message (text alternative to speaking) ───────────────────────
function _sendTypedMessage() {
	const text = voiceTextInput.value.trim()
	if (!text || voiceState.value === "thinking") return
	voiceMode.value = false // typed → don't auto-open the mic after the reply
	_stopSpeaking() // cancel any in-progress TTS
	voiceTextInput.value = ""
	_addMessage("user", text) // same chat thread as voice
	_sendTurn(text) // same pipeline as voice
}

// ── Send a user turn to the API ───────────────────────────────────────────────
async function _sendTurn(userText) {
	voiceState.value = "thinking"
	try {
		// Send the ACTUAL current form (props), so manual edits/removals/additions made
		// directly in the form are synced into the agent's source-of-truth JSON each turn.
		const collected = {
			...props.modelValue,
			...props.childTableValues,
		}
		const res = await ApiService.post("tms.ai.endpoints.agent.agent_chat", {
			message: userText,
			doctype: props.doctype,
			session_id: sessionId,
			collected: JSON.stringify(collected),
		})
		if (res.status && res.data) {
			const { response, fields, child_tables, is_complete, do_save } = res.data
			_mergeVoiceFields(fields, child_tables)
			_addMessage("ai", response)
			if (do_save) {
				// Saved — conversation done, don't reopen the mic
				voiceState.value = "complete"
				_speak(response, () => {
					voiceState.value = "idle"
				})
				nextTick(() => emit("voice-save"))
			} else {
				// Speak the reply, then in voice mode auto-reopen the mic for the next turn
				// (hands-free), otherwise go idle. Empty speech → no infinite loop (onend idles).
				_speak(response, () => {
					if (voiceMode.value) _startVoiceRecording()
					else voiceState.value = is_complete ? "complete" : "idle"
				})
			}
		} else {
			voiceAgentError.value = res.message || "AI response failed."
			voiceState.value = "idle"
		}
	} catch (e) {
		voiceAgentError.value = e.message || "AI request failed."
		voiceState.value = "idle"
	}
}

// ── Greet (first turn) ────────────────────────────────────────────────────────
async function _startConversation() {
	voiceState.value = "thinking"
	try {
		// Send the current form so the agent continues from any pre-filled data
		const collected = { ...props.modelValue, ...props.childTableValues }
		const res = await ApiService.post("tms.ai.endpoints.agent.agent_greet", {
			doctype: props.doctype,
			session_id: sessionId,
			collected: JSON.stringify(collected),
		})
		if (res.status && res.data) {
			const { response, fields, child_tables } = res.data
			if (fields || child_tables) _mergeVoiceFields(fields, child_tables)
			_addMessage("ai", response)
			_speak(response, () => {
				if (voiceMode.value) _startVoiceRecording()
				else voiceState.value = "idle"
			})
		} else {
			voiceState.value = "idle"
		}
	} catch {
		voiceState.value = "idle"
	}
}

// ── Start / stop recording ────────────────────────────────────────────────────
function _startVoiceRecording() {
	voiceAgentError.value = null
	voiceTranscript.value = ""
	_stopSpeaking() // cancel any TTS
	_startWaveLoop()

	const SR = window.SpeechRecognition || window.webkitSpeechRecognition
	if (!SR) {
		voiceAgentError.value = "Speech recognition not supported in this browser."
		return
	}

	// Show listening state immediately for snappy UI
	voiceState.value = "listening"
	_startDurationTimer()

	// Chrome keeps the audio device busy for a moment after speechSynthesis ends —
	// starting SpeechRecognition too soon causes "audio-capture".
	// 200 ms is enough for the synthesis pipeline to release the device.
	// Mic permission is already granted so setTimeout is safe here.
	setTimeout(() => _doStartRecognition(SR), 200)
}

function _doStartRecognition(SR, retryCount = 0) {
	// If state was changed (e.g. user reset) while we were waiting, bail out
	if (voiceState.value !== "listening") {
		console.log("[Voice] _doStartRecognition cancelled — state changed to", voiceState.value)
		return
	}

	// Kill any lingering instance before creating a new one
	if (_voiceSpeech) {
		const _old = _voiceSpeech
		_voiceSpeech = null
		try {
			_old.abort()
		} catch (_e) {
			// ignore abort errors
		}
	}

	const speech = new SR()
	const sessionId_dbg = Math.random().toString(36).slice(2, 6)
	_voiceSpeech = speech
	console.log(`[Voice] session ${sessionId_dbg} — new SR instance, retry=${retryCount}`)

	speech.lang = "en-US"
	speech.interimResults = true
	speech.maxAlternatives = 1
	// continuous = true so a pause mid-sentence doesn't end recognition. We decide when
	// the turn is over with our OWN silence timer (VOICE_SILENCE_MS), reset on every word.
	speech.continuous = true

	let finalText = ""

	speech.onresult = (e) => {
		if (_voiceSpeech !== speech) {
			console.warn(`[Voice] session ${sessionId_dbg} onresult — STALE, ignored`)
			return
		}
		let interim = ""
		for (let i = e.resultIndex; i < e.results.length; i++) {
			const t = e.results[i][0].transcript
			if (e.results[i].isFinal) finalText += t + " "
			else interim = t
		}
		voiceTranscript.value = (finalText + interim).trim()
		console.log(
			`[Voice] session ${sessionId_dbg} onresult — transcript: "${voiceTranscript.value}"`,
		)
		// Restart the silence countdown on every bit of speech; when it elapses with no
		// new words, end the turn (stop → onend → send).
		clearTimeout(_silenceTimer)
		_silenceTimer = setTimeout(() => {
			if (_voiceSpeech === speech) {
				try {
					speech.stop()
				} catch (_e) {
					// ignore stop errors
				}
			}
		}, VOICE_SILENCE_MS)
	}

	speech.onerror = (e) => {
		const isStale = _voiceSpeech !== speech
		console.error(
			`[Voice] session ${sessionId_dbg} onerror — error="${e.error}" stale=${isStale} retry=${retryCount}`,
		)
		if (isStale) return
		clearTimeout(_silenceTimer)
		_voiceSpeech = null

		// Chrome keeps the audio device busy after TTS/previous SR ends.
		// Auto-retry up to 4 times with growing back-off (300 → 600 → 900 → 1200 ms).
		if (e.error === "audio-capture" && retryCount < 4) {
			const delay = (retryCount + 1) * 300
			console.log(`[Voice] audio-capture — retrying in ${delay}ms (attempt ${retryCount + 1}/4)`)
			setTimeout(() => _doStartRecognition(SR, retryCount + 1), delay)
			return
		}

		// After a previous SR + TTS session, Chrome can fire no-speech immediately
		// (audio pipeline not yet ready) even when the user is speaking. Retry once
		// if no transcript was captured at all (i.e. mic was silent from the start).
		if (e.error === "no-speech" && !voiceTranscript.value && retryCount < 2) {
			console.log(
				`[Voice] no-speech with empty transcript — retrying in 400ms (attempt ${retryCount + 1}/2)`,
			)
			setTimeout(() => _doStartRecognition(SR, retryCount + 1), 400)
			return
		}

		_stopDurationTimer()
		if (e.error === "not-allowed") {
			voiceAgentError.value = "Microphone access denied. Allow microphone access and try again."
		} else if (e.error !== "no-speech" && e.error !== "aborted") {
			voiceAgentError.value = "Speech recognition error — please try again."
		}
		voiceState.value = "idle"
	}

	speech.onend = () => {
		const isStale = _voiceSpeech !== speech
		console.log(
			`[Voice] session ${sessionId_dbg} onend — stale=${isStale} voiceState="${voiceState.value}" transcript="${voiceTranscript.value.trim()}"`,
		)
		if (isStale) return
		clearTimeout(_silenceTimer)
		_voiceSpeech = null
		if (voiceState.value !== "listening") return
		_stopDurationTimer()
		const text = voiceTranscript.value.trim()
		if (text) {
			_addMessage("user", text)
			voiceTranscript.value = ""
			_sendTurn(text)
		} else {
			voiceState.value = "idle"
		}
	}

	try {
		speech.start()
		console.log(`[Voice] session ${sessionId_dbg} — start() called OK`)
	} catch (err) {
		console.error(`[Voice] session ${sessionId_dbg} — start() threw:`, err)
		_voiceSpeech = null
		_stopDurationTimer()
		voiceState.value = "idle"
		voiceAgentError.value = "Could not start voice recognition — please try again."
	}
}

function _cleanupRecording() {
	_stopSpeechRecognition()
	_stopDurationTimer()
}

function toggleVoice() {
	console.log(
		`[Voice] toggleVoice — state="${voiceState.value}" messages=${voiceChatMessages.value.length} _voiceSpeech=${!!_voiceSpeech}`,
	)
	// Any mic tap puts us in voice mode → the mic auto-reopens after each reply.
	if (voiceState.value !== "listening") voiceMode.value = true
	if (voiceState.value === "listening") {
		voiceState.value = "thinking"
		_stopDurationTimer()
		console.log("[Voice] manual stop → calling speech.stop()")
		_voiceSpeech?.stop()
	} else if (voiceState.value === "idle") {
		if (!voiceChatMessages.value.length) {
			_startConversation()
		} else {
			_startVoiceRecording()
		}
	} else if (voiceState.value === "speaking") {
		console.log("[Voice] interrupting TTS → starting recording")
		_stopSpeaking()
		_startVoiceRecording()
	} else if (voiceState.value === "complete") {
		voiceState.value = "idle"
		_startVoiceRecording()
	}
}

// Exit the hands-free conversation: stop listening + TTS, don't reopen the mic.
function endVoiceConversation() {
	voiceMode.value = false
	_cleanupRecording() // stops recognition + clears the silence timer
	_stopSpeaking() // stop any TTS playback
	_stopWaveLoop()
	voiceTranscript.value = ""
	voiceState.value = "idle"
}

function resetVoiceAgent() {
	_cleanupRecording()
	_stopSpeaking()
	_stopWaveLoop()
	voiceMode.value = false
	voiceState.value = "idle"
	voiceTranscript.value = ""
	voiceDurationLabel.value = "0:00"
	voiceAgentError.value = null
	voiceChatMessages.value = []
	voiceCollectedFields.value = {}
	voiceCollectedChildTables.value = {}
	voiceCollectedKeys.value = []
	voiceChildSummary.value = []
}

// Start waveform loop when tab is activated; stop on deactivate
watch(
	() => activeTab.value,
	(tab) => {
		if (tab === "voice") {
			nextTick(() => _startWaveLoop())
		} else {
			_stopWaveLoop()
			_stopSpeaking()
		}
	},
)

onUnmounted(() => {
	_cleanupRecording()
	_stopSpeaking()
	_stopWaveLoop()
})
</script>
