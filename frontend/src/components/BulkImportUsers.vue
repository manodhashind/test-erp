<template>
  <div class="panel" style="max-width:720px">
    <h3 style="margin-bottom:6px">Bulk import users</h3>
    <p style="color:var(--muted); font-size:13px; margin-bottom:20px">
      Upload an Excel file with columns: <code>email</code>, <code>first_name</code>, <code>last_name</code>
    </p>

    <div class="dropzone" @click="fileInput.click()" @dragover.prevent @drop.prevent="onDrop">
      <input ref="fileInput" type="file" accept=".xlsx,.xls,.csv" style="display:none" @change="onFileSelect" />
      <span v-if="!fileName">📄 Click or drop an Excel file here</span>
      <span v-else>✓ {{ fileName }} — {{ rows.length }} row(s) found</span>
    </div>

    <div v-if="rows.length" class="preview-table-wrap">
      <table class="data-table" style="margin-top:16px">
        <thead>
          <tr><th>Email</th><th>First name</th><th>Last name</th><th>Status</th></tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in rows" :key="i">
            <td class="mono">{{ row.email }}</td>
            <td>{{ row.first_name }}</td>
            <td>{{ row.last_name || '—' }}</td>
            <td>
              <span v-if="!row.status" class="pill" style="background:var(--bg); color:var(--muted)">Pending</span>
              <span v-else-if="row.status === 'success'" class="pill pill-on">Created</span>
              <span v-else class="pill pill-off" :title="row.errorMsg">Failed</span>
            </td>
          </tr>
        </tbody>
      </table>

      <div style="display:flex; align-items:center; gap:12px; margin-top:16px">
        <button class="btn btn-primary" :disabled="importing || !pendingCount" @click="importAll">
          {{ importing ? `Importing… (${doneCount}/${rows.length})` : `Import ${pendingCount} user(s)` }}
        </button>
        <button class="btn btn-ghost" @click="reset">Clear</button>
      </div>

      <p v-if="doneCount === rows.length && rows.length" class="toast toast-success">
        Done — {{ successCount }} created, {{ failCount }} failed.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import * as XLSX from 'xlsx'

const defaultPassword = 'Constr@2026!'
const fileInput = ref(null)
const fileName = ref('')
const rows = ref([])
const importing = ref(false)

const pendingCount = computed(() => rows.value.filter(r => !r.status).length)
const successCount = computed(() => rows.value.filter(r => r.status === 'success').length)
const failCount = computed(() => rows.value.filter(r => r.status === 'error').length)
const doneCount = computed(() => rows.value.filter(r => r.status).length)

function onDrop(e) {
  const file = e.dataTransfer.files[0]
  if (file) parseFile(file)
}

function onFileSelect(e) {
  const file = e.target.files[0]
  if (file) parseFile(file)
}

function parseFile(file) {
  fileName.value = file.name
  const reader = new FileReader()
  reader.onload = (e) => {
    const data = new Uint8Array(e.target.result)
    const workbook = XLSX.read(data, { type: 'array' })
    const sheet = workbook.Sheets[workbook.SheetNames[0]]
    const json = XLSX.utils.sheet_to_json(sheet, { defval: '' })

    rows.value = json
      .map(r => ({
        email: (r.email || r.Email || '').toString().trim(),
        first_name: (r.first_name || r['First Name'] || r.firstname || '').toString().trim(),
        last_name: (r.last_name || r['Last Name'] || r.lastname || '').toString().trim(),
        status: null,
        errorMsg: '',
      }))
      .filter(r => r.email && r.first_name)
  }
  reader.readAsArrayBuffer(file)
}

async function importAll() {
  importing.value = true
  for (const row of rows.value) {
    if (row.status) continue
    try {
      const res = await fetch('/api/method/construction_management.api.create_user_with_password', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: row.email,
          first_name: row.first_name,
          last_name: row.last_name,
          password: defaultPassword,
        }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.message || 'Failed')
      row.status = 'success'
    } catch (e) {
      row.status = 'error'
      row.errorMsg = e.message
    }
  }
  importing.value = false
}

function reset() {
  fileName.value = ''
  rows.value = []
  if (fileInput.value) fileInput.value.value = ''
}
</script>