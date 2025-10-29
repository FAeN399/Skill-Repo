---
name: web-performance-optimization
description: Comprehensive web performance optimization covering Core Web Vitals, asset optimization, code splitting, lazy loading, caching strategies, and automated performance auditing
---

# Web Performance Optimization Skill

## Overview

This skill provides comprehensive guidance for optimizing web application performance, focusing on measurable improvements in load time, interactivity, and visual stability. It covers the complete performance optimization workflow from initial audit through implementation and continuous monitoring.

**Key Capabilities:**
- Core Web Vitals optimization (LCP, FID, CLS, INP)
- Image and asset optimization strategies
- JavaScript and CSS code splitting and minification
- Lazy loading techniques for images, videos, and components
- Caching strategies and service worker implementation
- Performance monitoring and auditing automation
- Bundle analysis and optimization
- Network optimization and CDN configuration
- Critical rendering path optimization
- Third-party script management

**What This Skill Provides:**
- Automated performance auditing scripts
- Image optimization and compression tools
- Bundle analysis and tree-shaking guidance
- Performance budgets and monitoring setup
- Real-world optimization patterns and code examples
- Progressive enhancement strategies
- Performance testing and measurement techniques

**Integration with Other Skills:**
- Complements `html-static-design` with performance-optimized markup patterns
- Enhances `css-layout-builder` with optimized layout techniques
- Extends `javascript-interactive-design` with performance-conscious JS patterns
- Supports `ui-component-design` with lazy-loading component strategies
- Integrates with `design-system-builder` for performance-first design tokens

## Usage

Trigger this skill when you need to:
- "Optimize the performance of my website"
- "Improve Core Web Vitals scores"
- "Reduce page load time"
- "Analyze and optimize bundle size"
- "Implement lazy loading for images"
- "Set up performance monitoring"
- "Optimize JavaScript execution time"
- "Improve First Contentful Paint"
- "Reduce layout shift"
- "Audit and fix performance issues"

## Core Web Vitals

The three primary metrics that Google uses to measure user experience:

### 1. Largest Contentful Paint (LCP)
**Target:** < 2.5 seconds
**What it measures:** Time until the largest content element becomes visible
**Common issues:**
- Slow server response times
- Render-blocking resources
- Unoptimized images
- Client-side rendering delays

**Optimization strategies:**
```html
<!-- Preload critical resources -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/images/hero.jpg" as="image">

<!-- Optimize images with responsive sizing -->
<img
  src="/images/hero-800.jpg"
  srcset="/images/hero-400.jpg 400w,
          /images/hero-800.jpg 800w,
          /images/hero-1200.jpg 1200w"
  sizes="(max-width: 640px) 400px,
         (max-width: 1024px) 800px,
         1200px"
  alt="Hero image"
  loading="eager"
  decoding="async"
  fetchpriority="high">

<!-- Inline critical CSS -->
<style>
  /* Critical above-the-fold styles here */
  .hero { min-height: 400px; background: #f0f0f0; }
</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="/css/non-critical.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/css/non-critical.css"></noscript>
```

### 2. First Input Delay (FID) / Interaction to Next Paint (INP)
**FID Target:** < 100ms
**INP Target:** < 200ms
**What it measures:** Time from user interaction to browser response
**Common issues:**
- Large JavaScript bundles blocking main thread
- Long-running JavaScript tasks
- Heavy third-party scripts
- Unoptimized event handlers

**Optimization strategies:**
```javascript
// ❌ BAD: Blocking main thread
function processLargeDataset(data) {
  for (let i = 0; i < 1000000; i++) {
    // Heavy computation
  }
}

// ✅ GOOD: Break into smaller chunks
function processLargeDataset(data) {
  const chunkSize = 1000;
  let index = 0;

  function processChunk() {
    const end = Math.min(index + chunkSize, data.length);

    for (let i = index; i < end; i++) {
      // Process item
    }

    index = end;

    if (index < data.length) {
      requestIdleCallback(processChunk);
    }
  }

  processChunk();
}

// ✅ GOOD: Debounce expensive handlers
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

const handleSearch = debounce((query) => {
  // Expensive search operation
}, 300);

searchInput.addEventListener('input', (e) => handleSearch(e.target.value));

// ✅ GOOD: Use passive event listeners
document.addEventListener('scroll', handleScroll, { passive: true });
document.addEventListener('touchstart', handleTouch, { passive: true });
```

### 3. Cumulative Layout Shift (CLS)
**Target:** < 0.1
**What it measures:** Visual stability during page load
**Common issues:**
- Images without dimensions
- Ads, embeds, and iframes without reserved space
- Web fonts causing FOIT/FOUT
- Dynamic content insertion

