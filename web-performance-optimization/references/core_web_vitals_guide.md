# Core Web Vitals Guide

## Overview

Core Web Vitals are a set of standardized metrics from Google that measure real-world user experience on the web. They focus on three aspects of user experience: loading performance, interactivity, and visual stability.

## The Three Core Web Vitals

### 1. Largest Contentful Paint (LCP)

**What it measures:** Loading performance - specifically, the render time of the largest content element visible in the viewport.

**Target:** 2.5 seconds or less

**Common LCP Elements:**
- `<img>` elements
- `<image>` elements inside `<svg>`
- `<video>` elements (poster image)
- Background images loaded via CSS `url()`
- Block-level elements containing text nodes

**What Affects LCP:**
1. Slow server response times (TTFB)
2. Render-blocking JavaScript and CSS
3. Resource load times (images, fonts, etc.)
4. Client-side rendering

**Optimization Strategies:**

#### Server Response Time
```nginx
# nginx configuration for fast server response
server {
    # Enable gzip compression
    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
    gzip_min_length 1024;

    # Enable HTTP/2
    listen 443 ssl http2;

    # Set caching headers
    location ~* \.(jpg|jpeg|png|gif|webp|avif)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### Eliminate Render-Blocking Resources
```html
<!-- Inline critical CSS -->
<style>
  /* Above-the-fold styles */
  .hero { min-height: 500px; }
</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">

<!-- Defer JavaScript -->
<script src="app.js" defer></script>
```

#### Optimize Images
```html
<!-- Preload LCP image -->
<link rel="preload" as="image" href="hero.jpg" fetchpriority="high">

<!-- Responsive images with modern formats -->
<picture>
  <source type="image/avif" srcset="hero.avif">
  <source type="image/webp" srcset="hero.webp">
  <img src="hero.jpg" alt="Hero" width="1200" height="600" loading="eager">
</picture>
```

### 2. First Input Delay (FID) / Interaction to Next Paint (INP)

**FID (being replaced by INP):**
- Measures time from first user interaction to browser response
- Target: < 100ms

**INP (replacing FID in 2024):**
- Measures responsiveness throughout entire page lifecycle
- Target: < 200ms
- Assesses all interactions, not just the first

**What Affects FID/INP:**
1. Heavy JavaScript execution
2. Large bundles blocking main thread
3. Long tasks (>50ms)
4. Third-party scripts

**Optimization Strategies:**

#### Break Up Long Tasks
```javascript
// ❌ Bad: Blocks main thread
function processItems(items) {
  items.forEach(item => {
    // Heavy processing
    heavyProcess(item);
  });
}

