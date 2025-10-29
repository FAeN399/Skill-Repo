# Image Optimization Guide

## Overview

Images typically account for 50-70% of total page weight. Proper image optimization is one of the most impactful performance improvements you can make.

## Image Formats

### JPEG
**Best for:** Photographs, complex images with many colors

**Pros:**
- Excellent compression for photos
- Universal browser support
- Adjustable quality levels

**Cons:**
- No transparency support
- Lossy compression
- Not ideal for graphics with sharp edges

**Optimization:**
```bash
# Using ImageMagick
convert input.jpg -quality 85 -sampling-factor 4:2:0 -strip output.jpg

# Progressive JPEG for better perceived performance
convert input.jpg -quality 85 -interlace Plane output.jpg
```

**Recommended settings:**
- Quality: 80-85% for most photos
- Use progressive encoding
- Strip metadata
- Use 4:2:0 chroma subsampling

### PNG
**Best for:** Graphics, logos, images requiring transparency

**Pros:**
- Lossless compression
- Supports transparency
- Great for simple graphics

**Cons:**
- Larger file sizes than JPEG for photos
- Not ideal for complex images

**Optimization:**
```bash
# Using pngquant (lossy)
pngquant --quality=80-90 input.png -o output.png

# Using optipng (lossless)
optipng -o7 input.png
```

**Recommended settings:**
- Use PNG-8 for simple graphics (256 colors or less)
- Use pngquant for 70-80% size reduction with minimal quality loss
- Strip unnecessary metadata

### WebP
**Best for:** Modern browsers, balance of quality and file size

**Pros:**
- 25-35% smaller than JPEG at same quality
- Supports transparency
- Both lossy and lossless modes
- Wide browser support (95%+)

**Cons:**
- Not supported in IE11 and older browsers
- Slightly more CPU intensive to decode

**Optimization:**
```bash
# Using cwebp
cwebp -q 85 input.jpg -o output.webp

# Lossless WebP
cwebp -lossless input.png -o output.webp
```

**HTML implementation:**
```html
<picture>
  <source type="image/webp" srcset="image.webp">
  <img src="image.jpg" alt="Fallback">
</picture>
```

### AVIF
**Best for:** Next-generation format for maximum compression

**Pros:**
- 40-50% smaller than JPEG at same quality
- Better compression than WebP
- Supports HDR and wide color gamut
- Transparency support

**Cons:**
- Encoding is slow
- Browser support still growing (~85%)
- More CPU intensive to decode

**Optimization:**
```bash
# Using avif encoder
avifenc --min 20 --max 25 input.jpg output.avif
```

**HTML implementation:**
```html
<picture>
  <source type="image/avif" srcset="image.avif">
  <source type="image/webp" srcset="image.webp">
  <img src="image.jpg" alt="Fallback">
</picture>
```

### SVG
**Best for:** Logos, icons, simple graphics

**Pros:**
- Infinitely scalable
- Very small file sizes for simple graphics
- Searchable and accessible
- Styleable with CSS

**Cons:**
- Not suitable for photos
- Can be large for complex illustrations

**Optimization:**
```bash
# Using SVGO
svgo input.svg -o output.svg

# Or with precision
svgo --precision 2 input.svg -o output.svg
```

## Format Comparison

| Format | Photo (800KB) | Logo (50KB PNG) | Browser Support |
|--------|---------------|-----------------|-----------------|
| JPEG | 150KB (81% savings) | Not ideal | 100% |
| PNG | 800KB (baseline) | 50KB (baseline) | 100% |
| WebP | 100KB (87% savings) | 15KB (70% savings) | 95%+ |
| AVIF | 75KB (91% savings) | 10KB (80% savings) | 85%+ |
| SVG | Not suitable | 5KB (90% savings) | 100% |

## Responsive Images

### Basic Responsive Images
```html
<!-- Different sizes for different viewports -->
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w,
          image-800.jpg 800w,
          image-1200.jpg 1200w,
          image-1600.jpg 1600w"
  sizes="(max-width: 640px) 100vw,
         (max-width: 1024px) 50vw,
         800px"
  alt="Description">
```

### Art Direction
```html
<!-- Different crops for different viewports -->
<picture>
  <source media="(max-width: 640px)"
          srcset="image-mobile-400.jpg 1x,
                  image-mobile-800.jpg 2x">
  <source media="(max-width: 1024px)"
          srcset="image-tablet-600.jpg 1x,
                  image-tablet-1200.jpg 2x">
  <img src="image-desktop-1200.jpg"
       srcset="image-desktop-2400.jpg 2x"
       alt="Description">
</picture>
```