**Optimization strategies:**
```html
<!-- ✅ GOOD: Always specify image dimensions -->
<img src="image.jpg" width="800" height="600" alt="Description">

<!-- ✅ GOOD: Reserve space for responsive images -->
<div style="aspect-ratio: 16/9; position: relative;">
  <img src="image.jpg" alt="Description" style="width: 100%; height: auto;">
</div>

<!-- ✅ GOOD: Reserve space for ads/embeds -->
<div class="ad-container" style="min-height: 250px;">
  <!-- Ad content loads here -->
</div>

<style>
  /* ✅ GOOD: Font loading strategy to prevent shift */
  @font-face {
    font-family: 'Custom Font';
    src: url('/fonts/custom.woff2') format('woff2');
    font-display: swap; /* or optional */
  }

  body {
    font-family: 'Custom Font', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }

  /* ✅ GOOD: Size fallback font to match custom font */
  @font-face {
    font-family: 'Custom Font Fallback';
    src: local('Arial');
    ascent-override: 95%;
    descent-override: 25%;
    line-gap-override: 0%;
    size-adjust: 105%;
  }
</style>
```

## Performance Optimization Workflow

### Phase 1: Audit and Baseline

**1.1 Run Performance Audit**
```bash
# Using the bundled performance_auditor.py script
python scripts/performance_auditor.py --url https://yoursite.com --output report.json

# Or use Lighthouse CLI
npx lighthouse https://yoursite.com --output html --output-path ./report.html
```

**1.2 Establish Performance Budget**
```json
{
  "budgets": [
    {
      "resourceSizes": [
        { "resourceType": "script", "budget": 300 },
        { "resourceType": "stylesheet", "budget": 100 },
        { "resourceType": "image", "budget": 500 },
        { "resourceType": "font", "budget": 100 },
        { "resourceType": "total", "budget": 1000 }
      ],
      "timings": [
        { "metric": "first-contentful-paint", "budget": 1500 },
        { "metric": "largest-contentful-paint", "budget": 2500 },
        { "metric": "interactive", "budget": 3500 }
      ]
    }
  ]
}
```

**1.3 Analyze Current State**
- Core Web Vitals scores
- Bundle sizes (JS, CSS, images, fonts)
- Network waterfall analysis
- Render-blocking resources
- Third-party script impact

### Phase 2: Asset Optimization

**2.1 Image Optimization**

Use the bundled `image_optimizer.py` script:
```bash
python scripts/image_optimizer.py --input ./images --output ./images/optimized
```

Manual optimization strategies:
```html
<!-- Modern image formats with fallbacks -->
<picture>
  <source type="image/avif" srcset="image.avif">
  <source type="image/webp" srcset="image.webp">
  <img src="image.jpg" alt="Description" loading="lazy">
</picture>

<!-- Responsive images -->
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w,
          image-800.jpg 800w,
          image-1200.jpg 1200w,
          image-1600.jpg 1600w"
  sizes="(max-width: 640px) 100vw,
         (max-width: 1024px) 50vw,
         800px"
  alt="Description"
  loading="lazy"
  decoding="async">

<!-- Background images with CSS -->
<style>
  .hero {
    background-image: image-set(
      url('hero.avif') type('image/avif'),
      url('hero.webp') type('image/webp'),
      url('hero.jpg') type('image/jpeg')
    );
  }
</style>
```

**Image optimization checklist:**
- [ ] Use modern formats (AVIF, WebP) with fallbacks
- [ ] Implement responsive images with srcset
- [ ] Compress images (80-85% quality for JPEG)
- [ ] Use lazy loading for below-fold images
- [ ] Set explicit width/height to prevent CLS
- [ ] Use CDN for image delivery
- [ ] Implement blur-up or LQIP (Low Quality Image Placeholder)

**2.2 Font Optimization**

```html
<!-- Preload critical fonts -->
<link
  rel="preload"
  href="/fonts/main-regular.woff2"
  as="font"
  type="font/woff2"
  crossorigin>

<style>
  /* Font loading with swap strategy */
  @font-face {
    font-family: 'Main Font';
    src: url('/fonts/main-regular.woff2') format('woff2'),
         url('/fonts/main-regular.woff') format('woff');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
  }

  /* Only load weights you actually use */
  @font-face {
    font-family: 'Main Font';
    src: url('/fonts/main-bold.woff2') format('woff2');
    font-weight: 700;
    font-style: normal;
    font-display: swap;
  }

  /* Subsetting for specific character ranges */
  @font-face {
    font-family: 'Main Font';
    src: url('/fonts/main-latin.woff2') format('woff2');
    unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
  }
</style>
```

**Font optimization checklist:**
- [ ] Use WOFF2 format (best compression)
- [ ] Subset fonts to only needed characters
- [ ] Use font-display: swap or optional
- [ ] Preload critical fonts
- [ ] Limit font variations (weights/styles)
- [ ] Use system fonts as fallbacks
- [ ] Self-host fonts (avoid external requests)

**2.3 CSS Optimization**

```bash
# Analyze CSS with bundled script
python scripts/css_optimizer.py --input styles.css --output styles.min.css

# Manual optimization
npx purgecss --css styles.css --content index.html --output styles.purged.css
npx cssnano styles.css styles.min.css
```

