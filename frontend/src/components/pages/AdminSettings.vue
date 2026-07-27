<template>
  <div>
    <div class="settings-grid">
      <div class="panel settings-panel">
        <div class="settings-panel-header">
          <div>
            <h3>Color palette</h3>
            <p>Choose a primary color for the application</p>
          </div>
          <button class="btn btn-ghost btn-sm" @click="reset">Reset</button>
        </div>

        <div class="section-label">Presets</div>
        <div class="color-presets">
          <button
            v-for="preset in presets"
            :key="preset.hex"
            class="color-chip"
            :class="{ active: state.primaryColor === preset.hex }"
            @click="setPrimaryColor(preset.hex)"
          >
            <span class="color-dot" :style="{ background: preset.hex }"></span>
            {{ preset.label }}
          </button>
        </div>

        <div class="section-label">Custom color</div>
        <div class="custom-color-row">
          <input type="color" v-model="customHex" />
          <input type="text" v-model="customHex" />
          <button class="btn btn-primary btn-sm" @click="setPrimaryColor(customHex)">Apply</button>
        </div>

        <div class="section-label">Live preview</div>
        <div class="preview-box" style="margin-bottom:10px">
          <button class="btn btn-primary btn-sm">Button</button>
          <span class="pill pill-on">Active</span>
          <span style="font-size:13px">Text</span>
        </div>
        <div class="preview-box dark-preview">
          <button class="btn btn-primary btn-sm">Button</button>
          <span class="pill pill-on">Active</span>
          <span style="font-size:13px; color:#E7E9EE">Text</span>
        </div>
      </div>

      <div class="panel settings-panel">
        <div class="settings-panel-header">
          <div>
            <h3>UI preferences</h3>
            <p>Appearance and animation speed</p>
          </div>
        </div>

        <div class="section-label">Appearance</div>
        <div class="option-cards">
          <div class="option-card" :class="{ active: !state.darkMode }" @click="setDarkMode(false)">Light</div>
          <div class="option-card" :class="{ active: state.darkMode }" @click="setDarkMode(true)">Dark</div>
        </div>

        <div class="section-label">Accent / text color</div>
        <div class="color-presets">
          <button
            v-for="preset in accentPresets"
            :key="preset.hex"
            class="color-chip"
            :class="{ active: state.accentColor === preset.hex }"
            @click="setAccentColor(preset.hex)"
          >
            <span class="color-dot" :style="{ background: preset.hex }"></span>
            {{ preset.label }}
          </button>
        </div>
        <div class="custom-color-row">
          <input type="color" v-model="customAccentHex" />
          <input type="text" v-model="customAccentHex" />
          <button class="btn btn-primary btn-sm" @click="setAccentColor(customAccentHex)">Apply</button>
        </div>

        <div class="section-label">Animation speed</div>
        <div class="option-cards">
          <div
            v-for="speed in speeds"
            :key="speed.value"
            class="option-card"
            :class="{ active: state.animationSpeed === speed.value }"
            @click="setAnimationSpeed(speed.value)"
          >
            {{ speed.label }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useTheme } from '../../composables/useTheme'

// Destructure all theme helpers used by the template
const { state, setPrimaryColor, setAccentColor, setSidebarStyle, setDarkMode, setAnimationSpeed, reset } = useTheme()

// Local refs for the color inputs (keep in sync with the shared theme state)
const customHex = ref(state.value.primaryColor)
const customAccentHex = ref(state.value.accentColor)

// Keep local inputs updated if the shared state changes elsewhere
watch(() => state.value.primaryColor, (v) => { if (v !== customHex.value) customHex.value = v })
watch(() => state.value.accentColor, (v) => { if (v !== customAccentHex.value) customAccentHex.value = v })

const accentPresets = [
  { label: 'Pink', hex: '#CE5BA9' },
  { label: 'Amber', hex: '#D98C2B' },
  { label: 'Teal', hex: '#0F6E56' },
  { label: 'Blue', hex: '#185FA5' },
  { label: 'Rose', hex: '#993556' },
]

const presets = [
  { label: 'Purple', hex: '#6742CF' },
  { label: 'Navy', hex: '#1B2A41' },
  { label: 'Teal', hex: '#0F6E56' },
  { label: 'Forest', hex: '#27500A' },
  { label: 'Ocean', hex: '#042C53' },
  { label: 'Blue', hex: '#185FA5' },
  { label: 'Amber', hex: '#854F0B' },
  { label: 'Rose', hex: '#993556' },
  { label: 'Slate', hex: '#444441' },
]

const speeds = [
  { label: 'None', value: 'none' },
  { label: 'Fast', value: 'fast' },
  { label: 'Normal', value: 'normal' },
  { label: 'Slow', value: 'slow' },
]
</script>