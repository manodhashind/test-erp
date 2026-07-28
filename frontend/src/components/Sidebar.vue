<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <span class="brand">Site Register</span>
      <span class="brand-sub">Construction Management</span>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-section">Overview</div>
      <button
        v-for="item in overviewItems"
        :key="item.key"
        class="nav-item"
        :class="{ active: modelValue === item.key }"
        @click="$emit('update:modelValue', item.key)"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        {{ item.label }}
      </button>

      <div class="nav-section">Operations</div>
      <button
        v-for="item in opsItems"
        :key="item.key"
        class="nav-item"
        :class="{ active: modelValue === item.key }"
        @click="$emit('update:modelValue', item.key)"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        {{ item.label }}
      </button>

      <div class="nav-section">Admin</div>
      <button
        v-for="item in visibleAdminItems"
        :key="item.key"
        class="nav-item"
        :class="{ active: modelValue === item.key }"
        @click="$emit('update:modelValue', item.key)"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        {{ item.label }}
      </button>
    </nav>

    <div class="sidebar-footer">
      <span class="footer-user">{{ currentUser }}</span>
      <span v-if="isAdmin" class="footer-badge">Admin</span>
      <button class="btn-danger-text" style="display:block;margin-top:6px;padding:0" @click="$emit('logout')">
        Sign out
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: String,
  currentUser: String,
  isAdmin: Boolean,
})
defineEmits(['update:modelValue', 'logout'])

const overviewItems = [
  { key: 'dashboard', label: 'Dashboard', icon: '◫' },
  { key: 'projects', label: 'Projects', icon: '▤' },
]
const opsItems = [
  { key: 'sites', label: 'Sites', icon: '⌂' },
  { key: 'workers', label: 'Workers', icon: '◍' },
  { key: 'materials', label: 'Materials', icon: '▧' },
]
const adminItems = [
  { key: 'admin-settings', label: 'Admin settings', icon: '⚙', adminOnly: true },
  { key: 'create', label: 'New user', icon: '＋', adminOnly: true },
  { key: 'view', label: 'All users', icon: '☰', adminOnly: false },
  { key: 'bulk-import', label: 'Bulk import', icon: '⇪', adminOnly: true },
]

const visibleAdminItems = computed(() =>
  adminItems.filter(item => !item.adminOnly || props.isAdmin)
)
</script>