CSS optimization patterns:
```css
/* ✅ GOOD: Critical CSS inline in <head> */
/* Keep this under 14KB for first packet */

/* ✅ GOOD: Use CSS containment for performance */
.card {
  contain: layout style paint;
}

.article-content {
  contain: layout style;
}

/* ✅ GOOD: Use content-visibility for off-screen content */
.section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px; /* Estimated height */
}

/* ✅ GOOD: Avoid expensive properties */
/* Fast properties: opacity, transform */
.fade-in {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.slide-in {
  transform: translateY(20px);
  transition: transform 0.3s ease;
}

/* ❌ SLOW: Avoid animating layout properties */
/* Avoid: width, height, top, left, margin, padding */
```

**2.4 JavaScript Optimization**

```bash
# Analyze bundle with bundled script
python scripts/bundle_analyzer.py --input dist/bundle.js

# Tree-shaking and minification (Webpack example)
# webpack.config.js
```

JavaScript optimization patterns:
```javascript
// ✅ GOOD: Code splitting with dynamic imports
const LazyComponent = () => {
  const [Component, setComponent] = React.useState(null);

  React.useEffect(() => {
    import('./HeavyComponent.js').then(module => {
      setComponent(() => module.default);
    });
  }, []);

  return Component ? <Component /> : <div>Loading...</div>;
};

// ✅ GOOD: Route-based code splitting
const routes = [
  {
    path: '/dashboard',
    component: () => import('./pages/Dashboard.js')
  },
  {
    path: '/profile',
    component: () => import('./pages/Profile.js')
  }
];

// ✅ GOOD: Tree-shakeable imports
import { debounce } from 'lodash-es'; // ✅ Good
// import _ from 'lodash'; // ❌ Bad - imports entire library

// ✅ GOOD: Async script loading
function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.async = true;
    script.onload = resolve;
    script.onerror = reject;
    document.body.appendChild(script);
  });
}

// Load non-critical scripts after page load
window.addEventListener('load', () => {
  loadScript('/js/analytics.js');
  loadScript('/js/chat-widget.js');
});

// ✅ GOOD: Intersection Observer for lazy loading
const lazyLoadObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const element = entry.target;
      // Load content
      element.src = element.dataset.src;
      lazyLoadObserver.unobserve(element);
    }
  });
});

document.querySelectorAll('[data-src]').forEach(el => {
  lazyLoadObserver.observe(el);
});
```

### Phase 3: Lazy Loading Implementation

**3.1 Native Lazy Loading**
```html
<!-- Images -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- Iframes -->
<iframe src="video.html" loading="lazy" title="Video"></iframe>
```

**3.2 Advanced Lazy Loading**
```javascript
// Lazy load images with blur-up effect
class ImageLazyLoader {
  constructor() {
    this.observer = new IntersectionObserver(
      this.handleIntersection.bind(this),
      { rootMargin: '50px' }
    );
  }

  observe(image) {
    this.observer.observe(image);
  }

  handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        const src = img.dataset.src;
        const srcset = img.dataset.srcset;

        // Create new image to preload
        const tempImg = new Image();

        tempImg.onload = () => {
          if (srcset) img.srcset = srcset;
          img.src = src;
          img.classList.add('loaded');
        };

        tempImg.src = src;
        this.observer.unobserve(img);
      }
    });
  }
}

// Usage
const lazyLoader = new ImageLazyLoader();
document.querySelectorAll('img[data-src]').forEach(img => {
  lazyLoader.observe(img);
});
```

```css
/* Blur-up effect */
img[data-src] {
  filter: blur(10px);
  transition: filter 0.3s ease;
}

img[data-src].loaded {
  filter: blur(0);
}
```

**3.3 Lazy Loading Components/Sections**
```javascript
// Lazy load entire sections of the page
class SectionLazyLoader {
  constructor() {
    this.observer = new IntersectionObserver(
      this.handleIntersection.bind(this),
      { rootMargin: '200px' }
    );
  }

  observe(section) {
    this.observer.observe(section);
  }

  handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const section = entry.target;
        const componentName = section.dataset.component;

        // Dynamically load component
        import(`./components/${componentName}.js`)
          .then(module => {
            module.default.render(section);
          });

        this.observer.unobserve(section);
      }
    });
  }
}
```

### Phase 4: Caching Strategy

**4.1 HTTP Caching Headers**
```nginx
# nginx configuration
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ {
  expires 1y;
  add_header Cache-Control "public, immutable";
}

location ~* \.(html)$ {
  expires 0;
  add_header Cache-Control "no-cache";
}
```

**4.2 Service Worker Caching**
```javascript
// service-worker.js
const CACHE_NAME = 'v1';
const STATIC_ASSETS = [
  '/',
  '/css/main.css',
  '/js/main.js',
  '/fonts/main.woff2'
];

// Install - cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
});

// Fetch - serve from cache, fallback to network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});

// Activate - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    })
  );
});
```

