<template>
	<nav class="breadcrumbs mb-6 flex flex-col gap-0">
		<ol class="breadcrumb-list m-0 flex list-none items-center gap-2 p-0">
			<li
				v-for="(item, index) in items"
				:key="index"
				class="breadcrumb-item flex items-center gap-2 font-sans text-[16px]"
			>
				<router-link
					v-if="item.to && index < items.length - 1"
					:to="item.to"
					class="breadcrumb-link inline-flex items-center gap-1.5 font-medium text-slate-500 no-underline transition-colors duration-200 hover:text-primary dark:text-slate-400 dark:hover:text-primary-light"
				>
					<Icon v-if="item.icon" :icon="item.icon" :size="16" />
					{{ item.label }}
				</router-link>

				<span
					v-else
					class="breadcrumb-current inline-flex items-center gap-1.5 transition-all duration-200"
					:class="[
						index === items.length - 1
							? 'cursor-pointer font-extrabold text-primary active:scale-95 dark:text-primary'
							: 'font-semibold text-slate-500 dark:text-slate-400',
					]"
					@click="index === items.length - 1 && copyToClipboard(item.label)"
				>
					<Icon v-if="item.icon" :icon="item.icon" :size="16" />
					{{ item.label }}

					<svg
						v-if="index === items.length - 1"
						class="copy-icon transition-all duration-200"
						:class="[
							copied
								? 'text-emerald-500 opacity-100'
								: 'text-slate-400 opacity-0 group-hover:opacity-100',
						]"
						width="11"
						height="11"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2.5"
					>
						<template v-if="!copied">
							<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
							<rect x="8" y="2" width="8" height="4" rx="1" ry="1" />
						</template>
						<polyline v-else points="20 6 9 17 4 12" />
					</svg>
				</span>

				<svg
					v-if="index < items.length - 1"
					class="breadcrumb-separator h-4 w-4 flex-shrink-0 select-none text-slate-400 dark:text-slate-400"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="3"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<polyline points="9 18 15 12 9 6" />
				</svg>
			</li>
		</ol>
		<p v-if="subtitle" class="m-0 text-[11px] text-slate-500 dark:text-slate-400">
			{{ subtitle }}
		</p>
	</nav>
</template>

<script>
import { ref, computed } from "vue"
import { useToast } from "@/services/toastService"
import Icon from "@/components/Icon.vue"

export default {
	name: "Breadcrumbs",
	components: { Icon },
	props: {
		items: {
			type: Array,
			required: true,
		},
	},
	setup(props) {
		const copied = ref(false)
		const toast = useToast()
		let timeoutId = null

		const subtitle = computed(() => props.items[props.items.length - 1]?.subtitle || "")

		const copyToClipboard = async (text) => {
			try {
				await navigator.clipboard.writeText(text)
				copied.value = true
				toast.success(`Copied to clipboard`, { duration: 2000 })

				if (timeoutId) clearTimeout(timeoutId)
				timeoutId = setTimeout(() => {
					copied.value = false
				}, 2000)
			} catch (err) {
				console.error("Failed to copy:", err)
				toast.error("Failed to copy", { duration: 2000 })
			}
		}

		return {
			copied,
			copyToClipboard,
			subtitle,
		}
	},
}
</script>

<style scoped>
/* Added to handle the hover trigger for the icon since we aren't using a parent group class here */
.breadcrumb-current:hover .copy-icon {
	opacity: 1;
}
</style>
