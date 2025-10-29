---
name: css-layout-builder
description: Advanced CSS layout specialist for building complex, responsive layouts using CSS Grid, Flexbox, and modern positioning techniques. Handles multi-column layouts, responsive grids, container queries, and advanced layout patterns.
---

# CSS Layout Builder

Expert skill for creating sophisticated, responsive CSS layouts using modern techniques. Master CSS Grid, Flexbox, container queries, and advanced positioning patterns.

## Overview

This skill specializes in complex layout challenges:
- Multi-column responsive layouts
- CSS Grid systems and named areas
- Advanced Flexbox patterns
- Container queries for component-based responsive design
- Holy Grail, Sidebar, Dashboard layouts
- Responsive navigation patterns
- Complex grid systems

## Usage

Trigger this skill with queries like:
- "Build a responsive grid layout with [specifications]"
- "Create a sidebar layout with CSS Grid"
- "Design a dashboard layout"
- "Build a responsive navigation system"
- "Create a masonry-style grid"
- "Implement container queries for responsive components"

### Layout Design Process

**Step 1: Requirements Analysis**
- Identify layout structure (sidebar, multi-column, grid, etc.)
- Determine responsive breakpoints
- Understand content hierarchy
- Clarify interaction patterns

**Step 2: Layout Strategy**
- Choose appropriate technique (Grid vs Flexbox)
- Plan responsive behavior
- Define breakpoint strategy
- Consider mobile-first approach

**Step 3: Implementation**
- Build base layout structure
- Add responsive adjustments
- Optimize for performance
- Test across viewports

## Core Layout Patterns

### Holy Grail Layout
Three-column layout with header and footer, where side columns have fixed width and center column is fluid.

```css
.holy-grail {
  display: grid;
  grid-template-areas:
    "header header header"
    "left main right"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header { grid-area: header; }
.left { grid-area: left; }
.main { grid-area: main; }
.right { grid-area: right; }
.footer { grid-area: footer; }

/* Responsive */
@media (max-width: 768px) {
  .holy-grail {
    grid-template-areas:
      "header"
      "main"
      "left"
      "right"
      "footer";
    grid-template-columns: 1fr;
  }
}
```

### Sidebar Layout
Content area with collapsible sidebar.

```css
.layout-with-sidebar {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
}

.sidebar {
  position: sticky;
  top: 2rem;
  height: fit-content;
}

/* Collapsed sidebar */
.layout-with-sidebar[data-sidebar="collapsed"] {
  grid-template-columns: 60px 1fr;
}

@media (max-width: 1024px) {
  .layout-with-sidebar {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: fixed;
    transform: translateX(-100%);
    transition: transform 0.3s;
  }

  .sidebar[data-open="true"] {
    transform: translateX(0);
  }
}
```

### Dashboard Grid
Flexible dashboard with resizable panels.

```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem;
  padding: 1.5rem;
}

.panel-large {
  grid-column: span 8;
}

.panel-medium {
  grid-column: span 6;
}

.panel-small {
  grid-column: span 4;
}

@media (max-width: 768px) {
  .panel-large,
  .panel-medium,
  .panel-small {
    grid-column: span 12;
  }
}
```

### Masonry Layout (CSS Grid)
Pinterest-style masonry layout.

```css
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-auto-rows: 10px;
  gap: 1rem;
}

.masonry-item {
  /* Items span rows based on content height */
  grid-row-end: span var(--row-span);
}
```

### Card Grid
Responsive card grid with auto-fit.

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

/* With maximum columns */
.card-grid-limited {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  max-width: 1400px;
  margin: 0 auto;
}

@supports (width: min(300px, 100%)) {
  .card-grid {
    grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  }
}
```

## Advanced Techniques

### Container Queries
Component-responsive design independent of viewport.

```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card {
  display: block;
}

@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 300px 1fr;
  }
}
```

### Subgrid
Align nested grid items with parent grid.

```css
.main-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}

.nested-grid {
  display: grid;
  grid-column: span 2;
  grid-template-columns: subgrid;
  gap: 1rem;
}
```

### Sticky Headers/Footers
Fixed positioning within scroll containers.

```css
.scroll-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.sticky-header {
  position: sticky;
  top: 0;
  z-index: 10;
  background: white;
}

.scrollable-content {
  flex: 1;
  overflow-y: auto;
}

.sticky-footer {
  position: sticky;
  bottom: 0;
  z-index: 10;
  background: white;
}
```

### Responsive Navigation
Mobile-first navigation patterns.

```css
/* Mobile: Hamburger menu */
.nav {
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  width: 250px;
  height: 100vh;
  transform: translateX(-100%);
  transition: transform 0.3s;
}

.nav[data-open="true"] {
  transform: translateX(0);
}

/* Tablet: Horizontal */
@media (min-width: 768px) {
  .nav {
    position: static;
    flex-direction: row;
    width: auto;
    height: auto;
    transform: none;
  }
}

