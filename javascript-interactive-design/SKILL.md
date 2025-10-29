---
name: javascript-interactive-design
description: Add interactivity and dynamic behavior to web designs using vanilla JavaScript. Handles animations, user interactions, form validation, DOM manipulation, event handling, and progressive enhancement without frameworks.
---

# JavaScript Interactive Design

Transform static designs into interactive experiences using vanilla JavaScript. Add animations, handle user interactions, validate forms, and create dynamic UI behaviors.

## Overview

This skill adds interactivity to existing designs:
- Event-driven interactions (clicks, hovers, scrolls)
- Smooth animations and transitions
- Form validation and submission handling
- DOM manipulation and dynamic content
- Modal dialogs, tooltips, dropdowns
- Image galleries and carousels
- Progressive enhancement patterns
- Vanilla JavaScript (no frameworks)

## Usage

Trigger this skill with queries like:
- "Add click interaction to [element]"
- "Create a modal dialog with JavaScript"
- "Build an image carousel"
- "Add form validation"
- "Implement smooth scroll navigation"
- "Create an interactive dropdown menu"
- "Add animations on scroll"

### Development Process

**Step 1: Analyze Existing Design**
- Review HTML structure
- Identify interactive elements
- Plan interaction flows
- Consider accessibility

**Step 2: Plan Interactions**
- Define user actions (click, scroll, hover)
- Map expected behaviors
- Plan animations and transitions
- Consider mobile interactions

**Step 3: Implement JavaScript**
- Add event listeners
- Implement interaction logic
- Add animations
- Test across devices

## Common Interactive Patterns

### Modal Dialog
```javascript
class Modal {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);
    this.closeBtn = this.modal.querySelector('.modal-close');
    this.init();
  }

  init() {
    this.closeBtn.addEventListener('click', () => this.close());
    this.modal.addEventListener('click', (e) => {
      if (e.target === this.modal) this.close();
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen()) this.close();
    });
  }

  open() {
    this.modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    this.modal.setAttribute('aria-hidden', 'false');
    this.closeBtn.focus();
  }

  close() {
    this.modal.classList.remove('active');
    document.body.style.overflow = '';
    this.modal.setAttribute('aria-hidden', 'true');
  }

  isOpen() {
    return this.modal.classList.contains('active');
  }
}

// Usage
const modal = new Modal('myModal');
document.getElementById('openBtn').addEventListener('click', () => modal.open());
```

### Form Validation
```javascript
class FormValidator {
  constructor(formId) {
    this.form = document.getElementById(formId);
    this.errors = {};
    this.init();
  }

  init() {
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));

    // Real-time validation
    this.form.querySelectorAll('input, textarea').forEach(field => {
      field.addEventListener('blur', () => this.validateField(field));
      field.addEventListener('input', () => this.clearError(field));
    });
  }

  validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    let error = null;

    if (field.required && !value) {
      error = 'This field is required';
    } else if (type === 'email' && !this.isValidEmail(value)) {
      error = 'Please enter a valid email';
    } else if (field.minLength && value.length < field.minLength) {
      error = `Minimum ${field.minLength} characters required`;
    }

    if (error) {
      this.showError(field, error);
      return false;
    }
    return true;
  }

  showError(field, message) {
    this.clearError(field);
    this.errors[field.name] = message;

    field.classList.add('error');
    field.setAttribute('aria-invalid', 'true');

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.id = `${field.id}-error`;

    field.setAttribute('aria-describedby', errorDiv.id);
    field.parentNode.appendChild(errorDiv);
  }

  clearError(field) {
    field.classList.remove('error');
    field.removeAttribute('aria-invalid');
    field.removeAttribute('aria-describedby');

    const errorDiv = field.parentNode.querySelector('.error-message');
    if (errorDiv) errorDiv.remove();

    delete this.errors[field.name];
  }

  isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  handleSubmit(e) {
    e.preventDefault();

    // Validate all fields
    let isValid = true;
    this.form.querySelectorAll('input, textarea').forEach(field => {
      if (!this.validateField(field)) isValid = false;
    });

    if (isValid) {
      // Form is valid, submit data
      const formData = new FormData(this.form);
      console.log('Form submitted:', Object.fromEntries(formData));
      // Handle submission (AJAX, etc.)
    }
  }
}

// Usage
new FormValidator('contactForm');
```

