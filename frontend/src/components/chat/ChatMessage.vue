<template>
  <div class="chat-msg-row" :class="msg.role">
    <div class="chat-bubble" :class="msg.role">
      <div class="chat-bubble-text" v-html="rendered"></div>
      <div class="chat-bubble-footer">
        <span class="chat-time">{{ time }}</span>
        <button class="chat-copy-btn" @click="copy" :title="copied ? 'Copied!' : 'Copy'">
          {{ copied ? '✓' : '⧉' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({ msg: { type: Object, required: true } })
const copied = ref(false)

const time = computed(() =>
  new Date(props.msg.time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
)

const rendered = computed(() => {
  return props.msg.text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .split('\n')
    .map(line => (line.startsWith('• ') ? `<div class="chat-bullet">${line}</div>` : line))
    .join('<br/>')
})

function copy() {
  navigator.clipboard.writeText(props.msg.text)
  copied.value = true
  setTimeout(() => (copied.value = false), 1200)
}
</script>