**4.3 Cache Strategies**
```javascript
// Cache-first (for static assets)
async function cacheFirst(request) {
  const cached = await caches.match(request);
  return cached || fetch(request);
}

// Network-first (for API calls)
async function networkFirst(request) {
  try {
    const response = await fetch(request);
    const cache = await caches.open(CACHE_NAME);
    cache.put(request, response.clone());
    return response;
  } catch (error) {
    return caches.match(request);
  }
}

// Stale-while-revalidate (for frequent updates)
async function staleWhileRevalidate(request) {
  const cached = await caches.match(request);
  const fetchPromise = fetch(request).then(response => {
    const cache = caches.open(CACHE_NAME);
    cache.then(c => c.put(request, response.clone()));
    return response;
  });
  return cached || fetchPromise;
}
```

### Phase 5: Critical Rendering Path Optimization

**5.1 Eliminate Render-Blocking Resources**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- ✅ Inline critical CSS -->
  <style>
    /* Critical above-the-fold styles */
    body { margin: 0; font-family: system-ui, sans-serif; }
    .header { height: 60px; background: #333; }
    .hero { min-height: 400px; }
  </style>

  <!-- ✅ Preload critical resources -->
  <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/images/hero.jpg" as="image">

  <!-- ✅ Async non-critical CSS -->
  <link rel="preload" href="/css/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="/css/styles.css"></noscript>

  <!-- ✅ DNS prefetch for third-party domains -->
  <link rel="dns-prefetch" href="https://analytics.example.com">
  <link rel="preconnect" href="https://cdn.example.com" crossorigin>
</head>
<body>
  <!-- Content -->

  <!-- ✅ Defer JavaScript -->
  <script src="/js/main.js" defer></script>

  <!-- ✅ Async for independent scripts -->
  <script src="/js/analytics.js" async></script>
</body>
</html>
```

**5.2 Resource Hints**
```html
<!-- DNS Prefetch: Resolve DNS early -->
<link rel="dns-prefetch" href="https://fonts.googleapis.com">

<!-- Preconnect: Establish connection early -->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Prefetch: Load resource for next navigation -->
<link rel="prefetch" href="/pages/about.html">

<!-- Preload: Load resource for current page -->
<link rel="preload" href="/css/critical.css" as="style">

<!-- Prerender: Render entire page in background (use sparingly) -->
<link rel="prerender" href="/pages/next.html">
```

### Phase 6: Monitoring and Continuous Optimization

**6.1 Real User Monitoring (RUM)**
```javascript
// Web Vitals monitoring
import { onCLS, onFID, onLCP, onINP, onFCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    id: metric.id,
    delta: metric.delta,
    rating: metric.rating
  });

  // Use sendBeacon to ensure data is sent
  navigator.sendBeacon('/analytics', body);
}

// Monitor all Web Vitals
onCLS(sendToAnalytics);
onFID(sendToAnalytics);
onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

**6.2 Performance Observer API**
```javascript
// Monitor long tasks
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.warn('Long task detected:', {
      duration: entry.duration,
      startTime: entry.startTime
    });
  }
});

observer.observe({ entryTypes: ['longtask'] });

// Monitor resource timing
const resourceObserver = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.duration > 1000) {
      console.warn('Slow resource:', entry.name, entry.duration);
    }
  }
});

resourceObserver.observe({ entryTypes: ['resource'] });

// Monitor navigation timing
const navigationObserver = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log('Navigation timing:', {
      dns: entry.domainLookupEnd - entry.domainLookupStart,
      tcp: entry.connectEnd - entry.connectStart,
      request: entry.responseStart - entry.requestStart,
      response: entry.responseEnd - entry.responseStart,
      dom: entry.domContentLoadedEventEnd - entry.responseEnd,
      load: entry.loadEventEnd - entry.loadEventStart
    });
  }
});

navigationObserver.observe({ entryTypes: ['navigation'] });
```

**6.3 Automated Performance Testing**
```javascript
// Using bundled performance_monitor.js
import { PerformanceMonitor } from './scripts/performance_monitor.js';

const monitor = new PerformanceMonitor({
  thresholds: {
    lcp: 2500,
    fid: 100,
    cls: 0.1,
    fcp: 1800,
    ttfb: 600
  },
  onThresholdExceeded: (metric) => {
    console.error(`Performance threshold exceeded: ${metric.name} = ${metric.value}`);
  }
});

monitor.start();
```

## Bundled Resources

### Scripts

**performance_auditor.py**
Comprehensive performance audit tool that analyzes:
- Core Web Vitals scores
- Resource sizes and counts
- Render-blocking resources
- Caching opportunities
- Image optimization needs
- Third-party script impact

```bash
python scripts/performance_auditor.py --url https://example.com
```

**image_optimizer.py**
Batch image optimization tool:
- Converts images to WebP and AVIF
- Generates responsive image sets
- Compresses images with quality control
- Preserves metadata (optional)
- Generates HTML picture elements

