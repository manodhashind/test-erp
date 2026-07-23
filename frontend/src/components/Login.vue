<template>
  <div class="login-screen">
    <div class="login-panel">
      <span class="brand-sub" style="color:var(--amber)">Construction Management</span>
      <h1 style="margin:6px 0 24px">Site Register</h1>
      <form @submit.prevent="submitLogin">
        <div class="field">
          <label>Email</label>
          <input v-model="usr" type="data" required autofocus />
        </div>
        <div class="field">
          <label>Password</label>
          <input v-model="pwd" type="password" required />
        </div>
        <button type="submit" class="btn btn-primary" style="width:100%" :disabled="loading">
          {{ loading ? 'Signing in…' : 'Sign In' }}
        </button>
      </form>
      <p v-if="error" class="toast toast-error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['loggedIn'])
const usr = ref('')
const pwd = ref('')
const loading = ref(false)
const error = ref('')

async function submitLogin() {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('/api/method/login', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ usr: usr.value, pwd: pwd.value }),
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      throw new Error(data.message || 'Invalid email or password')
    }
    emit('loggedIn', usr.value)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>