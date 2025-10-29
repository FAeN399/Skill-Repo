# Web Accessibility Checklist

Comprehensive checklist for creating accessible static websites.

## WCAG 2.1 Compliance Levels

- **Level A**: Minimum accessibility (must have)
- **Level AA**: Recommended standard (should have)
- **Level AAA**: Enhanced accessibility (nice to have)

**Target: WCAG 2.1 Level AA compliance**

## Perceivable

### Text Alternatives

- [ ] All images have meaningful `alt` attributes
- [ ] Decorative images use `alt=""` or CSS backgrounds
- [ ] Icons paired with text or have `aria-label`
- [ ] Form inputs have associated `<label>` elements
- [ ] Complex images (charts, diagrams) have detailed descriptions

```html
<!-- Good examples -->
<img src="logo.png" alt="Company Name">
<img src="decorative.png" alt="" role="presentation">
<button aria-label="Close menu"><span aria-hidden="true">×</span></button>
```

### Color Contrast

- [ ] Text contrast ratio ≥ 4.5:1 for normal text (WCAG AA)
- [ ] Text contrast ratio ≥ 3:1 for large text (18pt+ or 14pt+ bold)
- [ ] Interactive elements have 3:1 contrast against background
- [ ] Don't rely solely on color to convey information

**Testing Tools:**
- Chrome DevTools Contrast Checker
- WebAIM Contrast Checker
- Contrast Ratio by Lea Verou

### Adaptable Content

- [ ] Semantic HTML used throughout
- [ ] Proper heading hierarchy (h1 → h2 → h3)
- [ ] Lists use `<ul>`, `<ol>`, or `<dl>` appropriately
- [ ] Tables use `<th>`, `scope`, and `<caption>`
- [ ] Reading order makes sense without CSS

## Operable

### Keyboard Navigation

- [ ] All interactive elements keyboard accessible
- [ ] Tab order is logical
- [ ] Focus indicators visible (no `outline: none` without alternative)
- [ ] Skip links provided for main content
- [ ] No keyboard traps

```css
/* Good focus styles */
:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none; /* Remove for mouse users */
}

:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}
```

### Navigation

- [ ] Multiple ways to navigate (menu, search, sitemap)
- [ ] Current page indicated in navigation
- [ ] Breadcrumbs for hierarchical sites
- [ ] Descriptive page titles (`<title>`)
- [ ] Consistent navigation across pages

### Forms

- [ ] Labels associated with inputs
- [ ] Required fields indicated
- [ ] Error messages clear and specific
- [ ] Autocomplete attributes used appropriately
- [ ] Group related inputs with `<fieldset>` and `<legend>`

```html
<!-- Accessible form example -->
<form>
  <fieldset>
    <legend>Personal Information</legend>

    <label for="name">Name <span aria-label="required">*</span></label>
    <input type="text" id="name" name="name" required
           autocomplete="name" aria-required="true">

    <label for="email">Email</label>
    <input type="email" id="email" name="email"
           autocomplete="email" aria-describedby="email-help">
    <span id="email-help">We'll never share your email</span>
  </fieldset>
</form>
```

## Understandable

### Readable

- [ ] Language specified (`<html lang="en">`)
- [ ] Language changes marked (`<span lang="es">`)
- [ ] Text is readable and understandable
- [ ] Avoid jargon or provide definitions
- [ ] Abbreviations expanded on first use

```html
<html lang="en">
  <p>Welcome! <span lang="fr">Bienvenue!</span></p>
  <p>The <abbr title="World Wide Web">WWW</abbr> is accessible.</p>
</html>
```

### Predictable

- [ ] Navigation consistent across pages
- [ ] Interactive elements behave predictably
- [ ] No automatic redirects without warning
- [ ] Form submission clearly indicated
- [ ] Focus doesn't cause unexpected context changes

### Input Assistance

- [ ] Form errors identified and described
- [ ] Error prevention for critical actions
- [ ] Suggestions provided for corrections
- [ ] Confirmation for irreversible actions
- [ ] Help text available when needed