```bash
python scripts/image_optimizer.py --input ./images --output ./optimized --quality 85
```

**bundle_analyzer.py**
JavaScript bundle analysis tool:
- Identifies large dependencies
- Detects duplicate code
- Suggests code-splitting opportunities
- Analyzes tree-shaking effectiveness
- Reports bundle composition

```bash
python scripts/bundle_analyzer.py --input dist/bundle.js --format html
```

**css_optimizer.py**
CSS optimization tool:
- Removes unused styles
- Minifies CSS
- Identifies critical CSS
- Suggests optimization opportunities
- Validates CSS performance best practices

```bash
python scripts/css_optimizer.py --input styles.css --html index.html
```

**cache_validator.py**
Validates caching configuration:
- Checks cache headers
- Validates service worker setup
- Identifies uncached resources
- Suggests cache strategies
- Tests cache effectiveness

```bash
python scripts/cache_validator.py --url https://example.com
```

### References

**core_web_vitals_guide.md**
Comprehensive guide to understanding and optimizing Core Web Vitals, including:
- Detailed metric explanations
- Measurement techniques
- Optimization strategies for each metric
- Real-world case studies
- Common pitfalls and solutions

**image_optimization_guide.md**
Deep dive into image optimization:
- Format comparison (JPEG, PNG, WebP, AVIF)
- Compression techniques
- Responsive images best practices
- Art direction with picture element
- Lazy loading strategies
- CDN integration

**javascript_performance_guide.md**
JavaScript performance optimization:
- Code splitting strategies
- Tree-shaking and dead code elimination
- Minification and compression
- Async and defer strategies
- Web Workers for heavy computation
- Performance profiling techniques

**caching_strategies_guide.md**
Comprehensive caching guide:
- HTTP caching headers explained
- Service Worker strategies
- Cache-first vs Network-first
- Stale-while-revalidate pattern
- CDN caching configuration
- Cache invalidation strategies

**critical_rendering_path_guide.md**
Understanding and optimizing the critical rendering path:
- Browser rendering process
- Render-blocking resources
- Critical CSS extraction
- Resource prioritization
- Preloading strategies
- PRPL pattern

## Common Patterns

### Pattern 1: Progressive Image Loading

```html
<div class="progressive-image" data-src="/images/full.jpg">
  <img
    class="progressive-image__placeholder"
    src="/images/placeholder-tiny.jpg"
    alt="Description">
  <img
    class="progressive-image__full"
    data-src="/images/full.jpg"
    alt="Description">
</div>

<style>
.progressive-image {
  position: relative;
  overflow: hidden;
}

.progressive-image__placeholder {
  filter: blur(20px);
  transform: scale(1.1);
  width: 100%;
}

.progressive-image__full {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.progressive-image__full.loaded {
  opacity: 1;
}
</style>

<script>
const progressiveImages = document.querySelectorAll('.progressive-image');

progressiveImages.forEach(container => {
  const fullImg = container.querySelector('.progressive-image__full');
  const src = fullImg.dataset.src;

  const img = new Image();
  img.onload = () => {
    fullImg.src = src;
    fullImg.classList.add('loaded');
  };
  img.src = src;
});
</script>
```

### Pattern 2: Lazy Load with Intersection Observer

```javascript
class LazyLoader {
  constructor(options = {}) {
    this.options = {
      rootMargin: '50px',
      threshold: 0.01,
      ...options
    };

    this.observer = new IntersectionObserver(
      this.handleIntersection.bind(this),
      this.options
    );
  }

  observe(elements) {
    elements.forEach(el => this.observer.observe(el));
  }

  handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        this.loadElement(entry.target);
        this.observer.unobserve(entry.target);
      }
    });
  }

  loadElement(element) {
    if (element.tagName === 'IMG') {
      this.loadImage(element);
    } else if (element.tagName === 'IFRAME') {
      this.loadIframe(element);
    } else {
      this.loadBackground(element);
    }
  }

  loadImage(img) {
    const src = img.dataset.src;
    const srcset = img.dataset.srcset;

    if (srcset) img.srcset = srcset;
    if (src) img.src = src;

    img.classList.add('loaded');
  }

  loadIframe(iframe) {
    const src = iframe.dataset.src;
    if (src) iframe.src = src;
  }

  loadBackground(element) {
    const bg = element.dataset.bg;
    if (bg) element.style.backgroundImage = `url(${bg})`;
  }
}

// Usage
const lazyLoader = new LazyLoader({ rootMargin: '100px' });
lazyLoader.observe(document.querySelectorAll('[data-src]'));
```

### Pattern 3: Code Splitting with Dynamic Imports

