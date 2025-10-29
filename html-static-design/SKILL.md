---
name: html-static-design
description: Collaborative HTML/CSS static design skill for building clean, semantic, and visually appealing static web pages through iterative refinement between AI and user. Handles structure, styling, layout, and design feedback.
---

# HTML Static Design

A collaborative skill for creating static HTML/CSS designs through iterative refinement. Build semantic, accessible, and visually appealing web pages from concept to completion.

## Overview

This skill guides the design and development of static HTML/CSS web pages through a structured, collaborative process:
- Design consultation and requirements gathering
- Semantic HTML structure creation
- CSS styling with modern best practices
- Iterative refinement based on user feedback
- Responsive design considerations
- Accessibility compliance

## Usage

Trigger this skill with queries like:
- "Design a static landing page for [project]"
- "Create an HTML/CSS portfolio page"
- "Build a simple website with [requirements]"
- "Design a static page with [specific elements]"

### Design Phase

**Step 1: Requirements Gathering**
Ask clarifying questions about:
- Purpose and target audience
- Desired sections and content
- Color preferences and branding
- Layout style (modern, minimal, classic, etc.)
- Any specific design inspirations

**Step 2: Design Proposal**
Present a design concept including:
- Overall layout structure
- Color palette suggestion
- Typography choices
- Section breakdown
- Key visual elements

### Development Phase

**Step 3: HTML Structure**
Build semantic HTML with:
- Proper DOCTYPE and meta tags
- Semantic HTML5 elements (header, nav, main, section, article, footer)
- Accessible markup (ARIA labels, alt text)
- Clean, organized structure

**Step 4: CSS Styling**
Apply modern CSS including:
- CSS custom properties for theme variables
- Flexbox and Grid for layouts
- Modern typography scaling
- Smooth transitions and hover effects
- Mobile-first responsive design

**Step 5: Iterative Refinement**
Collaborate with user to:
- Adjust colors, spacing, typography
- Refine layout and positioning
- Add or modify sections
- Implement feedback iteratively
- Polish visual details

## Bundled Resources

### Scripts

**`scripts/html_validator.py`** - Validates HTML structure and checks for common issues
- Validates semantic HTML usage
- Checks for accessibility attributes
- Identifies missing meta tags
- Reports structural issues

Usage:
```bash
python scripts/html_validator.py index.html
```

**`scripts/css_analyzer.py`** - Analyzes CSS for optimization opportunities
- Identifies unused selectors
- Checks specificity issues
- Suggests modern alternatives
- Reports on file size

Usage:
```bash
python scripts/css_analyzer.py styles.css
```

### References

**`references/html_semantic_guide.md`** - Comprehensive guide to semantic HTML5 elements and proper usage patterns

**`references/css_modern_patterns.md`** - Modern CSS patterns including Grid, Flexbox, custom properties, and responsive design techniques

**`references/accessibility_checklist.md`** - Accessibility requirements and testing checklist for static sites

**`references/color_design_principles.md`** - Color theory, palette generation, and contrast guidelines for web design

### Assets

**`assets/templates/`** - Starter HTML templates for common page types:
- Landing page template
- Portfolio page template
- Documentation page template
- About page template

**`assets/css-snippets/`** - Reusable CSS components:
- Navigation bars
- Hero sections
- Card layouts
- Footer designs
- Button styles
- Form styling

## Design Workflow

### Initial Creation
1. Gather requirements and preferences
2. Propose design concept for approval
3. Create base HTML structure
4. Apply initial CSS styling
5. Present for feedback

### Iterative Refinement
1. User provides feedback (colors, spacing, layout, etc.)
2. Make requested adjustments
3. Show updated version
4. Repeat until satisfied
5. Final polish and optimization

### Deliverables
- Complete HTML file(s)
- CSS stylesheet(s)
- Any required assets (images referenced)
- Usage instructions
- Browser compatibility notes

## Best Practices

**HTML Structure**
- Use semantic HTML5 elements appropriately
- Maintain proper heading hierarchy (h1 → h2 → h3)
- Include meta tags for SEO and responsiveness
- Use meaningful class names (BEM methodology recommended)
- Add alt text for all images

**CSS Styling**
- Use CSS custom properties for theme values
- Implement mobile-first responsive design
- Avoid inline styles; use external stylesheet
- Use relative units (rem, em, %, vw/vh) over fixed pixels
- Group related styles logically with comments

**Accessibility**
- Ensure sufficient color contrast (WCAG AA minimum)
- Add ARIA labels where needed
- Make interactive elements keyboard-accessible
- Test with screen reader considerations
- Use semantic HTML for better accessibility

**Performance**
- Minimize CSS file size
- Avoid overly specific selectors
- Use efficient layouts (Flexbox/Grid over floats)
- Optimize any embedded images
- Consider critical CSS for above-the-fold content

## Common Patterns

### Landing Page Structure
```html
<header> - Logo, navigation
<main>
  <section class="hero"> - Main value proposition
  <section class="features"> - Key features/benefits
  <section class="about"> - About/details
  <section class="cta"> - Call to action
</main>
<footer> - Contact, links, copyright
```

### Modern CSS Layout
```css
/* Use CSS custom properties */
:root {
  --primary-color: #3498db;
  --spacing-unit: 1rem;
}

/* Use Flexbox/Grid for layouts */
.container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-unit);
}
```

## Feedback Integration

When user provides feedback, acknowledge and implement:
- **Color changes**: Update CSS custom properties
- **Spacing adjustments**: Modify margin/padding values
- **Layout changes**: Adjust Grid/Flexbox properties
- **Content additions**: Add new semantic sections
- **Style refinements**: Update typography, borders, shadows

Always show the complete updated code after each iteration.

## Troubleshooting

**Layout issues**
- Check for missing closing tags
- Verify CSS box-sizing is set to border-box
- Inspect flexbox/grid container properties
- Test in multiple browser sizes

**Styling not applying**
- Check CSS specificity
- Verify class names match HTML
- Ensure CSS file is linked correctly
- Check for typos in property names

**Responsiveness problems**
- Add viewport meta tag
- Use relative units instead of fixed pixels
- Test breakpoints at common device widths
- Use mobile-first media queries

## When to Use This Skill

Use html-static-design when:
- Creating simple static websites or pages
- Building landing pages or portfolios
- Prototyping designs quickly
- Learning HTML/CSS fundamentals
- Need full control over markup and styling
- Working without JavaScript frameworks

Choose other skills for:
- Dynamic web applications (use javascript-interactive-design)
- Complex responsive layouts (use css-layout-builder)
- Component-based development (use ui-component-design)
- Design system creation (use design-system-builder)
