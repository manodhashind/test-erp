# Styles Directory

## Files Overview

### Core Styles
- **`variables.css`** - Design tokens (colors, spacing, typography, shadows, z-index)
- **`breakpoints.css`** - Named responsive breakpoints for media queries
- **`responsive.css`** - Responsive utility classes and containers
- **`utilities.css`** - General utility classes

### Component Styles
- **`buttons.css`** - Button variants and styles
- **`forms.css`** - Form controls (inputs, selects, etc.)
- **`cards.css`** - Card component styles
- **`badges.css`** - Badge/status indicator styles
- **`tables.css`** - Data table styles
- **`modals.css`** - Modal dialog styles

### Main Entry
- **`index.css`** - Main stylesheet that imports all other styles

---

## Quick Start

### Using Tailwind Breakpoints

```vue
<style scoped>
.my-component {
  padding: 20px;
}

@screen mobile {
  .my-component {
    padding: 12px;
  }
}

@screen tablet {
  .my-component {
    padding: 16px;
  }
}

@screen desktop {
  .my-component {
    padding: 20px;
  }
}
</style>
```

### Available Breakpoints

**Primary (most common):**
- `mobile` (< 640px)
- `tablet` (640px - 1023px)
- `desktop` (≥ 1024px)

**Standard Tailwind:**
- `sm`, `md`, `lg`, `xl`, `2xl`

**Additional:**
- `tablet-up`, `tablet-down`, `not-desktop`
- `desktop-lg`, `desktop-xl`

See `tailwind.config.js` for configuration.

---

## Using Design Tokens

```vue
<style scoped>
.my-button {
  background: var(--color-primary);
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
}
</style>
```

See `variables.css` for all available tokens.

---

## Tailwind Utility Classes

You can also use Tailwind's responsive utilities in templates:

```vue
<template>
  <div class="p-5 mobile:p-3 tablet:p-4 desktop:p-6">
    Content
  </div>
</template>
```

## Documentation

- **Tailwind Config**: `/tailwind.config.js`
- **Responsive Guide**: `/frontend/RESPONSIVE_GUIDE.md`
- **Design System**: `/DESIGN.md` (in project root)
