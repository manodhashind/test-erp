<template>
  <Login v-if="!currentUser" @logged-in="onLoggedIn" />
  <div v-else class="app-shell">
    <Sidebar
      v-model="activeTab"
      :current-user="currentUser"
      :is-admin="isAdmin"
      @logout="logout"
    />

    <main class="main">
      <transition name="fade" mode="out-in">
        <div v-if="editingUser && isAdmin" key="edit">
          <h1 class="page-title">Edit user</h1>
          <EditUser :user="editingUser" @cancel="editingUser = null" @updated="onUpdated" />
        </div>
        <div v-else-if="activeTab === 'admin-settings' && isAdmin" key="admin-settings">
          <h1 class="page-title">Admin settings</h1>
          <AdminSettings />
        </div>
        <div v-else-if="activeTab === 'create' && isAdmin" key="create">
          <h1 class="page-title">New user</h1>
          <CreateUser />
        </div>
        <div v-else-if="activeTab === 'view'" key="view">
          <h1 class="page-title">All users</h1>
          <ViewUsers :is-admin="isAdmin" @edit="startEdit" />
        </div>
        <div v-else-if="activeTab === 'dashboard'" key="dashboard">
          <h1 class="page-title">Dashboard</h1>
          <Dashboard />
        </div>
        <div v-else-if="activeTab === 'projects'" key="projects">
          <h1 class="page-title">Projects</h1>
          <Projects />
        </div>
        <div v-else-if="activeTab === 'sites'" key="sites">
          <h1 class="page-title">Sites</h1>
          <Sites />
        </div>
        <div v-else-if="activeTab === 'workers'" key="workers">
          <h1 class="page-title">Workers</h1>
          <Workers />
        </div>
        <div v-else-if="activeTab === 'materials'" key="materials">
          <h1 class="page-title">Materials</h1>
          <Materials />
        </div>
        <div v-else-if="activeTab === 'bulk-import' && isAdmin" key="bulk-import">
          <h1 class="page-title">Bulk import</h1>
          <BulkImportUsers />
        </div>
      </transition>
      <ChatWidget v-if="isAdmin" />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Login from './components/Login.vue'
import Sidebar from './components/Sidebar.vue'
import CreateUser from './components/CreateUser.vue'
import ViewUsers from './components/ViewUsers.vue'
import EditUser from './components/EditUser.vue'
import Dashboard from './components/pages/Dashboard.vue'
import Projects from './components/pages/Projects.vue'
import Sites from './components/pages/Sites.vue'
import Workers from './components/pages/Workers.vue'
import Materials from './components/pages/Materials.vue'
import AdminSettings from './components/pages/AdminSettings.vue'
import BulkImportUsers from './components/BulkImportUsers.vue'
import ChatWidget from './components/chat/ChatWidget.vue'

const currentUser = ref(null)
const isAdmin = ref(false)
const activeTab = ref('dashboard')
const editingUser = ref(null)

async function fetchUserInfo() {
  const res = await fetch('/api/method/construction_management.api.get_current_user_info', { credentials: 'include' })
  const data = await res.json()
  currentUser.value = data.message.user
  isAdmin.value = data.message.is_admin
}

onMounted(async () => {
  try {
    const res = await fetch('/api/method/frappe.auth.get_logged_user', { credentials: 'include' })
    const data = await res.json()
    if (data.message && data.message !== 'Guest') await fetchUserInfo()
  } catch (e) {}
})

async function onLoggedIn() { await fetchUserInfo() }
async function logout() {
  await fetch('/api/method/logout', { method: 'POST', credentials: 'include' })
  currentUser.value = null
  isAdmin.value = false
}
function startEdit(user) { editingUser.value = user }
function onUpdated() { editingUser.value = null }
</script>