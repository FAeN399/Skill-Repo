# HTML Semantic Elements Guide

Comprehensive guide to HTML5 semantic elements and their proper usage.

## Core Semantic Elements

### `<header>`
Container for introductory content or navigation links.

**Use for:**
- Site logo and branding
- Main navigation
- Page or section introductions

**Example:**
```html
<header>
  <h1>Site Name</h1>
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
</header>
```

### `<nav>`
Section containing navigation links.

**Use for:**
- Main site navigation
- Table of contents
- Pagination

**Example:**
```html
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/services">Services</a></li>
    <li><a href="/contact">Contact</a></li>
  </ul>
</nav>
```

### `<main>`
Dominant content of the page. Only one per page.

**Use for:**
- Primary page content
- Content unique to this page

**Example:**
```html
<main>
  <h1>Page Title</h1>
  <p>Main content goes here...</p>
</main>
```

### `<article>`
Self-contained composition that could be distributed independently.

**Use for:**
- Blog posts
- News articles
- User comments
- Forum posts

**Example:**
```html
<article>
  <h2>Article Title</h2>
  <p>Published on <time datetime="2024-01-15">January 15, 2024</time></p>
  <p>Article content...</p>
</article>
```

### `<section>`
Thematic grouping of content with a heading.

**Use for:**
- Chapters
- Tabbed content
- Numbered sections

**Example:**
```html
<section>
  <h2>Section Title</h2>
  <p>Related content...</p>
</section>
```

### `<aside>`
Content tangentially related to main content.

**Use for:**
- Sidebars
- Pull quotes
- Related links
- Advertisements

**Example:**
```html
<aside>
  <h3>Related Articles</h3>
  <ul>
    <li><a href="/related-1">Article 1</a></li>
    <li><a href="/related-2">Article 2</a></li>
  </ul>
</aside>
```

### `<footer>`
Footer for nearest sectioning content or root.

**Use for:**
- Copyright information
- Contact details
- Site map links
- Social media links

**Example:**
```html
<footer>
  <p>&copy; 2024 Company Name</p>
  <nav aria-label="Footer navigation">
    <a href="/privacy">Privacy</a>
    <a href="/terms">Terms</a>
  </nav>
</footer>
```

## Document Structure Elements

### `<figure>` and `<figcaption>`
Self-contained content with optional caption.

```html
<figure>
  <img src="diagram.png" alt="System architecture">
  <figcaption>Figure 1: System Architecture Diagram</figcaption>
</figure>
```

### `<time>`
Represents specific time or date.

```html
<time datetime="2024-01-15T14:30:00">January 15, 2024 at 2:30 PM</time>
```

### `<mark>`
Highlighted or marked text for reference.

```html
<p>Search results for <mark>semantic HTML</mark></p>
```

## Heading Hierarchy

Maintain proper heading levels:
- `<h1>` - Page title (one per page)
- `<h2>` - Major sections
- `<h3>` - Subsections
- `<h4>` - Sub-subsections
- Continue logically...

**Never skip heading levels!**

## Common Patterns

### Blog Post
```html
<article>
  <header>
    <h1>Post Title</h1>
    <p>By <span>Author Name</span> on <time datetime="2024-01-15">Jan 15, 2024</time></p>
  </header>
  <p>Post content...</p>
  <footer>
    <p>Tags: HTML, CSS, Web Design</p>
  </footer>
</article>
```

### Landing Page
```html
<body>
  <header>
    <nav>Site navigation</nav>
  </header>
  <main>
    <section class="hero">Hero content</section>
    <section class="features">Features</section>
    <section class="testimonials">Testimonials</section>
    <section class="cta">Call to action</section>
  </main>
  <footer>Footer content</footer>
</body>
```

## Best Practices

1. **Use semantic elements instead of divs** when appropriate
2. **Maintain heading hierarchy** - don't skip levels
3. **One `<main>` per page** - only one main content area
4. **`<header>` and `<footer>` can be nested** - they apply to their parent section
5. **`<section>` should have a heading** - even if visually hidden
6. **Use `<article>` for syndication** - content that makes sense independently
7. **Add ARIA labels** when needed for clarity

## Anti-patterns to Avoid

❌ Skipping heading levels
```html
<h1>Title</h1>
<h3>Subsection</h3> <!-- Wrong! Should be h2 -->
```

❌ Multiple `<main>` elements
```html
<main>Content 1</main>
<main>Content 2</main> <!-- Wrong! Only one main -->
```

❌ Using `<section>` without heading
```html
<section>
  <p>Content without heading</p> <!-- Wrong! Add a heading -->
</section>
```

❌ Divitis - overusing divs
```html
<div class="header"> <!-- Wrong! Use <header> -->
<div class="navigation"> <!-- Wrong! Use <nav> -->
```

## Accessibility Benefits

Semantic HTML provides:
- **Screen reader navigation** - Users can jump between sections
- **Better SEO** - Search engines understand content structure
- **Keyboard navigation** - Logical tab order
- **Meaning without CSS** - Content makes sense without styling
