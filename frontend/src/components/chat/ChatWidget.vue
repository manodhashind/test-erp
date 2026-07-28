<template>
  <div>
    <button class="chat-fab" @click="open = !open" :aria-label="open ? 'Close chat' : 'Open AI assistant'">
      {{ open ? '✕' : '💬' }}
    </button>

    <transition name="chat-pop">
      <div v-if="open" class="chat-panel">
        <div class="chat-header">
          <div>
            <div class="chat-title">Construction AI Assistant</div>
            <div class="chat-subtitle">User Management Assistant</div>
          </div>
          <button class="btn-danger-text" style="padding:4px 8px" @click="clearConversation">Clear</button>
        </div>

        <div class="chat-messages" ref="scrollEl">
          <div v-if="!messages.length" class="chat-welcome">
            <p style="font-weight:600; margin-bottom:8px">👋 Hi, I'm your assistant</p>
            <p style="color:var(--muted); font-size:13px; margin-bottom:16px">
              Ask me to view, search, create, edit, or manage users.
            </p>
            <div class="chat-suggestions">
              <button v-for="s in suggestions" :key="s" class="chat-suggestion" @click="send(s)">{{ s }}</button>
            </div>
          </div>

          <ChatMessage v-for="m in messages" :key="m.id" :msg="m" />

          <div v-if="loading" class="chat-msg-row assistant">
            <div class="chat-bubble assistant">
              <span class="chat-typing"><span></span><span></span><span></span></span>
            </div>
          </div>
        </div>

        <div class="chat-input-row">
          <textarea
            v-model="draft"
            placeholder="Ask me anything about users…"
            rows="1"
            @keydown.enter.exact.prevent="submit"
          ></textarea>
          <button class="btn btn-primary btn-sm" :disabled="loading || !draft.trim()" @click="submit">Send</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { useChat } from '../../composables/useChat'
import ChatMessage from './ChatMessage.vue'

const open = ref(false)
const draft = ref('')
const scrollEl = ref(null)
const { messages, loading, sendMessage, clearConversation } = useChat()

const suggestions = [
  'Show active users',
  'User statistics',
  'Create a user',
  'Find Mano',
]

function submit() {
  const text = draft.value
  draft.value = ''
  send(text)
}

function send(text) {
  sendMessage(text)
}

watch([messages, loading], async () => {
  await nextTick()
  if (scrollEl.value) scrollEl.value.scrollTop = scrollEl.value.scrollHeight
}, { deep: true })
</script>