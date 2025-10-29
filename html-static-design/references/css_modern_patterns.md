# Modern CSS Patterns

Modern CSS techniques for flexible, maintainable, and efficient styling.

## CSS Custom Properties (Variables)

Define reusable values throughout your stylesheet.

### Basic Usage
```css
:root {
  --primary-color: #3498db;
  --secondary-color: #2ecc71;
  --font-main: 'Segoe UI', Tahoma, sans-serif;
  --spacing-unit: 1rem;
  --border-radius: 4px;
}

.button {
  background-color: var(--primary-color);
  font-family: var(--font-main);
  padding: var(--spacing-unit);
  border-radius: var(--border-radius);
}
```

### Theme Switching
```css
:root {
  --bg-color: #ffffff;
  --text-color: #333333;
}

[data-theme="dark"] {
  --bg-color: #1a1a1a;
  --text-color: #f0f0f0;
}

body {
  background-color: var(--bg-color);
  color: var(--text-color);
}
```

## CSS Grid Layout

Powerful two-dimensional layout system.

### Basic Grid
```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}
```

### Responsive Grid (Auto-fit)
```css
.responsive-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}
```

### Named Grid Areas
```css
.layout {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main main"
    "footer footer footer";
  grid-template-columns: 250px 1fr 1fr;
  gap: 1rem;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

### Full-Height Layout
```css
.app {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}
```

## Flexbox

One-dimensional layout for flexible alignment.

### Centering
```css
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

### Space Between
```css
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

### Flexible Cards
```css
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.card {
  flex: 1 1 300px; /* grow, shrink, base width */
}
```

## Modern Responsive Design

### Container Queries (New!)
```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: flex;
  }
}
```

### Clamp for Fluid Typography
```css
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
  /* min, preferred, max */
}

.container {
  width: clamp(300px, 90%, 1200px);
  margin: 0 auto;
}
```

### Modern Media Queries
```css
/* Mobile first */
.element { /* mobile styles */ }

@media (min-width: 768px) {
  .element { /* tablet styles */ }
}

@media (min-width: 1024px) {
  .element { /* desktop styles */ }
}
```

## Aspect Ratio

Maintain aspect ratios without padding hacks.

```css
.video-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}

.square {
  aspect-ratio: 1;
}
```

## Modern Selectors

### :is() Pseudo-class
```css
/* Instead of: */
header a:hover,
footer a:hover,
nav a:hover { }

/* Use: */
:is(header, footer, nav) a:hover { }
```

### :where() Pseudo-class (No specificity)
```css
:where(h1, h2, h3, h4) {
  margin-top: 0;
}
```

### :has() Parent Selector
```css
/* Style card if it contains an image */
.card:has(img) {
  padding: 0;
}

/* Style form with invalid input */
form:has(input:invalid) {
  border-color: red;
}
```

## Scroll Behavior

### Smooth Scrolling
```css
html {
  scroll-behavior: smooth;
}
```

### Scroll Snap
```css
.scroll-container {
  scroll-snap-type: x mandatory;
  overflow-x: scroll;
}

.scroll-item {
  scroll-snap-align: center;
}
```

## Modern Effects

### Backdrop Filter
```css
.glass-effect {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}
```

### CSS Filters
```css
.image {
  filter: grayscale(50%) brightness(1.1);
}

.image:hover {
  filter: none;
  transition: filter 0.3s;
}
```

### Clip Path
```css
.diagonal-section {
  clip-path: polygon(0 0, 100% 0, 100% 90%, 0 100%);
}
```

## Grid + Flexbox Combo

Use both together for powerful layouts.

```css
.page-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
}

.header {
  grid-column: 1 / -1; /* span all columns */
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

## Logical Properties

Direction-agnostic properties for internationalization.

```css
/* Instead of: */
margin-left: 1rem;
padding-right: 2rem;

/* Use: */
margin-inline-start: 1rem;
padding-inline-end: 2rem;
```

## Custom Scrollbars

```css
.container::-webkit-scrollbar {
  width: 8px;
}

.container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}
```

## Performance Best Practices

### Use Transform for Animations
```css
/* Good - GPU accelerated */
.element {
  transform: translateX(100px);
  transition: transform 0.3s;
}

/* Avoid - causes reflow */
.element {
  left: 100px;
  transition: left 0.3s;
}
```

### Will-change Hint
```css
.animate-me {
  will-change: transform;
}

.animate-me:hover {
  transform: scale(1.1);
}
```

### Content-visibility
```css
.off-screen-section {
  content-visibility: auto;
}
```

## Modern Resets

```css
/* Modern CSS Reset */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  min-height: 100vh;
  line-height: 1.6;
}

img, picture, video {
  max-width: 100%;
  display: block;
}

input, button, textarea, select {
  font: inherit;
}
```

## Utility-First Patterns

Create reusable utility classes.

```css
.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.gap-4 { gap: 1rem; }
.p-4 { padding: 1rem; }
.m-0 { margin: 0; }
.text-center { text-align: center; }
```

## Component Patterns

### Card Component
```css
.card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s;
}

.card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
```

### Button Component
```css
.button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  background: var(--primary-color);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.button:hover {
  background: var(--primary-color-dark);
}
```

## Browser Support

Check compatibility at [caniuse.com](https://caniuse.com)

Most modern features work in:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