### Modern Formats with Responsive Sizes
```html
<picture>
  <!-- AVIF with responsive sizes -->
  <source type="image/avif"
          srcset="image-400.avif 400w,
                  image-800.avif 800w,
                  image-1200.avif 1200w"
          sizes="(max-width: 640px) 100vw, 800px">

  <!-- WebP with responsive sizes -->
  <source type="image/webp"
          srcset="image-400.webp 400w,
                  image-800.webp 800w,
                  image-1200.webp 1200w"
          sizes="(max-width: 640px) 100vw, 800px">

  <!-- JPEG fallback with responsive sizes -->
  <img src="image-800.jpg"
       srcset="image-400.jpg 400w,
               image-800.jpg 800w,
               image-1200.jpg 1200w"
       sizes="(max-width: 640px) 100vw, 800px"
       alt="Description"
       loading="lazy">
</picture>
```

## Lazy Loading

### Native Lazy Loading
```html
<!-- Simple lazy loading -->
<img src="image.jpg" loading="lazy" alt="Description">

<!-- Eager loading for above-fold images -->
<img src="hero.jpg" loading="eager" alt="Hero">

<!-- Auto (default browser behavior) -->
<img src="image.jpg" loading="auto" alt="Description">
```

### JavaScript Lazy Loading
```javascript
// Intersection Observer for custom lazy loading
const imageObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;

      if (img.dataset.srcset) {
        img.srcset = img.dataset.srcset;
      }

      img.classList.add('loaded');
      observer.unobserve(img);
    }
  });
}, {
  rootMargin: '50px' // Start loading 50px before entering viewport
});

// Observe all lazy images
document.querySelectorAll('img[data-src]').forEach(img => {
  imageObserver.observe(img);
});
```

### Blur-up Technique
```html
<div class="progressive-image">
  <!-- Tiny placeholder (inline or very small file) -->
  <img class="placeholder"
       src="tiny-placeholder.jpg"
       alt="Description">

  <!-- Full-size image -->
  <img class="full"
       data-src="full-image.jpg"
       alt="Description">
</div>
```

```css
.progressive-image {
  position: relative;
  overflow: hidden;
}

.progressive-image .placeholder {
  filter: blur(10px);
  transform: scale(1.1);
  transition: opacity 0.3s;
}

.progressive-image .full {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  opacity: 0;
  transition: opacity 0.3s;
}

.progressive-image .full.loaded {
  opacity: 1;
}

.progressive-image .full.loaded ~ .placeholder {
  opacity: 0;
}
```

## Image Sizing Strategy

### Recommended Sizes
```
Mobile (portrait):  400w, 800w (2x)
Mobile (landscape): 600w, 1200w (2x)
Tablet:            800w, 1600w (2x)
Desktop:           1200w, 2400w (2x)
Large Desktop:     1600w, 3200w (2x)
```

### Calculating Sizes Attribute
```html
<!-- Full width on mobile, 50% on tablet, 33% on desktop -->
<img
  srcset="image-400.jpg 400w,
          image-800.jpg 800w,
          image-1200.jpg 1200w"
  sizes="(max-width: 640px) 100vw,
         (max-width: 1024px) 50vw,
         33vw"
  alt="Description">
```

### Density Descriptors (x)
```html
<!-- For fixed-size images -->
<img
  srcset="image.jpg 1x,
          image@2x.jpg 2x,
          image@3x.jpg 3x"
  alt="Description">
```

## Background Images

### CSS Background Images
```css
/* Basic optimization */
.hero {
  background-image: url('hero-800.jpg');
}

@media (min-width: 1024px) {
  .hero {
    background-image: url('hero-1200.jpg');
  }
}

@media (min-width: 1920px) {
  .hero {
    background-image: url('hero-1600.jpg');
  }
}

/* Modern formats with fallback */
.hero {
  background-image: url('hero.jpg');
  background-image: image-set(
    url('hero.avif') type('image/avif'),
    url('hero.webp') type('image/webp'),
    url('hero.jpg') type('image/jpeg')
  );
}

/* Resolution-based */
.hero {
  background-image: image-set(
    url('hero-1x.jpg') 1x,
    url('hero-2x.jpg') 2x
  );
}
```

### JavaScript-based Loading
```javascript
// Lazy load background images
const bgObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const element = entry.target;
      const imageUrl = element.dataset.bg;

      // Preload image
      const img = new Image();
      img.onload = () => {
        element.style.backgroundImage = `url(${imageUrl})`;
        element.classList.add('loaded');
      };
      img.src = imageUrl;

      bgObserver.unobserve(element);
    }
  });
});

document.querySelectorAll('[data-bg]').forEach(el => {
  bgObserver.observe(el);
});
```

## CDN and Delivery

### Image CDN Services
- **Cloudinary**: On-the-fly transformations, automatic format selection
- **Imgix**: Real-time image processing, responsive images
- **CloudFlare Images**: Automatic optimization and delivery
- **AWS CloudFront + Lambda@Edge**: Custom image processing
- **Vercel Image Optimization**: Automatic WebP/AVIF conversion