// ✅ Good: Yields to main thread
async function processItems(items) {
  for (const item of items) {
    heavyProcess(item);

    // Yield to main thread every 50ms
    if (performance.now() % 50 < 1) {
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  }
}

// ✅ Better: Use requestIdleCallback
function processItems(items) {
  function processChunk(startIndex) {
    const deadline = performance.now() + 50;

    let index = startIndex;
    while (index < items.length && performance.now() < deadline) {
      heavyProcess(items[index]);
      index++;
    }

    if (index < items.length) {
      requestIdleCallback(() => processChunk(index));
    }
  }

  requestIdleCallback(() => processChunk(0));
}
```

#### Code Splitting
```javascript
// Split by route
const routes = {
  '/': () => import('./pages/Home.js'),
  '/about': () => import('./pages/About.js'),
  '/products': () => import('./pages/Products.js')
};

// Split by interaction
button.addEventListener('click', async () => {
  const { Modal } = await import('./components/Modal.js');
  Modal.open();
});
```

#### Web Workers for Heavy Computation
```javascript
// main.js
const worker = new Worker('worker.js');

worker.postMessage({ data: largeDataset });

worker.onmessage = (e) => {
  console.log('Result:', e.data);
};

// worker.js
self.onmessage = (e) => {
  const result = heavyComputation(e.data.data);
  self.postMessage(result);
};
```

### 3. Cumulative Layout Shift (CLS)

**What it measures:** Visual stability - how much unexpected layout shift occurs during page load.

**Target:** 0.1 or less

**Formula:** CLS = Impact Fraction × Distance Fraction

**Common Causes:**
1. Images without dimensions
2. Ads, embeds, iframes without reserved space
3. Dynamically injected content
4. Web fonts causing FOIT/FOUT
5. Actions waiting on network response

**Optimization Strategies:**

#### Always Set Image Dimensions
```html
<!-- ❌ Bad: No dimensions -->
<img src="product.jpg" alt="Product">

<!-- ✅ Good: Explicit dimensions -->
<img src="product.jpg" width="800" height="600" alt="Product">

<!-- ✅ Good: Aspect ratio for responsive images -->
<div style="aspect-ratio: 16/9;">
  <img src="product.jpg" style="width: 100%; height: auto;" alt="Product">
</div>
```

#### Reserve Space for Dynamic Content
```css
/* Reserve space for ads */
.ad-slot {
  min-height: 250px;
  background: #f0f0f0;
}

/* Skeleton screens for loading content */
.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

#### Optimize Font Loading
```css
/* Use font-display to control font loading behavior */
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* or optional */
}

/* Match fallback font metrics to reduce shift */
@font-face {
  font-family: 'CustomFont Fallback';
  src: local('Arial');
  size-adjust: 105%;
  ascent-override: 95%;
  descent-override: 25%;
  line-gap-override: 0%;
}

body {
  font-family: 'CustomFont', 'CustomFont Fallback', sans-serif;
}
```

#### Transform/Opacity Animations Only
```css
/* ❌ Bad: Causes layout shift */
.element {
  transition: margin-top 0.3s;
}
.element:hover {
  margin-top: 10px;
}

/* ✅ Good: Uses transform */
.element {
  transition: transform 0.3s;
}
.element:hover {
  transform: translateY(-10px);
}
```

## Measuring Core Web Vitals

### 1. Chrome DevTools
```javascript
// Open Chrome DevTools > Performance
// Record page load
// Look for "Experience" section for CLS
// Check "Main" thread for long tasks affecting FID
```

### 2. Lighthouse
```bash
# CLI
npx lighthouse https://example.com --view

# Chrome DevTools > Lighthouse tab
```

### 3. Web Vitals JavaScript Library
```html
<script type="module">
import {onCLS, onFID, onLCP, onINP} from 'https://unpkg.com/web-vitals@3?module';

onCLS(console.log);
onFID(console.log);
onLCP(console.log);
onINP(console.log);
</script>
```

### 4. Real User Monitoring
```javascript
import {onCLS, onFID, onLCP, onINP} from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,
    id: metric.id,
    navigationType: metric.navigationType
  });

  // Use sendBeacon to ensure data is sent
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/analytics', body);
  } else {
    fetch('/analytics', { body, method: 'POST', keepalive: true });
  }
}

onCLS(sendToAnalytics);
onFID(sendToAnalytics);
onLCP(sendToAnalytics);
onINP(sendToAnalytics);
```

## Rating Thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤ 2.5s | 2.5s - 4.0s | > 4.0s |
| FID | ≤ 100ms | 100ms - 300ms | > 300ms |
| INP | ≤ 200ms | 200ms - 500ms | > 500ms |
| CLS | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

## Common Patterns by Score Range

### Poor LCP (> 4.0s)
**Common issues:**
- Unoptimized hero images (2-5MB)
- No CDN usage
- Blocking scripts in `<head>`
- Server response time > 600ms
- Client-side rendering with large bundle

**Quick wins:**
1. Optimize and preload hero image
2. Move scripts to bottom with defer
3. Enable CDN
4. Implement server-side rendering or static generation

### Poor FID/INP (> 300ms/500ms)
**Common issues:**
- Large JavaScript bundle (> 500KB)
- Heavy third-party scripts
- Complex calculations on main thread
- Polling or frequent timers

**Quick wins:**
1. Code split by route
2. Defer third-party scripts
3. Use Web Workers for heavy computation
4. Debounce expensive operations

### Poor CLS (> 0.25)
**Common issues:**
- Images without dimensions
- Ads without reserved space
- Custom fonts without fallback matching
- Content injected above existing content

**Quick wins:**
1. Set width/height on all images
2. Reserve space for ads and embeds
3. Use font-display: optional or swap
4. Use transform animations instead of layout properties

## Advanced Optimization Techniques

### Priority Hints
```html
<!-- High priority for LCP image -->
<link rel="preload" as="image" href="hero.jpg" fetchpriority="high">
<img src="hero.jpg" fetchpriority="high" alt="Hero">

<!-- Low priority for below-fold images -->
<img src="footer-logo.jpg" fetchpriority="low" loading="lazy" alt="Logo">
```

### Content Visibility
```css
/* Render only visible content -->
.section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px; /* Estimated height */
}
```

### Early Hints (103 Status Code)
```
HTTP/1.1 103 Early Hints
Link: </style.css>; rel=preload; as=style
Link: </script.js>; rel=preload; as=script
```

## Further Resources

- [Web.dev Core Web Vitals](https://web.dev/vitals/)
- [Chrome User Experience Report](https://developers.google.com/web/tools/chrome-user-experience-report)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [WebPageTest](https://www.webpagetest.org/)
