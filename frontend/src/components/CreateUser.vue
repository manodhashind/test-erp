<template>
  <div class="panel">
    <form @submit.prevent="submitForm">
      <div class="field">
        <label>Email</label>
        <input v-model="form.email" type="email" required />
      </div>
      <div class="field">
        <label>First Name</label>
        <input v-model="form.first_name" type="text" required />
      </div>
      <div class="field">
        <label>Last Name</label>
        <input v-model="form.last_name" type="text" />
      </div>
      <div class="field checkbox-row">
        <input v-model="form.send_welcome_email" type="checkbox" id="swe" />
        <label for="swe" style="margin:0;text-transform:none;font-weight:400;font-size:14px;color:var(--charcoal)">Send welcome email</label>
      </div>
      <button type="submit" class="btn btn-primary" :disabled="creating">
        {{ creating ? 'Saving…' : 'Create User' }}
      </button>
    </form>
    <p v-if="error" class="toast toast-error">{{ error }}</p>
    <p v-if="success" class="toast toast-success">
      User created — default password is <strong>{{ defaultPassword }}</strong>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const defaultPassword = 'mano@123'

const form = reactive({
  email: '',
  first_name: '',
  last_name: '',
  send_welcome_email: false, // false so Frappe doesn't email a random reset link instead
})

const creating = ref(false)
const error = ref('')
const success = ref(false)

async function submitForm() {
  creating.value = true; error.value = ''; success.value = false
  try {
    const res = await fetch('/api/method/construction_management.api.create_user_with_password', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: form.email,
        first_name: form.first_name,
        last_name: form.last_name,
        password: defaultPassword,
      }),
    })
    if (!res.ok) throw new Error((await res.json()).message || 'Create failed')
    success.value = true
    Object.assign(form, { email: '', first_name: '', last_name: '', send_welcome_email: false })
  } catch (e) {
    error.value = e.message
  } finally {
    creating.value = false
  }
}
</script>