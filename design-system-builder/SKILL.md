---
name: design-system-builder
description: Build complete, scalable design systems with design tokens, component libraries, documentation, and governance. Create cohesive visual languages, establish design principles, and maintain consistency across products and teams.
---

# Design System Builder

Create comprehensive design systems that scale across teams and products. Establish design tokens, component libraries, documentation, and governance for consistent user experiences.

## Overview

This skill builds complete design systems:
- Design tokens (colors, typography, spacing)
- Component library architecture
- Documentation and guidelines
- Governance and contribution models
- Theming and customization
- Accessibility standards
- Version control and releases

## Usage

Trigger this skill with queries like:
- "Build a design system for [organization]"
- "Create design tokens structure"
- "Establish design system governance"
- "Document design principles"
- "Set up theme customization"
- "Create design system style guide"

## Design System Architecture

### Foundation Layer: Design Tokens

**tokens.css**
```css
:root {
  /* Colors - Primitives */
  --color-blue-50: #eff6ff;
  --color-blue-500: #3b82f6;
  --color-blue-900: #1e3a8a;
  --color-gray-50: #f9fafb;
  --color-gray-900: #111827;

  /* Colors - Semantic */
  --color-primary: var(--color-blue-500);
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);
  --color-background: var(--color-gray-50);
  --color-surface: #ffffff;

  /* Typography */
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --font-family-mono: 'Fira Code', monospace;

  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  --font-size-3xl: 1.875rem;  /* 30px */
  --font-size-4xl: 2.25rem;   /* 36px */

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;

  /* Spacing */
  --spacing-0: 0;
  --spacing-1: 0.25rem;   /* 4px */
  --spacing-2: 0.5rem;    /* 8px */
  --spacing-3: 0.75rem;   /* 12px */
  --spacing-4: 1rem;      /* 16px */
  --spacing-6: 1.5rem;    /* 24px */
  --spacing-8: 2rem;      /* 32px */
  --spacing-12: 3rem;     /* 48px */
  --spacing-16: 4rem;     /* 64px */

  /* Border Radius */
  --radius-none: 0;
  --radius-sm: 0.125rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);

  /* Transitions */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 300ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 500ms cubic-bezier(0.4, 0, 0.2, 1);

  /* Z-index */
  --z-dropdown: 1000;
  --z-sticky: 1100;
  --z-modal: 1300;
  --z-tooltip: 1400;
}
```

### Component Layer

Components built using design tokens:
- Buttons, inputs, cards
- Navigation, modals, tooltips
- Data tables, forms, layouts
- All referencing design tokens

### Pattern Layer

Common patterns and templates:
- Page layouts
- Form patterns
- Dashboard templates
- Navigation patterns

### Documentation Layer

Comprehensive guides:
- Design principles
- Component documentation
- Usage guidelines
- Code examples

## Design System Structure

```
design-system/
├── foundation/
│   ├── tokens/
│   │   ├── colors.css
│   │   ├── typography.css
│   │   ├── spacing.css
│   │   └── index.css
│   ├── principles.md
│   └── accessibility.md
├── components/
│   ├── button/
│   ├── input/
│   ├── card/
│   └── ...
├── patterns/
│   ├── layouts/
│   ├── forms/
│   └── navigation/
├── documentation/
│   ├── getting-started.md
│   ├── contributing.md
│   ├── changelog.md
│   └── components/
└── examples/
    ├── landing-page/
    ├── dashboard/
    └── form/
```

## Design Principles Template

```markdown
# Design Principles

## 1. Consistency
Maintain visual and functional consistency across all touchpoints.

## 2. Accessibility
Design for all users, meeting WCAG 2.1 AA standards minimum.

## 3. Clarity
Clear communication through intentional design choices.

## 4. Efficiency
Streamline user tasks and developer workflows.

## 5. Flexibility
Support customization while maintaining coherence.

## Core Values
- User-centered
- Inclusive by default
- Performance-focused
- Documentation-first
```

## Theming System

**Theme Structure**
```css
/* Light Theme (Default) */
:root {
  --theme-background: var(--color-gray-50);
  --theme-surface: #ffffff;
  --theme-text-primary: var(--color-gray-900);
  --theme-text-secondary: var(--color-gray-600);
  --theme-border: var(--color-gray-200);
}

/* Dark Theme */
[data-theme="dark"] {
  --theme-background: var(--color-gray-900);
  --theme-surface: var(--color-gray-800);
  --theme-text-primary: var(--color-gray-50);
  --theme-text-secondary: var(--color-gray-400);
  --theme-border: var(--color-gray-700);
}

/* Brand Variants */
[data-brand="brand-a"] {
  --color-primary: #ff6b6b;
  --color-secondary: #4ecdc4;
}

[data-brand="brand-b"] {
  --color-primary: #6c5ce7;
  --color-secondary: #a29bfe;
}
```

## Component Documentation Template

