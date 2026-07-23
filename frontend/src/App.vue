<template>
  <Login v-if="!currentUser" @logged-in="onLoggedIn" />

  <div v-else class="app-shell">
    <aside class="sidebar">
      <span class="brand">Site Register</span>
      <span class="brand-sub">Construction Mgmt</span>

      <button
        v-if="isAdmin"
        class="nav-item"
        :class="{ active: activeTab === 'create' }"
        @click="switchTab('create')"
      >
        + New User
      </button>
      <button class="nav-item" :class="{ active: activeTab === 'view' }" @click="switchTab('view')">
        All Users
      </button>

      <div style="margin-top:auto;padding-top:24px;border-top:1px solid rgba(255,255,255,0.1);font-size:12px;color:#9AA3B5">
        {{ currentUser }}
        <span v-if="isAdmin" style="color:var(--amber)"> · Admin</span>
        <button class="btn-danger-text" style="display:block;margin-top:6px;padding:0" @click="logout">Sign out</button>
      </div>
    </aside>

    <main class="main">
      <transition name="fade" mode="out-in">
        <div v-if="editingUser && isAdmin" key="edit">
          <h1 class="page-title">Edit User</h1>
          <EditUser :user="editingUser" @cancel="editingUser = null" @updated="onUpdated" />
        </div>
        <div v-else-if="activeTab === 'create' && isAdmin" key="create">
          <h1 class="page-title">New User</h1>
          <CreateUser />
        </div>
        <div v-else key="view">
          <h1 class="page-title">All Users</h1>
          <ViewUsers :is-admin="isAdmin" @edit="startEdit" />
        </div>
      </transition>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Login from './components/Login.vue'
import CreateUser from './components/CreateUser.vue'
import ViewUsers from './components/ViewUsers.vue'
import EditUser from './components/EditUser.vue'

const currentUser = ref(null)
const isAdmin = ref(false)
const activeTab = ref('view')
const editingUser = ref(null)

async function fetchUserInfo() {
  const res = await fetch('/api/method/construction_management.api.get_current_user_info', {
    credentials: 'include',
  })
  const data = await res.json()
  currentUser.value = data.message.user
  isAdmin.value = data.message.is_admin
}

onMounted(async () => {
  try {
    const res = await fetch('/api/method/frappe.auth.get_logged_user', { credentials: 'include' })
    const data = await res.json()
    if (data.message && data.message !== 'Guest') {
      await fetchUserInfo()
    }
  } catch (e) {
    // not logged in
  }
})

async function onLoggedIn() {
  await fetchUserInfo()
}

async function logout() {
  await fetch('/api/method/logout', { method: 'POST', credentials: 'include' })
  currentUser.value = null
  isAdmin.value = false
}

function switchTab(tab) { editingUser.value = null; activeTab.value = tab }
function startEdit(user) { editingUser.value = user }
function onUpdated() { editingUser.value = null }
</script>