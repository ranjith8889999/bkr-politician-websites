/* =============================================
   B KISHORE REDDY - MAIN JAVASCRIPT
   ============================================= */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initPreloader();
    initNavbar();
    initParticles();
    initScrollAnimations();
    initCounter();
    initGallery();
    initForms();
    initScrollTop();
});

// =============================================
// PRELOADER
// =============================================
function initPreloader() {
    const preloader = document.getElementById('preloader');
    
    window.addEventListener('load', function() {
        setTimeout(function() {
            preloader.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }, 1000);
    });
}

// =============================================
// NAVBAR
// =============================================
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Mobile menu toggle
    navToggle.addEventListener('click', function() {
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
    });
    
    // Close menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });
    
    // Active link on scroll
    window.addEventListener('scroll', function() {
        let current = '';
        const sections = document.querySelectorAll('section[id]');
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (window.scrollY >= sectionTop - 100) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// =============================================
// PARTICLES BACKGROUND - ENHANCED
// =============================================
function initParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;
    
    // Create multiple types of particles
    const particleCount = 60;
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(particlesContainer, i);
    }
    
    // Add floating geometric shapes
    createFloatingShapes(particlesContainer);
    
    // Add glowing orbs
    createGlowingOrbs(particlesContainer);
    
    // Add connecting lines effect
    initMouseParallax();
}

function createParticle(container, index) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    const size = Math.random() * 10 + 3;
    const left = Math.random() * 100;
    const top = Math.random() * 100;
    const duration = Math.random() * 15 + 10;
    const delay = Math.random() * 5;
    
    // Alternate between circle and star shapes
    const isCircle = index % 3 !== 0;
    const opacity = Math.random() * 0.3 + 0.1;
    
    if (isCircle) {
        particle.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: rgba(255, 255, 255, ${opacity});
            border-radius: 50%;
            left: ${left}%;
            top: ${top}%;
            animation: floatParticle ${duration}s ease-in-out infinite;
            animation-delay: ${delay}s;
            pointer-events: none;
        `;
    } else {
        // Star/sparkle particle
        particle.innerHTML = '✦';
        particle.style.cssText = `
            position: absolute;
            left: ${left}%;
            top: ${top}%;
            color: rgba(255, 153, 51, ${opacity + 0.2});
            font-size: ${size + 5}px;
            animation: floatParticle ${duration}s ease-in-out infinite, pulse 2s ease-in-out infinite;
            animation-delay: ${delay}s;
            pointer-events: none;
        `;
    }
    
    container.appendChild(particle);
}

function createFloatingShapes(container) {
    const shapes = ['◇', '○', '△', '□'];
    const colors = ['rgba(255, 107, 53, 0.2)', 'rgba(255, 153, 51, 0.2)', 'rgba(255, 255, 255, 0.1)'];
    
    for (let i = 0; i < 8; i++) {
        const shape = document.createElement('div');
        shape.className = 'floating-shape';
        shape.innerHTML = shapes[i % shapes.length];
        
        const size = Math.random() * 30 + 20;
        const left = Math.random() * 100;
        const top = Math.random() * 100;
        const duration = Math.random() * 20 + 15;
        
        shape.style.cssText = `
            position: absolute;
            left: ${left}%;
            top: ${top}%;
            font-size: ${size}px;
            color: ${colors[i % colors.length]};
            animation: float ${duration}s ease-in-out infinite, rotate ${duration * 2}s linear infinite;
            pointer-events: none;
            opacity: 0.5;
        `;
        
        container.appendChild(shape);
    }
}

function createGlowingOrbs(container) {
    for (let i = 0; i < 5; i++) {
        const orb = document.createElement('div');
        orb.className = 'glowing-orb';
        
        const size = Math.random() * 150 + 100;
        const left = Math.random() * 100;
        const top = Math.random() * 100;
        const duration = Math.random() * 10 + 8;
        const hue = i % 2 === 0 ? '20' : '30'; // Orange hues
        
        orb.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            background: radial-gradient(circle, hsla(${hue}, 100%, 60%, 0.15) 0%, transparent 70%);
            border-radius: 50%;
            left: ${left}%;
            top: ${top}%;
            animation: float ${duration}s ease-in-out infinite, pulse ${duration / 2}s ease-in-out infinite;
            pointer-events: none;
            filter: blur(20px);
        `;
        
        container.appendChild(orb);
    }
}

function initMouseParallax() {
    const heroContent = document.querySelector('.hero-content');
    const heroImage = document.querySelector('.hero-image');
    
    if (!heroContent) return;
    
    document.addEventListener('mousemove', (e) => {
        const x = (window.innerWidth / 2 - e.clientX) / 50;
        const y = (window.innerHeight / 2 - e.clientY) / 50;
        
        if (heroImage) {
            heroImage.style.transform = `translateX(${x}px) translateY(${y}px)`;
        }
        
        // Move particles slightly
        const particles = document.querySelectorAll('.floating-shape');
        particles.forEach((p, i) => {
            const speed = (i + 1) * 0.5;
            p.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
        });
    });
}

// =============================================
// SCROLL ANIMATIONS
// =============================================
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                
                // Stagger animation for grid items
                if (entry.target.parentElement.classList.contains('stagger-animation')) {
                    entry.target.parentElement.classList.add('animated');
                }
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// =============================================
// COUNTER ANIMATION - ENHANCED
// =============================================
function initCounter() {
    const counters = document.querySelectorAll('.stat-number');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-count'));
                
                // Add stagger delay based on index
                const index = Array.from(counters).indexOf(counter);
                setTimeout(() => {
                    animateCounter(counter, target);
                }, index * 200);
                
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => {
        observer.observe(counter);
    });
}