```markdown
# Component Name

## Overview
Brief description of the component's purpose and use cases.

## Design Tokens Used
- `--color-primary`
- `--spacing-4`
- `--radius-md`
- `--shadow-md`

## Anatomy
Visual breakdown of component parts.

## Variants
### Primary
[Description and example]

### Secondary
[Description and example]

## States
- Default
- Hover
- Active
- Disabled
- Loading
- Error

## Usage Guidelines

### Do
- Use for primary actions
- Maintain consistent sizing
- Provide clear labels

### Don't
- Don't use more than one primary button per section
- Don't mix button styles unnecessarily

## Accessibility
- Keyboard navigation: [details]
- Screen reader support: [details]
- ARIA attributes: [details]
- Color contrast: [ratios]

## Code Example
\`\`\`html
<!-- Usage example -->
\`\`\`

## Props/API
| Prop | Type | Default | Description |
|------|------|---------|-------------|

## Related Components
- [Component A]
- [Component B]

## Version History
- v1.2.0: Added loading state
- v1.1.0: Improved accessibility
- v1.0.0: Initial release
```

## Governance Model

### Contribution Process
1. **Proposal** - Submit design proposal
2. **Review** - Design review by core team
3. **Prototype** - Create working prototype
4. **Testing** - Accessibility and usability testing
5. **Documentation** - Complete documentation
6. **Approval** - Final approval and merge
7. **Release** - Versioned release

### Roles
- **Design System Lead** - Overall vision and direction
- **Core Contributors** - Active maintainers
- **Community Contributors** - Submit proposals and improvements
- **Users** - Provide feedback and report issues

### Decision Making
- **Minor changes** - Core contributors decide
- **Major changes** - Require design review
- **Breaking changes** - Full team consensus

## Bundled Resources

### Scripts

**`scripts/token_generator.py`** - Generates design tokens from config
- Converts JSON/YAML to CSS variables
- Creates platform-specific tokens (iOS, Android)
- Generates documentation

Usage:
```bash
python scripts/token_generator.py tokens.json --output css
```

**`scripts/component_audit.py`** - Audits component usage
- Scans codebase for component usage
- Identifies outdated components
- Suggests updates

**`scripts/theme_validator.py`** - Validates theme completeness
- Ensures all tokens defined
- Checks color contrast ratios
- Validates accessibility

### References

**`references/design_tokens_guide.md`** - Comprehensive guide to design tokens structure and naming

**`references/design_system_governance.md`** - Governance models and contribution guidelines

**`references/theming_strategies.md`** - Multi-brand theming patterns and implementation

**`references/documentation_standards.md`** - Documentation best practices for design systems

**`references/versioning_strategy.md`** - Semantic versioning and changelog management

## Best Practices

**Design Tokens**
- Use semantic naming (not color values)
- Create scales for consistency
- Document token purpose
- Version token changes

**Components**
- Build from design tokens
- Document all variants and states
- Include accessibility requirements
- Provide code examples

**Documentation**
- Keep docs with code
- Include visual examples
- Document breaking changes
- Maintain changelog

**Governance**
- Clear contribution process
- Regular design reviews
- Version releases properly
- Communicate changes

**Maintenance**
- Regular accessibility audits
- Update dependencies
- Monitor component usage
- Gather user feedback

## Design System Checklist

**Foundation**
- [ ] Design principles documented
- [ ] Design tokens defined
- [ ] Color system established
- [ ] Typography scale created
- [ ] Spacing system defined
- [ ] Accessibility standards documented

**Components**
- [ ] Core components built
- [ ] All variants implemented
- [ ] States documented
- [ ] Accessibility tested
- [ ] Examples provided
- [ ] API documented

**Documentation**
- [ ] Getting started guide
- [ ] Component documentation
- [ ] Usage guidelines
- [ ] Code examples
- [ ] Changelog maintained
- [ ] Contributing guide

**Tooling**
- [ ] Token generator
- [ ] Build process
- [ ] Testing setup
- [ ] Documentation site
- [ ] Version control
- [ ] CI/CD pipeline

**Governance**
- [ ] Contribution process defined
- [ ] Review process established
- [ ] Roles assigned
- [ ] Communication channels set up
- [ ] Release schedule planned

## When to Use This Skill

Use design-system-builder when:
- Building design systems from scratch
- Scaling design across teams
- Ensuring brand consistency
- Need comprehensive documentation
- Managing multi-brand products
- Establishing design governance

Choose other skills for:
- Single pages (use html-static-design)
- Layout work (use css-layout-builder)
- Adding interactivity (use javascript-interactive-design)
- Individual components (use ui-component-design)

## Scaling Considerations

**Small Teams (1-5 people)**
- Focus on core components
- Lightweight documentation
- Flexible governance
- Regular sync meetings

**Medium Teams (5-20 people)**
- Comprehensive component library
- Detailed documentation
- Structured contribution process
- Dedicated design system team

**Large Teams (20+ people)**
- Full design system team
- Automated tooling
- Formal governance
- Multi-product support
- Regular audits and updates

## Maintenance Strategy

**Regular Activities**
- Quarterly accessibility audits
- Monthly component usage analysis
- Bi-weekly design reviews
- Continuous documentation updates
- Weekly user support

**Version Releases**
- Patch (bug fixes): As needed
- Minor (new features): Monthly
- Major (breaking changes): Quarterly

**Communication**
- Changelog for all releases
- Migration guides for breaking changes
- Regular newsletters
- Office hours for support
