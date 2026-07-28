<template>
  <div class="login-screen">
    <div class="login-bg"></div>
    <div class="login-orb login-orb-1"></div>
    <div class="login-orb login-orb-2"></div>

    <div class="login-panel">
      <div class="login-mark">🏗</div>
      <span class="brand-sub" style="color:var(--amber)">Construction Management</span>
      <h1 style="margin:6px 0 28px">Site Register</h1>

      <form @submit.prevent="submitLogin">
        <div class="field login-field" style="animation-delay:0.05s">
          <label>Email</label>
          <input v-model="usr" type="text" required autofocus />
        </div>
        <div class="field login-field" style="animation-delay:0.12s">
          <label>Password</label>
          <input v-model="pwd" type="password" required />
        </div>
        <button
          type="submit"
          class="btn btn-primary login-submit"
          style="width:100%; animation-delay:0.2s"
          :disabled="loading"
        >
          <span v-if="!loading">Sign in</span>
          <span v-else class="login-spinner"></span>
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