### Smooth Scroll Navigation
```javascript
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const targetId = this.getAttribute('href');

    if (targetId === '#') return;

    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      targetElement.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });

      // Update URL without jumping
      history.pushState(null, null, targetId);

      // Focus target for accessibility
      targetElement.setAttribute('tabindex', '-1');
      targetElement.focus();
    }
  });
});
```

### Dropdown Menu
```javascript
class Dropdown {
  constructor(element) {
    this.dropdown = element;
    this.toggle = this.dropdown.querySelector('.dropdown-toggle');
    this.menu = this.dropdown.querySelector('.dropdown-menu');
    this.isOpen = false;
    this.init();
  }

  init() {
    this.toggle.addEventListener('click', () => this.toggleMenu());

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!this.dropdown.contains(e.target) && this.isOpen) {
        this.close();
      }
    });

    // Keyboard navigation
    this.toggle.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.toggleMenu();
      }
    });
  }

  toggleMenu() {
    this.isOpen ? this.close() : this.open();
  }

  open() {
    this.menu.classList.add('active');
    this.toggle.setAttribute('aria-expanded', 'true');
    this.isOpen = true;
  }

  close() {
    this.menu.classList.remove('active');
    this.toggle.setAttribute('aria-expanded', 'false');
    this.isOpen = false;
  }
}

// Initialize all dropdowns
document.querySelectorAll('.dropdown').forEach(el => new Dropdown(el));
```

### Scroll Animations
```javascript
class ScrollAnimator {
  constructor() {
    this.elements = document.querySelectorAll('[data-animate]');
    this.observer = null;
    this.init();
  }

  init() {
    // Use Intersection Observer for performance
    this.observer = new IntersectionObserver(
      (entries) => this.handleIntersection(entries),
      {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
      }
    );

    this.elements.forEach(el => this.observer.observe(el));
  }

  handleIntersection(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const animationType = entry.target.dataset.animate;
        entry.target.classList.add('animated', animationType);
        this.observer.unobserve(entry.target);
      }
    });
  }
}

// Usage
new ScrollAnimator();
```

### Image Carousel
```javascript
class Carousel {
  constructor(carouselId) {
    this.carousel = document.getElementById(carouselId);
    this.track = this.carousel.querySelector('.carousel-track');
    this.slides = Array.from(this.track.children);
    this.currentIndex = 0;
    this.init();
  }

  init() {
    // Create navigation buttons
    this.createControls();

    // Auto-play
    this.startAutoPlay();

    // Pause on hover
    this.carousel.addEventListener('mouseenter', () => this.stopAutoPlay());
    this.carousel.addEventListener('mouseleave', () => this.startAutoPlay());

    // Touch swipe support
    this.addSwipeSupport();
  }

  createControls() {
    const prevBtn = document.createElement('button');
    prevBtn.className = 'carousel-btn prev';
    prevBtn.innerHTML = '&larr;';
    prevBtn.addEventListener('click', () => this.prev());

    const nextBtn = document.createElement('button');
    nextBtn.className = 'carousel-btn next';
    nextBtn.innerHTML = '&rarr;';
    nextBtn.addEventListener('click', () => this.next());

    this.carousel.appendChild(prevBtn);
    this.carousel.appendChild(nextBtn);
  }

  goToSlide(index) {
    this.currentIndex = (index + this.slides.length) % this.slides.length;
    const offset = -this.currentIndex * 100;
    this.track.style.transform = `translateX(${offset}%)`;

    // Update aria-live for screen readers
    this.carousel.setAttribute('aria-live', 'polite');
  }

  next() {
    this.goToSlide(this.currentIndex + 1);
  }

  prev() {
    this.goToSlide(this.currentIndex - 1);
  }

  startAutoPlay() {
    this.autoPlayInterval = setInterval(() => this.next(), 5000);
  }

  stopAutoPlay() {
    clearInterval(this.autoPlayInterval);
  }

  addSwipeSupport() {
    let startX = 0;

    this.track.addEventListener('touchstart', (e) => {
      startX = e.touches[0].clientX;
    });

    this.track.addEventListener('touchend', (e) => {
      const endX = e.changedTouches[0].clientX;
      const diff = startX - endX;

      if (Math.abs(diff) > 50) {
        diff > 0 ? this.next() : this.prev();
      }
    });
  }
}

// Usage
new Carousel('myCarousel');
```

