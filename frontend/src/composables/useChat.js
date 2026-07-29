import { ref } from 'vue'

export function useChat() {
  const messages = ref([])
  const context = ref({ last_user: null, pending: null })
  const loading = ref(false)

  function pushMessage(role, text) {
    messages.value.push({
      id: Date.now() + Math.random(),
      role,
      text,
      time: new Date(),
    })
  }

  async function sendMessage(text) {
    if (!text.trim()) return
    pushMessage('user', text)
    loading.value = true
    try {
      const res = await fetch('/api/method/construction_management.llm_chat.process_chat_message_llm', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          context: JSON.stringify(context.value),
        }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.message || 'Something went wrong')
      const result = data.message
      context.value = result.context || { last_user: null, pending: null }
      pushMessage('assistant', result.reply)
    } catch (e) {
      pushMessage('assistant', `Sorry, something went wrong: ${e.message}`)
    } finally {
      loading.value = false
    }
  }

  function clearConversation() {
    messages.value = []
    context.value = { last_user: null, pending: null }
  }

  return { messages, loading, sendMessage, clearConversation }
}