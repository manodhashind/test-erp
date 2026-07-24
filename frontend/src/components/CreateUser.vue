<template>
  <div class="panel">
    <form @submit.prevent="submitForm">
      <div class="field">
        <label>Email</label>
        <input v-model="form.email" type="email" required />
      </div>
      <div class="field">
        <label>First name</label>
        <input v-model="form.first_name" type="text" required />
      </div>
      <div class="field">
        <label>Last name</label>
        <input v-model="form.last_name" type="text" />
      </div>
      <button type="submit" class="btn btn-primary" :disabled="creating">
        {{ creating ? 'Saving…' : 'Create user' }}
      </button>
    </form>
    <p v-if="error" class="toast toast-error">{{ error }}</p>
    <p v-if="success" class="toast toast-success">
      User created — password: <strong>{{ createdPassword }}</strong>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const defaultPassword = 'Constr@2026!'
const form = reactive({ email: '', first_name: '', last_name: '' })
const creating = ref(false)
const error = ref('')
const success = ref(false)
const createdPassword = ref('')

async function submitForm() {
  creating.value = true; error.value = ''; success.value = false
  try {
    const res = await fetch('/api/method/construction_management.api.create_user_with_password', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, password: defaultPassword }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.message || 'Create failed')
    createdPassword.value = data.message.password
    success.value = true
    Object.assign(form, { email: '', first_name: '', last_name: '' })
  } catch (e) {
    error.value = e.message
  } finally {
    creating.value = false
  }
}
</script>