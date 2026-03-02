// UzLingKorpus - Main JavaScript

// ============= Header Scroll Animation =============
window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// ============= Quick Search Toggle =============
function toggleSearch() {
    const searchBar = document.getElementById('quickSearch');
    searchBar.classList.toggle('active');
    if (searchBar.classList.contains('active')) {
        const input = searchBar.querySelector('input');
        if (input) input.focus();
    }
}

// ============= Carousel =============
let currentSlide = 0;

function showSlide(n) {
    const slides = document.querySelectorAll('.carousel-slide');
    const dots = document.querySelectorAll('.dot');
    
    if (slides.length === 0) return;
    
    // Wrap around
    if (n >= slides.length) currentSlide = 0;
    else if (n < 0) currentSlide = slides.length - 1;
    else currentSlide = n;
    
    // Hide all slides
    slides.forEach(slide => {
        slide.classList.remove('active');
        slide.style.display = 'none';
    });
    
    // Remove active from all dots
    dots.forEach(dot => dot.classList.remove('active'));
    
    // Show current slide with animation
    if (slides[currentSlide]) {
        slides[currentSlide].style.display = 'block';
        setTimeout(() => {
            slides[currentSlide].classList.add('active');
        }, 10);
    }
    
    // Activate current dot
    if (dots[currentSlide]) {
        dots[currentSlide].classList.add('active');
    }
}

function moveCarousel(direction) {
    showSlide(currentSlide + direction);
}

function goToSlide(n) {
    showSlide(n);
}

// Initialize carousel on page load
document.addEventListener('DOMContentLoaded', () => {
    showSlide(0);
    
    // Auto-play carousel every 5 seconds
    setInterval(() => {
        const slides = document.querySelectorAll('.carousel-slide');
        if (slides.length > 0) {
            moveCarousel(1);
        }
    }, 5000);
});

// ============= Tabs =============
function switchTab(tabName) {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    // You can add logic here to show/hide different scholar groups
}

// ============= Smooth Scrolling =============
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// ============= Scroll Animation =============
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all sections
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
});

// ============= Header Scroll Effect =============
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.1)';
    } else {
        header.style.boxShadow = '0 6px 30px rgba(0,0,0,0.15)';
    }
    
    lastScroll = currentScroll;
});

// ============= Search Functionality =============
const searchInput = document.querySelector('.search-input');
if (searchInput) {
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const query = searchInput.value.trim();
            if (query) {
                window.location.href = `/konkordans?q=${encodeURIComponent(query)}`;
            }
        }
    });
}

// ============= Book Card Hover Effect =============
const bookCards = document.querySelectorAll('.book-card');
bookCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-8px) rotate(2deg)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) rotate(0)';
    });
});

// ============= Video Play =============
const videoThumbnails = document.querySelectorAll('.video-thumbnail');
videoThumbnails.forEach(thumbnail => {
    thumbnail.addEventListener('click', function() {
        // Here you can add logic to open video modal or redirect to video page
        console.log('Video clicked');
    });
});

// ============= Lazy Loading Images =============
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ============= Mobile Menu Toggle =============
const createMobileMenu = () => {
    if (window.innerWidth <= 768) {
        const nav = document.querySelector('.main-nav');
        if (!document.querySelector('.menu-toggle')) {
            const menuToggle = document.createElement('button');
            menuToggle.className = 'menu-toggle';
            menuToggle.innerHTML = '☰';
            menuToggle.style.cssText = 'background: none; border: none; color: white; font-size: 24px; cursor: pointer; display: block;';
            
            menuToggle.addEventListener('click', () => {
                nav.classList.toggle('active');
            });
            
            document.querySelector('.header-content').insertBefore(menuToggle, nav);
        }
    }
};

window.addEventListener('resize', createMobileMenu);
window.addEventListener('load', createMobileMenu);

console.log('UzLingKorpus initialized successfully!');