### CDN URL Parameters
```html
<!-- Cloudinary example -->
<img src="https://res.cloudinary.com/demo/image/upload/w_400,f_auto,q_auto/sample.jpg">

<!-- Parameters:
     w_400 = width 400px
     f_auto = automatic format (WebP/AVIF if supported)
     q_auto = automatic quality
-->
```

### Self-Hosted with Cache Headers
```nginx
# nginx configuration
location ~* \.(jpg|jpeg|png|gif|webp|avif)$ {
  expires 1y;
  add_header Cache-Control "public, immutable";
  add_header Vary "Accept";

  # Enable AVIF/WebP conversion (requires modules)
  # image_filter_webp on;
}
```

## Performance Checklist

### Image Optimization Checklist
- [ ] Use modern formats (AVIF, WebP) with fallbacks
- [ ] Implement responsive images with `srcset` and `sizes`
- [ ] Compress images (80-85% quality for JPEG)
- [ ] Use appropriate formats (JPEG for photos, PNG for graphics, SVG for logos)
- [ ] Lazy load below-fold images
- [ ] Set explicit `width` and `height` to prevent CLS
- [ ] Use CDN for image delivery
- [ ] Preload critical above-fold images
- [ ] Strip unnecessary metadata
- [ ] Implement blur-up or LQIP for better UX
- [ ] Use progressive JPEG encoding
- [ ] Optimize SVGs with SVGO
- [ ] Set `fetchpriority="high"` for LCP images
- [ ] Use `loading="eager"` for above-fold images
- [ ] Set `decoding="async"` for non-critical images

### Testing Tools
- **Lighthouse**: Overall image optimization score
- **WebPageTest**: Detailed image analysis
- **Chrome DevTools**: Network tab for image sizes
- **ImageOptim**: Mac app for image compression
- **Squoosh**: Web-based image compressor
- **SVGOMG**: Online SVG optimizer

## Advanced Techniques

### Client Hints
```html
<!-- Enable client hints -->
<meta http-equiv="Accept-CH" content="DPR, Width, Viewport-Width">
```

```nginx
# Server responds with optimized images based on hints
# (Requires server-side implementation)
```

### HTTP/2 Server Push
```
Link: </images/hero.jpg>; rel=preload; as=image
```

### Image Preloading
```html
<!-- Preload LCP image -->
<link rel="preload" as="image" href="hero.jpg" fetchpriority="high">

<!-- Preload responsive image -->
<link rel="preload"
      as="image"
      href="hero-800.jpg"
      imagesrcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1200.jpg 1200w"
      imagesizes="100vw">
```

### Low Quality Image Placeholder (LQIP)
```javascript
// Generate base64 LQIP at build time
const lqip = 'data:image/jpeg;base64,/9j/4AAQSkZJRg...'; // Tiny 20x20 image

const img = `
  <img src="${lqip}"
       data-src="full-image.jpg"
       alt="Description"
       class="lazy">
`;
```

## Real-World Examples

### E-commerce Product Images
```html
<picture>
  <!-- Mobile: 400x400 -->
  <source media="(max-width: 640px)"
          type="image/avif"
          srcset="product-400.avif 1x, product-800.avif 2x">
  <source media="(max-width: 640px)"
          type="image/webp"
          srcset="product-400.webp 1x, product-800.webp 2x">

  <!-- Desktop: 600x600 -->
  <source type="image/avif"
          srcset="product-600.avif 1x, product-1200.avif 2x">
  <source type="image/webp"
          srcset="product-600.webp 1x, product-1200.webp 2x">

  <img src="product-600.jpg"
       srcset="product-1200.jpg 2x"
       width="600"
       height="600"
       alt="Product name"
       loading="lazy">
</picture>
```

### Hero Images
```html
<!-- Hero should load eagerly with high priority -->
<link rel="preload" as="image" href="hero-1200.avif" fetchpriority="high">

<picture>
  <source type="image/avif"
          srcset="hero-600.avif 600w,
                  hero-1200.avif 1200w,
                  hero-2400.avif 2400w"
          sizes="100vw">
  <source type="image/webp"
          srcset="hero-600.webp 600w,
                  hero-1200.webp 1200w,
                  hero-2400.webp 2400w"
          sizes="100vw">
  <img src="hero-1200.jpg"
       srcset="hero-600.jpg 600w,
               hero-1200.jpg 1200w,
               hero-2400.jpg 2400w"
       sizes="100vw"
       width="1200"
       height="600"
       alt="Hero image"
       loading="eager"
       fetchpriority="high">
</picture>
```

## Conclusion

Image optimization is an ongoing process. Regularly audit your images, test new formats as browser support improves, and monitor the impact on Core Web Vitals, especially LCP and CLS.
