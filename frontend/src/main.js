import { createApp } from 'vue'
import App from './App.vue'
import { FrappeUI } from 'frappe-ui'
import './style.css'

const app = createApp(App)
app.use(FrappeUI)
app.mount('#app')