```javascript
// Route-based code splitting
const routes = {
  '/': () => import('./pages/Home.js'),
  '/about': () => import('./pages/About.js'),
  '/contact': () => import('./pages/Contact.js')
};

async function loadRoute(path) {
  const loader = routes[path];
  if (!loader) return;

  try {
    const module = await loader();
    module.default.render();
  } catch (error) {
    console.error('Failed to load route:', error);
  }
}

// Component-based code splitting
class ComponentLoader {
  constructor() {
    this.cache = new Map();
  }

  async load(componentName) {
    if (this.cache.has(componentName)) {
      return this.cache.get(componentName);
    }

    try {
      const module = await import(`./components/${componentName}.js`);
      this.cache.set(componentName, module.default);
      return module.default;
    } catch (error) {
      console.error(`Failed to load component ${componentName}:`, error);
    }
  }
}

const loader = new ComponentLoader();

// Load on interaction
document.querySelector('.load-modal').addEventListener('click', async () => {
  const Modal = await loader.load('Modal');
  Modal.open();
});
```

### Pattern 4: Resource Prefetching

```javascript
// Prefetch on hover (for links)
const prefetchCache = new Set();

function prefetchPage(url) {
  if (prefetchCache.has(url)) return;

  const link = document.createElement('link');
  link.rel = 'prefetch';
  link.href = url;
  document.head.appendChild(link);

  prefetchCache.add(url);
}

document.querySelectorAll('a[data-prefetch]').forEach(link => {
  link.addEventListener('mouseenter', () => {
    prefetchPage(link.href);
  }, { once: true });
});

// Prefetch visible links
const linkObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const link = entry.target;
      prefetchPage(link.href);
      linkObserver.unobserve(link);
    }
  });
}, { rootMargin: '200px' });

document.querySelectorAll('a[data-prefetch-visible]').forEach(link => {
  linkObserver.observe(link);
});

// Prefetch on idle
if ('requestIdleCallback' in window) {
  requestIdleCallback(() => {
    document.querySelectorAll('a[data-prefetch-idle]').forEach(link => {
      prefetchPage(link.href);
    });
  });
}
```

### Pattern 5: Font Loading Optimization

```javascript
// Font loading with FontFace API
async function loadFonts() {
  const fonts = [
    new FontFace('Main Font', 'url(/fonts/main-regular.woff2)', {
      weight: '400',
      style: 'normal',
      display: 'swap'
    }),
    new FontFace('Main Font', 'url(/fonts/main-bold.woff2)', {
      weight: '700',
      style: 'normal',
      display: 'swap'
    })
  ];

  try {
    const loadedFonts = await Promise.all(
      fonts.map(font => font.load())
    );

    loadedFonts.forEach(font => {
      document.fonts.add(font);
    });

    document.documentElement.classList.add('fonts-loaded');
  } catch (error) {
    console.error('Font loading failed:', error);
  }
}

// Load fonts on page load
if (document.readyState === 'complete') {
  loadFonts();
} else {
  window.addEventListener('load', loadFonts);
}
```

```css
/* FOUT mitigation */
body {
  font-family: system-ui, -apple-system, sans-serif;
}

.fonts-loaded body {
  font-family: 'Main Font', system-ui, sans-serif;
}

/* Prevent layout shift */
@font-face {
  font-family: 'Main Font Fallback';
  src: local('Arial');
  ascent-override: 95%;
  descent-override: 25%;
  size-adjust: 105%;
}

body {
  font-family: 'Main Font Fallback', system-ui, sans-serif;
}

.fonts-loaded body {
  font-family: 'Main Font', 'Main Font Fallback', system-ui, sans-serif;
}
```

### Pattern 6: Third-Party Script Management

```javascript
// Delayed third-party script loading
class ThirdPartyManager {
  constructor() {
    this.loaded = new Set();
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    this.initialized = true;

    // Wait for user interaction or page load
    const events = ['scroll', 'mousedown', 'touchstart', 'keydown'];

    const loadScripts = () => {
      this.loadAll();
      events.forEach(event => {
        document.removeEventListener(event, loadScripts);
      });
    };

    events.forEach(event => {
      document.addEventListener(event, loadScripts, { once: true, passive: true });
    });

    // Fallback: load after 5 seconds
    setTimeout(loadScripts, 5000);
  }

  async load(name, src, options = {}) {
    if (this.loaded.has(name)) return;

    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = src;
      script.async = true;

      if (options.defer) script.defer = true;
      if (options.module) script.type = 'module';

      script.onload = () => {
        this.loaded.add(name);
        resolve();
      };

      script.onerror = reject;

      document.body.appendChild(script);
    });
  }

  async loadAll() {
    const scripts = [
      { name: 'analytics', src: '/js/analytics.js' },
      { name: 'chat', src: '/js/chat-widget.js' },
      { name: 'ads', src: '/js/ads.js' }
    ];

    await Promise.all(
      scripts.map(script => this.load(script.name, script.src))
    );
  }
}

const thirdPartyManager = new ThirdPartyManager();
thirdPartyManager.init();
```

## Best Practices

### Performance Budget

Establish and enforce performance budgets:

```json
{
  "budgets": {
    "javascript": {
      "total": 300,
      "warning": 250,
      "units": "KB"
    },
    "css": {
      "total": 100,
      "warning": 80,
      "units": "KB"
    },
    "images": {
      "total": 500,
      "warning": 400,
      "units": "KB"
    },
    "fonts": {
      "total": 100,
      "warning": 80,
      "units": "KB"
    },
    "metrics": {
      "fcp": {
        "target": 1500,
        "warning": 2000,
        "units": "ms"
      },
      "lcp": {
        "target": 2500,
        "warning": 3000,
        "units": "ms"
      },
      "tti": {
        "target": 3500,
        "warning": 4500,
        "units": "ms"
      },
      "cls": {
        "target": 0.1,
        "warning": 0.15,
        "units": "score"
      }
    }
  }
}
```

### Testing Checklist

- [ ] Test on real devices (not just emulators)
- [ ] Test on slow networks (throttle to 3G)
- [ ] Test with cache disabled
- [ ] Test on low-end devices
- [ ] Monitor performance in production
- [ ] Set up alerting for performance regressions
- [ ] Conduct regular performance audits
- [ ] A/B test performance optimizations

### Optimization Priority

1. **Critical Path** - Optimize what blocks initial render
2. **Above the Fold** - Prioritize visible content
3. **Core Functionality** - Ensure key features are fast
4. **Progressive Enhancement** - Layer on enhancements
5. **Below the Fold** - Lazy load non-critical content
6. **Nice-to-Have** - Defer optional features

### Browser Support

Target modern browsers with progressive enhancement:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Use feature detection for advanced features:
```javascript
// Check for Intersection Observer
if ('IntersectionObserver' in window) {
  // Use Intersection Observer for lazy loading
} else {
  // Fallback: load all images immediately
}

// Check for Service Worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}

// Check for modern image formats
const supportsWebP = document.createElement('canvas')
  .toDataURL('image/webp')
  .indexOf('data:image/webp') === 0;
```

### Performance Anti-Patterns

**❌ Avoid:**
- Synchronous scripts in `<head>` without defer/async
- Large hero images without optimization
- Loading all JavaScript upfront
- Blocking third-party scripts
- Animating layout properties (width, height, top, left)
- Large DOM trees (>1500 nodes)
- Deep nesting (>32 levels)
- Uncompressed assets
- No caching headers
- Missing image dimensions
- Loading fonts from slow CDNs
- Excessive polyfills
- Large dependencies for simple tasks

**✅ Do:**
- Use defer/async for scripts
- Optimize and compress all images
- Code split by route/component
- Lazy load third-party scripts
- Animate with transform and opacity
- Keep DOM lightweight
- Flatten component hierarchy
- Compress all assets (gzip/brotli)
- Set aggressive cache headers
- Always specify image dimensions
- Self-host critical fonts
- Only polyfill what's needed
- Use lightweight alternatives

## Troubleshooting

### Issue: Poor LCP Score

**Symptoms:** LCP > 2.5s

**Common causes:**
1. Large, unoptimized images
2. Render-blocking CSS/JS
3. Slow server response time
4. Client-side rendering delay

**Solutions:**
```bash
# 1. Optimize images
python scripts/image_optimizer.py --input ./images

# 2. Check for render-blocking resources
python scripts/performance_auditor.py --url https://yoursite.com | grep "render-blocking"

# 3. Extract and inline critical CSS
# Manually identify critical CSS and inline in <head>

# 4. Preload LCP image
```
```html
<link rel="preload" as="image" href="/hero.jpg" fetchpriority="high">
```

### Issue: High CLS Score

**Symptoms:** CLS > 0.1

**Common causes:**
1. Images without dimensions
2. Dynamic content insertion
3. Web fonts causing layout shift
4. Ads without reserved space

**Solutions:**
```html
<!-- Always set dimensions -->
<img src="image.jpg" width="800" height="600" alt="Description">

<!-- Reserve space for dynamic content -->
<div style="min-height: 250px;">
  <!-- Dynamic content loads here -->
</div>

<!-- Use font-display: swap with fallback matching -->
<style>
@font-face {
  font-family: 'Main Font';
  src: url('/fonts/main.woff2') format('woff2');
  font-display: swap;
}
</style>
```

### Issue: Slow Time to Interactive (TTI)

**Symptoms:** TTI > 3.5s, poor FID/INP

**Common causes:**
1. Large JavaScript bundles
2. Long-running JavaScript tasks
3. Heavy third-party scripts
4. Excessive DOM manipulation

**Solutions:**
```bash
# 1. Analyze bundle
python scripts/bundle_analyzer.py --input dist/bundle.js

# 2. Implement code splitting
# Use dynamic imports for routes and heavy components

# 3. Defer third-party scripts
# Load after user interaction
```

