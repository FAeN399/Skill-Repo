# Color Design Principles for Web

Comprehensive guide to color theory, palette creation, and web design color best practices.

## Color Theory Basics

### Color Wheel

**Primary Colors:** Red, Blue, Yellow (in traditional theory)
**Secondary Colors:** Green, Orange, Purple (mix of primaries)
**Tertiary Colors:** Mix of primary and secondary

### Color Relationships

**Complementary** - Opposite on color wheel
- High contrast, vibrant
- Example: Blue (#3498db) + Orange (#e67e22)
- Use: Call-to-action buttons against background

**Analogous** - Adjacent on color wheel
- Harmonious, pleasing
- Example: Blue → Blue-Green → Green
- Use: Gradient backgrounds, related sections

**Triadic** - Equally spaced (120° apart)
- Balanced, vibrant
- Example: Red, Yellow, Blue
- Use: Feature highlights, icons

**Split-Complementary** - Base + two adjacent to complement
- Less tension than complementary
- Example: Blue + Red-Orange + Yellow-Orange
- Use: Balanced color schemes

**Monochromatic** - Variations of single hue
- Cohesive, sophisticated
- Example: Light blue → Medium blue → Dark blue
- Use: Minimalist designs, professional sites

## Color Properties

### Hue
The pure color (red, blue, green, etc.)

### Saturation
Intensity or purity of color
- High saturation: Vivid, bold
- Low saturation: Muted, subtle

### Lightness/Value
How light or dark the color is
- Lighter: Tints (add white)
- Darker: Shades (add black)

### Temperature
- **Warm colors:** Red, orange, yellow (energetic, passionate)
- **Cool colors:** Blue, green, purple (calming, professional)

## Building Color Palettes

### 60-30-10 Rule

**60% - Dominant color** (backgrounds, large sections)
**30% - Secondary color** (supporting sections, panels)
**10% - Accent color** (buttons, links, highlights)

```css
:root {
  --color-dominant: #f8f9fa;    /* 60% - Light gray backgrounds */
  --color-secondary: #2c3e50;   /* 30% - Dark blue-gray sections */
  --color-accent: #3498db;      /* 10% - Bright blue accents */
}
```

### Essential Palette Colors

1. **Primary brand color** - Main identity color
2. **Secondary color(s)** - Supporting colors
3. **Neutral colors** - Grays for text, backgrounds
4. **Semantic colors** - Success, warning, error, info
5. **Accent color** - For emphasis

```css
:root {
  /* Brand */
  --primary: #3498db;
  --secondary: #2ecc71;

  /* Neutrals */
  --gray-50: #f8f9fa;
  --gray-100: #e9ecef;
  --gray-200: #dee2e6;
  --gray-700: #495057;
  --gray-900: #212529;

  /* Semantic */
  --success: #28a745;
  --warning: #ffc107;
  --error: #dc3545;
  --info: #17a2b8;

  /* Accent */
  --accent: #ff6b6b;
}
```

### Color Scales

Create tints and shades for flexibility.

```css
:root {
  --blue-50: #e3f2fd;
  --blue-100: #bbdefb;
  --blue-200: #90caf9;
  --blue-300: #64b5f6;
  --blue-400: #42a5f5;
  --blue-500: #2196f3;  /* Base color */
  --blue-600: #1e88e5;
  --blue-700: #1976d2;
  --blue-800: #1565c0;
  --blue-900: #0d47a1;
}
```

## Contrast and Accessibility

### WCAG Contrast Requirements

**Level AA (Minimum)**
- Normal text: 4.5:1 ratio
- Large text (18pt+): 3:1 ratio

**Level AAA (Enhanced)**
- Normal text: 7:1 ratio
- Large text: 4.5:1 ratio

### Contrast Examples

```css
/* Good contrast - passes AA */
.text-good {
  color: #212529;           /* Dark gray */
  background: #ffffff;      /* White */
  /* Ratio: 16.1:1 */
}

/* Poor contrast - fails */
.text-bad {
  color: #adb5bd;           /* Light gray */
  background: #ffffff;      /* White */
  /* Ratio: 2.5:1 - FAIL */
}

/* Good accent on dark */
.accent-good {
  color: #3498db;           /* Bright blue */
  background: #1a1a1a;      /* Dark gray */
  /* Ratio: 5.8:1 - PASS */
}
```

### Testing Tools

- Chrome DevTools Contrast Checker
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Coolors Contrast Checker](https://coolors.co/contrast-checker)

## Color Psychology

### Red (#e74c3c)
- **Emotions:** Passion, energy, urgency, danger
- **Use for:** Sale badges, error messages, CTAs
- **Industries:** Food, entertainment, sports

### Blue (#3498db)
- **Emotions:** Trust, calm, professional, stable
- **Use for:** Corporate sites, tech, healthcare
- **Industries:** Finance, technology, healthcare

### Green (#2ecc71)
- **Emotions:** Growth, health, success, nature
- **Use for:** Success messages, eco products, health
- **Industries:** Environment, health, finance

### Yellow (#f39c12)
- **Emotions:** Optimism, warning, energy, happiness
- **Use for:** Warnings, highlights, attention
- **Industries:** Food, children, entertainment

### Purple (#9b59b6)
- **Emotions:** Luxury, creativity, wisdom, mystery
- **Use for:** Premium products, creative services
- **Industries:** Beauty, luxury, creative

### Orange (#e67e22)
- **Emotions:** Friendly, confident, energetic
- **Use for:** CTAs, playful brands, food
- **Industries:** Food, entertainment, sports

### Gray (#95a5a6)
- **Emotions:** Neutral, balanced, sophisticated
- **Use for:** Backgrounds, text, modern designs
- **Industries:** Technology, professional services

## Practical Application

### Text Colors

```css
:root {
  --text-primary: #212529;     /* Main content */
  --text-secondary: #6c757d;   /* Supporting text */
  --text-muted: #adb5bd;       /* Disabled/subtle */
  --text-inverse: #ffffff;     /* On dark backgrounds */
}
```

### Background Colors

```css
:root {
  --bg-primary: #ffffff;       /* Main background */
  --bg-secondary: #f8f9fa;     /* Alternate sections */
  --bg-tertiary: #e9ecef;      /* Cards, panels */
  --bg-dark: #212529;          /* Dark mode/sections */
}
```

### Interactive Elements

```css
.button {
  background: var(--primary);
  color: white;
}

.button:hover {
  background: var(--primary-dark);  /* Darker on hover */
}

.button:active {
  background: var(--primary-darker); /* Even darker on click */
}

.link {
  color: var(--primary);
}

.link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

.link:visited {
  color: var(--purple);
}
```

## Common Color Schemes

### Professional/Corporate
```css
:root {
  --primary: #2c3e50;    /* Navy blue */
  --secondary: #34495e;  /* Dark gray-blue */
  --accent: #3498db;     /* Bright blue */
  --background: #ecf0f1; /* Light gray */
}
```

### Creative/Modern
```css
:root {
  --primary: #9b59b6;    /* Purple */
  --secondary: #e74c3c;  /* Red */
  --accent: #f39c12;     /* Orange */
  --background: #1a1a1a; /* Dark */
}
```

### Natural/Eco
```css
:root {
  --primary: #27ae60;    /* Green */
  --secondary: #16a085;  /* Teal */
  --accent: #f39c12;     /* Golden */
  --background: #f8f9fa; /* Off-white */
}
```

### Minimalist
```css
:root {
  --primary: #000000;    /* Black */
  --secondary: #666666;  /* Medium gray */
  --accent: #ff0000;     /* Red accent */
  --background: #ffffff; /* White */
}
```

## Color Palette Tools

### Generation Tools
- [Coolors.co](https://coolors.co) - Palette generator
- [Adobe Color](https://color.adobe.com) - Color wheel tool
- [Paletton](https://paletton.com) - Scheme designer
- [Colormind](http://colormind.io) - AI palette generator

### Inspiration
- [Dribbble](https://dribbble.com/colors) - Design inspiration
- [Muzli Colors](https://colors.muz.li) - Curated palettes
- [Color Hunt](https://colorhunt.co) - Trendy palettes

### Accessibility
- [Who Can Use](https://whocanuse.com) - Color vision simulation
- [Colorable](https://colorable.jxnblk.com) - Contrast tester

## Best Practices

### Do's
✅ Limit palette to 3-5 main colors
✅ Ensure sufficient contrast for text
✅ Use color consistently throughout
✅ Test on multiple devices/screens
✅ Consider color-blind users
✅ Use semantic colors appropriately
✅ Create color scales for flexibility

### Don'ts
❌ Use too many colors (overwhelms)
❌ Rely solely on color to convey meaning
❌ Use bright colors for large areas
❌ Ignore accessibility guidelines
❌ Mix warm and cool randomly
❌ Use pure black (#000000) for text
❌ Forget to test contrast

## Dark Mode Considerations

```css
:root {
  --bg: #ffffff;
  --text: #212529;
  --border: #dee2e6;
}

[data-theme="dark"] {
  --bg: #1a1a1a;
  --text: #e9ecef;
  --border: #495057;
}

body {
  background: var(--bg);
  color: var(--text);
  border-color: var(--border);
}
```

**Dark mode tips:**
- Don't just invert colors
- Reduce saturation slightly
- Use dark grays, not pure black
- Ensure contrast still meets WCAG
- Test thoroughly

## Color Naming

Use descriptive names, not color names:

```css
/* Bad - what if brand changes? */
:root {
  --blue: #3498db;
  --red: #e74c3c;
}

/* Good - semantic naming */
:root {
  --primary: #3498db;
  --danger: #e74c3c;
}

/* Even better - purpose-based */
:root {
  --brand-primary: #3498db;
  --status-error: #e74c3c;
  --action-cta: #2ecc71;
}
```

## Quick Reference

### Typical Web Palette Structure
- 1 primary color (brand)
- 1-2 secondary colors (supporting)
- 1 accent color (CTAs, emphasis)
- 3-5 neutral grays (text, backgrounds)
- 4 semantic colors (success, warning, error, info)
- Light and dark variants of each

**Total: 15-25 color values** in your CSS variables