## Robust

### Compatible

- [ ] Valid HTML (use W3C validator)
- [ ] Proper semantic elements
- [ ] Unique IDs for elements
- [ ] ARIA used correctly (when needed)
- [ ] Works with assistive technologies

### ARIA Best Practices

- [ ] Use semantic HTML first, ARIA second
- [ ] Don't override native semantics
- [ ] All interactive ARIA controls are keyboard accessible
- [ ] ARIA labels/descriptions provided where needed
- [ ] ARIA states updated dynamically (if JavaScript used)

```html
<!-- Good ARIA usage -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<nav id="menu" aria-labelledby="menu-button" hidden>
  <!-- Navigation links -->
</nav>

<!-- Bad: unnecessary ARIA -->
<div role="button">Click</div> <!-- Use <button> instead -->
```

## Testing Checklist

### Manual Tests

- [ ] Navigate entire site using only keyboard (Tab, Enter, Escape)
- [ ] Disable CSS and check content order
- [ ] Zoom to 200% - content still readable?
- [ ] Test with grayscale filter (color-blind simulation)
- [ ] Read through with text-to-speech

### Automated Tests

- [ ] Run Lighthouse accessibility audit
- [ ] Check with axe DevTools
- [ ] Validate HTML (W3C validator)
- [ ] Test contrast ratios
- [ ] Check heading structure

### Screen Reader Tests

- [ ] Test with NVDA (Windows)
- [ ] Test with JAWS (Windows)
- [ ] Test with VoiceOver (Mac/iOS)
- [ ] Verify all content announced correctly
- [ ] Check navigation shortcuts work

## Common Issues and Fixes

### Issue: Images without alt text
```html
<!-- Bad -->
<img src="product.jpg">

<!-- Good -->
<img src="product.jpg" alt="Blue cotton t-shirt">
```

### Issue: Links with non-descriptive text
```html
<!-- Bad -->
<a href="/products">Click here</a>

<!-- Good -->
<a href="/products">View our products</a>
```

### Issue: Form inputs without labels
```html
<!-- Bad -->
<input type="text" placeholder="Name">

<!-- Good -->
<label for="name">Name</label>
<input type="text" id="name" placeholder="John Doe">
```

### Issue: Non-interactive elements made clickable
```html
<!-- Bad -->
<div onclick="submit()">Submit</div>

<!-- Good -->
<button type="submit">Submit</button>
```

### Issue: Skip link missing
```html
<!-- Add at start of <body> -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
</style>
```

## Quick Reference

### ARIA Landmarks
- `role="banner"` - Site header (or use `<header>`)
- `role="navigation"` - Navigation (or use `<nav>`)
- `role="main"` - Main content (or use `<main>`)
- `role="complementary"` - Supporting content (or use `<aside>`)
- `role="contentinfo"` - Footer (or use `<footer>`)

### ARIA States
- `aria-expanded="true|false"` - Expandable sections
- `aria-hidden="true|false"` - Hide from screen readers
- `aria-disabled="true|false"` - Disabled state
- `aria-current="page"` - Current page in navigation
- `aria-live="polite|assertive"` - Dynamic content updates

### ARIA Properties
- `aria-label="Text"` - Label for element
- `aria-labelledby="id"` - Reference to labeling element
- `aria-describedby="id"` - Reference to description
- `aria-required="true"` - Required form field
- `aria-invalid="true"` - Validation error

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Articles](https://webaim.org/articles/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [Chrome Lighthouse](https://developers.google.com/web/tools/lighthouse)

## Priority Levels

**Critical (Fix immediately):**
- Missing alt text on meaningful images
- Keyboard navigation broken
- Insufficient color contrast
- Missing form labels

**Important (Fix soon):**
- Improper heading hierarchy
- Missing skip links
- Non-semantic HTML
- Missing ARIA labels

**Enhancement (Nice to have):**
- Enhanced focus indicators
- Additional ARIA descriptions
- Improved error messages
- Better mobile accessibility
