<template>
  <div class="panel">
    <h3 style="margin-bottom:18px;font-size:15px;color:var(--muted);font-family:'JetBrains Mono',monospace;font-weight:400">
      {{ userEmail }}
    </h3>
    <form @submit.prevent="submitForm">
      <div class="field">
        <label>First Name</label>
        <input v-model="form.first_name" type="text" required />
      </div>
      <div class="field">
        <label>Last Name</label>
        <input v-model="form.last_name" type="text" />
      </div>
      <div class="field checkbox-row">
        <input v-model="form.enabled" type="checkbox" id="enabled" />
        <label for="enabled" style="margin:0;text-transform:none;font-weight:400;font-size:14px;color:var(--charcoal)">Enabled</label>
      </div>
      <button type="submit" class="btn btn-primary" :disabled="saving">
        {{ saving ? 'Saving…' : 'Save Changes' }}
      </button>
      <button type="button" class="btn btn-ghost" @click="$emit('cancel')">Cancel</button>
    </form>
    <p v-if="error" class="toast toast-error">{{ error }}</p>
    <p v-if="success" class="toast toast-success">Updated successfully</p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const props = defineProps({ user: { type: Object, required: true } })
const emit = defineEmits(['cancel', 'updated'])

const userEmail = props.user.email
const form = reactive({
  first_name: props.user.first_name || '',
  last_name: props.user.last_name || '',
  enabled: !!props.user.enabled,
})

const saving = ref(false)
const error = ref('')
const success = ref(false)

async function submitForm() {
  saving.value = true; error.value = ''; success.value = false
  try {
    const res = await fetch(`/api/resource/User/${encodeURIComponent(userEmail)}`, {
      method: 'PUT', credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    if (!res.ok) throw new Error((await res.json()).exception || 'Update failed')
    success.value = true
    emit('updated')
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}
</script>