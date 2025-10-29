---
name: ui-component-design
description: Create reusable, modular UI components with HTML, CSS, and JavaScript. Build component libraries with consistent styling, variants, states, and documentation. Focuses on component architecture, reusability, and maintainability.
---

# UI Component Design

Build reusable, modular UI components for scalable web applications. Create component libraries with consistent patterns, variants, and comprehensive documentation.

## Overview

This skill creates production-ready UI components:
- Reusable component architecture
- Component variants and states
- Props/configuration patterns
- Consistent naming conventions
- Accessibility built-in
- Documentation and examples
- Common UI patterns (buttons, cards, modals, inputs, etc.)

## Usage

Trigger this skill with queries like:
- "Create a reusable button component"
- "Build a card component with variants"
- "Design an input component with validation states"
- "Create a modal component library"
- "Build a navigation component system"
- "Design a data table component"

## Component Architecture

### Base Component Structure
```html
<!-- component.html -->
<div class="c-component c-component--variant" data-component="example">
  <div class="c-component__header">
    <h3 class="c-component__title">Title</h3>
  </div>
  <div class="c-component__body">
    Content
  </div>
  <div class="c-component__footer">
    Footer
  </div>
</div>
```

### Component CSS (BEM Methodology)
```css
/* component.css */
.c-component {
  /* Base styles */
  display: block;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
}

/* Variants */
.c-component--primary {
  background: var(--primary-color);
  color: white;
}

.c-component--secondary {
  background: var(--secondary-color);
}

/* Elements */
.c-component__header {
  margin-bottom: 0.5rem;
}

.c-component__title {
  font-size: 1.25rem;
  font-weight: 600;
}

/* States */
.c-component[data-state="loading"] {
  opacity: 0.6;
  pointer-events: none;
}

.c-component[data-state="error"] {
  border-color: var(--error-color);
}
```

### Component JavaScript
```javascript
// component.js
class Component {
  constructor(element, options = {}) {
    this.element = element;
    this.options = {
      variant: 'default',
      disabled: false,
      ...options
    };
    this.init();
  }

  init() {
    this.applyOptions();
    this.attachEvents();
  }

  applyOptions() {
    if (this.options.variant) {
      this.element.classList.add(`c-component--${this.options.variant}`);
    }
    if (this.options.disabled) {
      this.disable();
    }
  }

  attachEvents() {
    // Component-specific event handlers
  }

  disable() {
    this.element.setAttribute('disabled', '');
    this.element.setAttribute('aria-disabled', 'true');
  }

  enable() {
    this.element.removeAttribute('disabled');
    this.element.setAttribute('aria-disabled', 'false');
  }

  destroy() {
    // Cleanup
  }
}

// Factory function
function createComponent(selector, options) {
  const elements = document.querySelectorAll(selector);
  return Array.from(elements).map(el => new Component(el, options));
}
```

## Core Component Library

### Button Component
```html
<button class="c-btn c-btn--primary c-btn--lg" type="button">
  <span class="c-btn__icon">→</span>
  <span class="c-btn__text">Click me</span>
</button>
```

**Variants:** primary, secondary, outline, ghost, danger
**Sizes:** sm, md, lg, xl
**States:** default, hover, active, disabled, loading

### Card Component
```html
<div class="c-card c-card--elevated">
  <img class="c-card__image" src="image.jpg" alt="Description">
  <div class="c-card__content">
    <h3 class="c-card__title">Card Title</h3>
    <p class="c-card__description">Description text</p>
  </div>
  <div class="c-card__actions">
    <button class="c-btn c-btn--primary">Action</button>
  </div>
</div>
```

**Variants:** flat, elevated, outlined
**Layouts:** vertical, horizontal, media-left, media-right

### Input Component
```html
<div class="c-input" data-state="default">
  <label class="c-input__label" for="email">Email</label>
  <div class="c-input__wrapper">
    <input
      class="c-input__field"
      type="email"
      id="email"
      placeholder="you@example.com"
      aria-describedby="email-help">
    <span class="c-input__icon">@</span>
  </div>
  <span class="c-input__help" id="email-help">Enter your email address</span>
  <span class="c-input__error" role="alert">Invalid email format</span>
</div>
```

**States:** default, focus, success, error, disabled
**Types:** text, email, password, number, textarea, select