## Bundled Resources

### Scripts

**`scripts/js_minifier.py`** - Minifies JavaScript code for production
- Removes comments and whitespace
- Basic variable name shortening
- Outputs minified .min.js file

Usage:
```bash
python scripts/js_minifier.py script.js
```

**`scripts/event_debugger.py`** - Analyzes event listeners in code
- Lists all event types used
- Identifies potential memory leaks
- Suggests optimizations

Usage:
```bash
python scripts/event_debugger.py script.js
```

### References

**`references/vanilla_js_patterns.md`** - Common vanilla JavaScript patterns and anti-patterns

**`references/dom_manipulation.md`** - Efficient DOM manipulation techniques

**`references/event_handling.md`** - Event handling best practices and delegation patterns

**`references/animation_performance.md`** - High-performance animation techniques using requestAnimationFrame

**`references/accessibility_javascript.md`** - JavaScript accessibility patterns (ARIA, keyboard navigation, focus management)

## Best Practices

**Event Handling**
- Use event delegation for dynamic elements
- Remove event listeners when elements are removed
- Use passive event listeners for scroll/touch events
- Throttle/debounce expensive operations

**DOM Manipulation**
- Batch DOM updates to minimize reflows
- Use DocumentFragment for multiple insertions
- Cache DOM queries in variables
- Use classList instead of className manipulation

**Performance**
- Use Intersection Observer for scroll-based animations
- Prefer requestAnimationFrame for animations
- Avoid layout thrashing
- Use Web Workers for heavy computations

**Accessibility**
- Add ARIA attributes for dynamic content
- Manage focus appropriately
- Ensure keyboard navigation works
- Provide alternative text for visual changes

**Progressive Enhancement**
- Start with semantic HTML
- Add JavaScript as enhancement
- Graceful degradation for older browsers
- Feature detection over browser detection

## Animation Techniques

### CSS + JavaScript Combo
```javascript
// Trigger CSS animations with JavaScript
element.classList.add('animate');

// Wait for animation to complete
element.addEventListener('animationend', () => {
  element.classList.remove('animate');
}, { once: true });
```

### RequestAnimationFrame
```javascript
function animate() {
  element.style.transform = `translateX(${position}px)`;
  position += speed;

  if (position < maxPosition) {
    requestAnimationFrame(animate);
  }
}

requestAnimationFrame(animate);
```

## Troubleshooting

**Events not firing**
- Check element exists before adding listener
- Verify event type spelling
- Check if event propagation was stopped
- Use event delegation for dynamic content

**Memory leaks**
- Remove event listeners when done
- Clear intervals and timeouts
- Remove references to DOM elements
- Use WeakMap for element associations

**Animation janky**
- Use transform and opacity (GPU accelerated)
- Avoid animating layout properties
- Use requestAnimationFrame
- Check for layout thrashing

**Accessibility issues**
- Test with keyboard only
- Add proper ARIA attributes
- Manage focus correctly
- Test with screen reader

## When to Use This Skill

Use javascript-interactive-design when:
- Adding interactivity to static designs
- Building UI components without frameworks
- Need lightweight, vanilla JavaScript solutions
- Progressive enhancement required
- Performance is critical

Choose other skills for:
- Initial HTML/CSS structure (use html-static-design)
- Complex layouts (use css-layout-builder)
- Reusable component libraries (use ui-component-design)
- Complete design systems (use design-system-builder)

## Browser Support

Modern JavaScript features:
- ES6+ syntax (arrow functions, classes, etc.)
- IntersectionObserver API
- classList API
- requestAnimationFrame
- addEventListener

For older browser support, consider transpiling with Babel.
