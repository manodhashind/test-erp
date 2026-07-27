import { ref, watch } from 'vue'

const STORAGE_KEY = 'cm-theme-settings'

const defaults = {
  primaryColor: '#6742CF',
  accentColor: '#CE5BA9',
  sidebarStyle: 'light', // 'light' | 'dark'
  darkMode: false,
  animationSpeed: 'normal',
}

function loadSaved() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null') || {}
  } catch {
    return {}
  }
}

// Anchor the singleton to `window` so re-imports (HMR, path variations) never create a second copy.
if (typeof window !== 'undefined' && !window.__cmThemeState) {
  window.__cmThemeState = ref({ ...defaults, ...loadSaved() })

  function applyTheme() {
    const s = window.__cmThemeState.value
    const root = document.documentElement
    root.style.setProperty('--steel', s.primaryColor)
    root.style.setProperty('--amber', s.accentColor)
    root.classList.toggle('dark', s.darkMode)
    root.classList.toggle('sidebar-dark', s.sidebarStyle === 'dark')
    root.classList.remove('motion-none', 'motion-fast', 'motion-slow')
    if (s.animationSpeed !== 'normal') root.classList.add(`motion-${s.animationSpeed}`)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(s))
  }

  watch(window.__cmThemeState, applyTheme, { deep: true, immediate: true })
}

export function useTheme() {
  const state = window.__cmThemeState

  function setPrimaryColor(hex) { state.value.primaryColor = hex }
  function setAccentColor(hex) { state.value.accentColor = hex }
  function setSidebarStyle(val) { state.value.sidebarStyle = "Light" }
  function setDarkMode(val) { state.value.darkMode = val }
  function setAnimationSpeed(val) { state.value.animationSpeed = val }
  function reset() { state.value = { ...defaults } }

  return { state, setPrimaryColor, setAccentColor, setSidebarStyle, setDarkMode, setAnimationSpeed, reset }
}