### Modal Component
```html
<div class="c-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <div class="c-modal__overlay" data-dismiss="modal"></div>
  <div class="c-modal__container">
    <div class="c-modal__header">
      <h2 class="c-modal__title" id="modal-title">Modal Title</h2>
      <button class="c-modal__close" aria-label="Close modal">&times;</button>
    </div>
    <div class="c-modal__body">
      Modal content
    </div>
    <div class="c-modal__footer">
      <button class="c-btn c-btn--secondary">Cancel</button>
      <button class="c-btn c-btn--primary">Confirm</button>
    </div>
  </div>
</div>
```

**Variants:** small, medium, large, fullscreen
**Features:** backdrop click, escape key, focus trap, scroll lock

### Navigation Component
```html
<nav class="c-nav c-nav--horizontal" role="navigation">
  <a class="c-nav__item c-nav__item--active" href="#" aria-current="page">Home</a>
  <a class="c-nav__item" href="#">About</a>
  <div class="c-nav__item c-nav__item--dropdown">
    <button class="c-nav__toggle" aria-expanded="false">Services</button>
    <div class="c-nav__submenu">
      <a class="c-nav__subitem" href="#">Service 1</a>
      <a class="c-nav__subitem" href="#">Service 2</a>
    </div>
  </div>
</nav>
```

**Layouts:** horizontal, vertical, sidebar
**Features:** dropdowns, mobile toggle, active states

## Component Documentation Template

```markdown
# Component Name

## Description
Brief description of what the component does.

## Usage
\`\`\`html
<!-- Basic example -->
\`\`\`

## Props/Options
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | string | 'default' | Visual variant |
| size | string | 'md' | Size option |
| disabled | boolean | false | Disable state |

## Variants
- default
- primary
- secondary

## States
- default
- hover
- active
- disabled
- loading

## Accessibility
- ARIA attributes used
- Keyboard navigation support
- Screen reader considerations

## Examples
[Multiple usage examples]

## Browser Support
Modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
```

## Bundled Resources

### Scripts

**`scripts/component_generator.py`** - Generates component boilerplate
- Creates HTML, CSS, and JS files
- Applies naming conventions
- Generates documentation template

Usage:
```bash
python scripts/component_generator.py ButtonGroup
```

**`scripts/component_validator.py`** - Validates component structure
- Checks BEM naming conventions
- Validates accessibility attributes
- Ensures documentation exists

### References

**`references/bem_methodology.md`** - BEM naming convention guide and best practices

**`references/component_patterns.md`** - Common UI component patterns and implementations

**`references/accessibility_components.md`** - Building accessible components with ARIA

**`references/css_architecture.md`** - CSS organization strategies for component libraries

## Best Practices

**Naming Conventions**
- Use BEM methodology: `.c-component__element--modifier`
- Prefix components with `c-` for clarity
- Use semantic, descriptive names
- Keep names consistent across HTML, CSS, JS

**Component Structure**
- Single responsibility principle
- Composable and reusable
- Configuration over modification
- Consistent API across components

**Styling**
- Use CSS custom properties for theming
- Avoid global styles within components
- Scope styles to component
- Support variants and states

**JavaScript**
- Progressive enhancement
- Event delegation where appropriate
- Clean up on destroy
- Consistent initialization API

**Accessibility**
- Include ARIA attributes
- Keyboard navigation support
- Focus management
- Screen reader announcements

**Documentation**
- Document all props/options
- Provide usage examples
- List variants and states
- Note browser support

## Component Checklist

- [ ] HTML structure follows BEM
- [ ] CSS scoped to component
- [ ] JavaScript initialization works
- [ ] All variants implemented
- [ ] All states styled
- [ ] Accessibility attributes added
- [ ] Keyboard navigation works
- [ ] Responsive design applied
- [ ] Documentation created
- [ ] Examples provided
- [ ] Browser testing complete

## When to Use This Skill

Use ui-component-design when:
- Building component libraries
- Creating reusable UI patterns
- Need consistent design implementation
- Scaling web applications
- Team collaboration requires shared components

Choose other skills for:
- Single-page designs (use html-static-design)
- Layout-focused work (use css-layout-builder)
- Adding interactions (use javascript-interactive-design)
- Complete design systems (use design-system-builder)

## Component Library Structure

```
components/
├── buttons/
│   ├── button.html
│   ├── button.css
│   ├── button.js
│   └── button.md
├── cards/
│   ├── card.html
│   ├── card.css
│   ├── card.js
│   └── card.md
├── forms/
│   ├── input.html
│   ├── input.css
│   ├── input.js
│   └── input.md
└── index.html (component showcase)
```