```javascript
// Break up long tasks
function processInChunks(items, processItem) {
  const chunks = [];
  for (let i = 0; i < items.length; i += 100) {
    chunks.push(items.slice(i, i + 100));
  }

  function processChunk(index) {
    if (index >= chunks.length) return;

    chunks[index].forEach(processItem);

    requestIdleCallback(() => processChunk(index + 1));
  }

  processChunk(0);
}
```

### Issue: Large Bundle Size

**Symptoms:** JavaScript > 300KB

**Solutions:**
```bash
# 1. Analyze what's in the bundle
python scripts/bundle_analyzer.py --input dist/bundle.js --format html

# 2. Check for duplicate dependencies
npm dedupe

# 3. Use tree-shakeable imports
# ✅ import { debounce } from 'lodash-es'
# ❌ import _ from 'lodash'

# 4. Implement code splitting
# Use dynamic imports for routes and features
```

### Issue: Slow Image Loading

**Symptoms:** Images block LCP, slow page load

**Solutions:**
```bash
# 1. Optimize all images
python scripts/image_optimizer.py --input ./images --quality 85

# 2. Implement responsive images
# Use srcset and sizes attributes

# 3. Use modern formats
# Convert to WebP/AVIF with fallbacks

# 4. Implement lazy loading
# Use loading="lazy" for below-fold images

# 5. Use a CDN
# Serve images from CDN with automatic optimization
```

### Issue: Font Loading Delay

**Symptoms:** FOIT (Flash of Invisible Text) or FOUT (Flash of Unstyled Text)

**Solutions:**
```html
<!-- 1. Preload critical fonts -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>

<!-- 2. Use font-display: swap -->
<style>
@font-face {
  font-family: 'Main Font';
  src: url('/fonts/main.woff2') format('woff2');
  font-display: swap;
}
</style>

<!-- 3. Match fallback font metrics -->
<style>
@font-face {
  font-family: 'Main Font Fallback';
  src: local('Arial');
  ascent-override: 95%;
  descent-override: 25%;
  size-adjust: 105%;
}
</style>
```

### Issue: Excessive HTTP Requests

**Symptoms:** Many small resources, slow load time

**Solutions:**
```bash
# 1. Concatenate CSS/JS files
# Use build tools to bundle

# 2. Use HTTP/2 Server Push
# Or at least HTTP/2 multiplexing

# 3. Inline critical resources
# Inline critical CSS and small SVGs

# 4. Use CSS sprites for icons
# Or better: use SVG sprites or icon fonts

# 5. Implement resource bundling
# Bundle related resources together
```

## When to Use This Skill

**Use web-performance-optimization when:**
- Building a new website or application
- Core Web Vitals scores are poor
- Page load time is slow
- Users report sluggish interactions
- Bundle sizes are too large
- Images are not optimized
- No caching strategy is in place
- Third-party scripts slow down the site
- Planning a performance audit
- Setting up performance monitoring

**Combine with other skills:**
- Use with `html-static-design` for performance-optimized HTML structure
- Use with `css-layout-builder` for performant CSS layouts
- Use with `javascript-interactive-design` for optimized JavaScript interactions
- Use with `ui-component-design` for lazy-loaded components
- Use with `design-system-builder` for performance-first design systems

**Consider alternatives:**
- For simple static sites with few assets, basic optimization may be sufficient
- For server-side rendered apps, focus on server optimization alongside client-side
- For native apps, use platform-specific performance tools

## Performance Metrics Glossary

- **FCP (First Contentful Paint):** Time until first content appears (target: < 1.8s)
- **LCP (Largest Contentful Paint):** Time until largest content element appears (target: < 2.5s)
- **FID (First Input Delay):** Time from first user interaction to browser response (target: < 100ms)
- **INP (Interaction to Next Paint):** Responsiveness throughout page lifecycle (target: < 200ms)
- **CLS (Cumulative Layout Shift):** Visual stability during page load (target: < 0.1)
- **TTI (Time to Interactive):** Time until page is fully interactive (target: < 3.5s)
- **TTFB (Time to First Byte):** Server response time (target: < 600ms)
- **TBT (Total Blocking Time):** Time main thread is blocked (target: < 200ms)
- **SI (Speed Index):** How quickly content is visually displayed (target: < 3.4s)

## Additional Resources

For more detailed information, see the bundled references:
- `references/core_web_vitals_guide.md` - Comprehensive Core Web Vitals documentation
- `references/image_optimization_guide.md` - Advanced image optimization techniques
- `references/javascript_performance_guide.md` - JavaScript performance deep dive
- `references/caching_strategies_guide.md` - Complete caching implementation guide
- `references/critical_rendering_path_guide.md` - Critical path optimization strategies

Use the bundled scripts for automated optimization:
- `scripts/performance_auditor.py` - Comprehensive performance audit
- `scripts/image_optimizer.py` - Batch image optimization
- `scripts/bundle_analyzer.py` - JavaScript bundle analysis
- `scripts/css_optimizer.py` - CSS optimization and cleanup
- `scripts/cache_validator.py` - Cache configuration validation
