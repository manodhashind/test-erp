<template>
	<div class="tab-content">
		<transition :name="transitionName" mode="out-in">
			<component :is="currentComponent" :key="activeTab" v-bind="componentProps" />
		</transition>
	</div>
</template>

<script>
export default {
	name: "TabContent",
	props: {
		activeTab: {
			type: String,
			required: true,
		},
		tabComponents: {
			type: Object,
			required: true,
			// Format: { 'tab1': Component, 'tab2': Component }
		},
		componentProps: {
			type: Object,
			default: () => ({}),
		},
		transitionName: {
			type: String,
			default: "fade",
		},
	},
	computed: {
		currentComponent() {
			return this.tabComponents[this.activeTab]
		},
	},
}
</script>

<style scoped>
.tab-content {
	position: relative;
	min-height: 200px;
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}

/* Slide transition */
.slide-enter-active,
.slide-leave-active {
	transition: all 0.3s ease;
}

.slide-enter-from {
	transform: translateX(20px);
	opacity: 0;
}

.slide-leave-to {
	transform: translateX(-20px);
	opacity: 0;
}
</style>