/* Desktop: Full width with dropdowns */
@media (min-width: 1024px) {
  .nav {
    justify-content: space-between;
  }

  .nav-dropdown {
    position: absolute;
    display: none;
  }

  .nav-item:hover .nav-dropdown {
    display: block;
  }
}
```

## Bundled Resources

### Scripts

**`scripts/layout_analyzer.py`** - Analyzes CSS layout complexity and suggests optimizations
- Detects layout methods used (Grid, Flexbox, Float)
- Identifies responsive breakpoints
- Checks for browser compatibility issues
- Suggests modern alternatives

Usage:
```bash
python scripts/layout_analyzer.py styles.css
```

**`scripts/breakpoint_generator.py`** - Generates responsive breakpoint templates
- Creates standard breakpoint boilerplate
- Generates mobile-first media queries
- Outputs container query templates

Usage:
```bash
python scripts/breakpoint_generator.py --output breakpoints.css
```

### References

**`references/grid_complete_guide.md`** - Comprehensive CSS Grid guide with all properties and patterns

**`references/flexbox_complete_guide.md`** - Complete Flexbox reference with alignment patterns and use cases

**`references/responsive_patterns.md`** - Collection of responsive design patterns and breakpoint strategies

**`references/container_queries_guide.md`** - Modern container queries guide for component-based responsive design

**`references/layout_debugging.md`** - Techniques for debugging layout issues and common pitfalls

## Responsive Strategy

### Mobile-First Approach
```css
/* Base styles for mobile */
.container {
  display: block;
  padding: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    padding: 2rem;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    grid-template-columns: repeat(3, 1fr);
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### Fluid Typography with Clamp
```css
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
}

.container {
  width: clamp(300px, 90%, 1200px);
  padding: clamp(1rem, 3vw, 3rem);
}
```

### Responsive Spacing
```css
:root {
  --spacing-xs: clamp(0.5rem, 1vw, 0.75rem);
  --spacing-sm: clamp(0.75rem, 2vw, 1rem);
  --spacing-md: clamp(1rem, 3vw, 1.5rem);
  --spacing-lg: clamp(1.5rem, 4vw, 2rem);
  --spacing-xl: clamp(2rem, 5vw, 3rem);
}
```

## Best Practices

**CSS Grid**
- Use for two-dimensional layouts
- Leverage named grid areas for clarity
- Use auto-fit/auto-fill for responsive grids
- Consider subgrid for nested grids
- Use gap instead of margins between grid items

**Flexbox**
- Use for one-dimensional layouts
- Best for navigation, toolbars, card rows
- Use flex-wrap for responsive rows
- Leverage flex-grow/shrink for flexible items
- Combine with gap for consistent spacing

**General Layout**
- Start mobile-first
- Use CSS custom properties for breakpoints
- Minimize media queries with fluid techniques
- Consider container queries for components
- Test on real devices, not just browser resize
- Use semantic HTML with layout CSS

**Performance**
- Avoid nested calc() functions
- Minimize layout recalculations
- Use transform for animations, not positioning
- Consider will-change for animated elements
- Optimize for paint and composite

## Common Patterns

### Centered Container
```css
.container {
  width: min(90%, 1200px);
  margin-inline: auto;
  padding-inline: 1rem;
}
```

### Full Bleed Sections
```css
.full-bleed {
  width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
}
```

### Aspect Ratio Containers
```css
.video-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}

.square {
  aspect-ratio: 1;
}
```

### Equal Height Columns
```css
.equal-height-columns {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-auto-rows: 1fr;
}
```

## Troubleshooting

**Grid items not aligning**
- Check grid-template-columns definition
- Verify grid-area names match
- Ensure grid-column/row spans are correct
- Check for conflicting positioning

**Flexbox items overflowing**
- Add flex-wrap: wrap
- Set min-width: 0 on flex items
- Check flex-shrink values
- Verify parent width

**Responsive layout breaking**
- Test breakpoints at actual device widths
- Check for fixed widths instead of max-width
- Verify overflow handling
- Test with long content

**Performance issues**
- Avoid animating layout properties
- Use transform/opacity for animations
- Check for excessive nesting
- Minimize repaints with containment

## When to Use This Skill

Use css-layout-builder when:
- Building complex multi-section layouts
- Creating responsive grid systems
- Implementing dashboard or admin layouts
- Need advanced positioning patterns
- Building component-based responsive designs
- Optimizing layout performance

Choose other skills for:
- Simple static pages (use html-static-design)
- Adding interactions (use javascript-interactive-design)
- Component libraries (use ui-component-design)
- Complete design systems (use design-system-builder)

## Browser Support

Modern features support:
- **CSS Grid**: All modern browsers (IE11 with -ms- prefix)
- **Flexbox**: All modern browsers (IE10+ with prefixes)
- **Container Queries**: Chrome 105+, Safari 16+, Firefox 110+
- **Subgrid**: Chrome 117+, Safari 16+, Firefox 71+
- **aspect-ratio**: Chrome 88+, Safari 15+, Firefox 89+

Use feature queries for progressive enhancement:
```css
@supports (container-type: inline-size) {
  /* Container query styles */
}
```