function animateCounter(element, target) {
    const duration = 2500;
    const frameDuration = 1000 / 60;
    const totalFrames = Math.round(duration / frameDuration);
    let frame = 0;
    
    // Easing function for smooth animation
    const easeOutQuart = (t) => 1 - Math.pow(1 - t, 4);
    
    element.classList.add('counting');
    
    const timer = setInterval(() => {
        frame++;
        const progress = easeOutQuart(frame / totalFrames);
        const current = Math.round(target * progress);
        
        // Add flip animation class periodically
        if (frame % 10 === 0) {
            element.style.transform = 'scale(1.1)';
            setTimeout(() => {
                element.style.transform = 'scale(1)';
            }, 100);
        }
        
        element.textContent = formatNumber(current);
        
        if (frame >= totalFrames) {
            element.textContent = formatNumber(target);
            element.classList.remove('counting');
            
            // Add celebration effect
            createCounterCelebration(element);
            clearInterval(timer);
        }
    }, frameDuration);
}

function createCounterCelebration(element) {
    const rect = element.getBoundingClientRect();
    const colors = ['#ff6b35', '#ff9933', '#ffffff'];
    
    for (let i = 0; i < 8; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            left: ${rect.left + rect.width / 2}px;
            top: ${rect.top}px;
            width: 8px;
            height: 8px;
            background: ${colors[i % colors.length]};
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            animation: confettiFall 1s ease-out forwards;
        `;
        
        const angle = (i / 8) * Math.PI * 2;
        const velocity = 50 + Math.random() * 50;
        const tx = Math.cos(angle) * velocity;
        const ty = Math.sin(angle) * velocity - 30;
        
        confetti.style.setProperty('--tx', tx + 'px');
        confetti.style.setProperty('--ty', ty + 'px');
        
        document.body.appendChild(confetti);
        
        setTimeout(() => confetti.remove(), 1000);
    }
}

function formatNumber(num) {
    if (num >= 1000) {
        return (num / 1000).toFixed(0) + 'K+';
    }
    return num + '+';
}

// =============================================
// GALLERY & LIGHTBOX
// =============================================
function initGallery() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = lightbox?.querySelector('.lightbox-image');
    const lightboxClose = lightbox?.querySelector('.lightbox-close');
    const lightboxPrev = lightbox?.querySelector('.lightbox-prev');
    const lightboxNext = lightbox?.querySelector('.lightbox-next');
    
    let currentIndex = 0;
    let visibleItems = [];
    
    // Filter functionality
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            
            galleryItems.forEach(item => {
                if (filter === 'all' || item.getAttribute('data-category') === filter) {
                    item.style.display = 'block';
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'scale(1)';
                    }, 100);
                } else {
                    item.style.opacity = '0';
                    item.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        item.style.display = 'none';
                    }, 300);
                }
            });
            
            updateVisibleItems();
        });
    });
    
    // Lightbox functionality
    function updateVisibleItems() {
        visibleItems = Array.from(galleryItems).filter(item => 
            item.style.display !== 'none'
        );
    }
    
    updateVisibleItems();
    
    galleryItems.forEach((item, index) => {
        item.addEventListener('click', function() {
            updateVisibleItems();
            currentIndex = visibleItems.indexOf(this);
            openLightbox(this.querySelector('img').src);
        });
    });
    
    function openLightbox(src) {
        if (!lightbox) return;
        lightboxImage.src = src;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    function closeLightbox() {
        if (!lightbox) return;
        lightbox.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
    
    function showPrev() {
        currentIndex = (currentIndex - 1 + visibleItems.length) % visibleItems.length;
        lightboxImage.src = visibleItems[currentIndex].querySelector('img').src;
    }
    
    function showNext() {
        currentIndex = (currentIndex + 1) % visibleItems.length;
        lightboxImage.src = visibleItems[currentIndex].querySelector('img').src;
    }
    
    if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
    if (lightboxPrev) lightboxPrev.addEventListener('click', showPrev);
    if (lightboxNext) lightboxNext.addEventListener('click', showNext);
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (!lightbox?.classList.contains('active')) return;
        
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') showPrev();
        if (e.key === 'ArrowRight') showNext();
    });
    
    // Close on overlay click
    lightbox?.addEventListener('click', function(e) {
        if (e.target === lightbox) closeLightbox();
    });
}

// =============================================
// FORMS
// =============================================
function initForms() {
    const contactForm = document.getElementById('contactForm');
    const volunteerForm = document.getElementById('volunteerForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', handleFormSubmit);
    }
    
    if (volunteerForm) {
        volunteerForm.addEventListener('submit', handleFormSubmit);
    }
}

function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    submitBtn.disabled = true;
    
    // Simulate form submission
    setTimeout(() => {
        // Create mailto link for simple email sending
        const subject = data.subject || 'New Form Submission';
        const body = Object.entries(data)
            .map(([key, value]) => `${key}: ${value}`)
            .join('\n');
        
        // For real implementation, you would use EmailJS or a backend service
        // window.location.href = `mailto:ranjith888999@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        
        showNotification('Thank you! Your message has been sent successfully.', 'success');
        form.reset();
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 1500);
}

// =============================================
// NOTIFICATION
// =============================================
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// =============================================
// SCROLL TO TOP
// =============================================
function initScrollTop() {
    const scrollTopBtn = document.getElementById('scrollTop');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 500) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    });
    
    scrollTopBtn?.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// =============================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// =============================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// =============================================
// TYPING EFFECT (Optional)
// =============================================
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// =============================================
// LAZY LOADING IMAGES
// =============================================
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// =============================================
// ADD CSS FOR NOTIFICATIONS
// =============================================
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(notificationStyles);
