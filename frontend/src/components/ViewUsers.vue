<template>
  <div>
    <button class="btn btn-ghost btn-sm" style="margin-bottom:16px" @click="loadUsers">Refresh</button>
    <div v-if="loading">Loading...</div>
    <table v-else class="data-table">
      <thead>
        <tr>
          <th>Email</th><th>Full Name</th><th>Status</th>
          <th v-if="isAdmin"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(u, i) in users" :key="u.email" :style="{ animationDelay: i * 0.03 + 's' }" >
          <td class="mono">{{ u.email }}</td>
          <td>{{ u.first_name }} {{ u.last_name }}</td>
          <td>
            <span class="pill" :class="u.enabled ? 'pill-on' : 'pill-off'">
              {{ u.enabled ? 'Active' : 'Disabled' }}
            </span>
          </td>
          <td v-if="isAdmin" style="text-align:right">
            <button class="btn btn-ghost btn-sm" @click="$emit('edit', u)">Edit</button>
            <button class="btn-danger-text" @click="deleteUser(u.email)" :disabled="deleting === u.email">
              {{ deleting === u.email ? 'Deleting…' : 'Delete' }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="deleteError" class="toast toast-error">{{ deleteError }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

defineProps({ isAdmin: { type: Boolean, default: false } })
defineEmits(['edit'])

const users = ref([])
const loading = ref(false)
const deleting = ref(null)
const deleteError = ref('')

async function loadUsers() {
  loading.value = true
  try {
    const res = await fetch('/api/method/construction_management.api.get_all_users', {
      credentials: 'include',
    })
    const data = await res.json()
    users.value = data.message || []
  } finally {
    loading.value = false
  }
}

onMounted(loadUsers)

async function deleteUser(email) {
  if (!confirm(`Delete user ${email}? This cannot be undone.`)) return
  deleting.value = email
  deleteError.value = ''
  try {
    const res = await fetch(`/api/resource/User/${encodeURIComponent(email)}`, {
      method: 'DELETE', credentials: 'include',
    })
    if (!res.ok) throw new Error('Delete failed')
    loadUsers()
  } catch (e) {
    deleteError.value = e.message
  } finally {
    deleting.value = null
  }
}
</script>