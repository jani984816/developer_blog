/* ===== NAVIGATION ===== */
const navbar = document.getElementById('navbar');
const navToggle = document.getElementById('nav-toggle');
const navLinks = document.getElementById('nav-links');
const allNavLinks = document.querySelectorAll('.nav-link');

// Scroll effect on navbar
window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
  updateActiveNavLink();
});

// Mobile menu toggle
navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

// Close mobile menu on link click
allNavLinks.forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
  });
});

// Active nav link based on scroll position
function updateActiveNavLink() {
  const sections = document.querySelectorAll('section[id]');
  const scrollPos = window.scrollY + 100;

  sections.forEach(section => {
    const top = section.offsetTop;
    const height = section.offsetHeight;
    const id = section.getAttribute('id');
    const link = document.querySelector(`.nav-link[href="#${id}"]`);

    if (scrollPos >= top && scrollPos < top + height) {
      allNavLinks.forEach(l => l.classList.remove('active'));
      if (link) link.classList.add('active');
    }
  });
}

/* ===== ROLE ROTATOR (Typewriter effect) ===== */
const roles = [
  'Full Stack Web Apps',
  'PHP & Laravel APIs',
  'React Dashboards',
  'Flutter Mobile Apps',
  'Angular Frontends',
  'Node.js Backends',
];

let roleIndex = 0;
let charIndex = 0;
let isDeleting = false;
const rotator = document.getElementById('role-rotator');
const typingSpeed = 80;
const deletingSpeed = 45;
const pauseDelay = 2000;

function typeRole() {
  const currentRole = roles[roleIndex];

  if (!isDeleting) {
    rotator.textContent = currentRole.substring(0, charIndex + 1);
    charIndex++;
    if (charIndex === currentRole.length) {
      isDeleting = true;
      setTimeout(typeRole, pauseDelay);
      return;
    }
  } else {
    rotator.textContent = currentRole.substring(0, charIndex - 1);
    charIndex--;
    if (charIndex === 0) {
      isDeleting = false;
      roleIndex = (roleIndex + 1) % roles.length;
    }
  }

  setTimeout(typeRole, isDeleting ? deletingSpeed : typingSpeed);
}

typeRole();

/* ===== INTERSECTION OBSERVER (Scroll animations) ===== */
const observerOptions = {
  threshold: 0.15,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      // Stagger animations for children
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, 0);
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

// Observe all animated elements
document.querySelectorAll('[data-aos]').forEach((el, index) => {
  el.style.transitionDelay = `${(index % 4) * 0.1}s`;
  observer.observe(el);
});

/* ===== SMOOTH SCROLL ===== */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

/* ===== STAT NUMBER COUNTER ANIMATION ===== */
function animateCounter(el, target, suffix = '') {
  const duration = 1500;
  const start = performance.now();
  const isDecimal = String(target).includes('.');

  const tick = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = eased * target;

    el.textContent = isDecimal
      ? current.toFixed(1) + suffix
      : Math.floor(current) + suffix;

    if (progress < 1) requestAnimationFrame(tick);
  };

  requestAnimationFrame(tick);
}

const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const statNumbers = entry.target.querySelectorAll('.stat-number');
      statNumbers.forEach(el => {
        const text = el.textContent;
        const numMatch = text.match(/[\d.]+/);
        const suffix = text.replace(/[\d.]+/, '').trim();
        if (numMatch) {
          animateCounter(el, parseFloat(numMatch[0]), suffix);
        }
      });
      statsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.hero-stats');
if (statsSection) statsObserver.observe(statsSection);

/* ===== CURSOR GLOW EFFECT ===== */
const glows = document.querySelectorAll('.glow');
let mouseX = 0;
let mouseY = 0;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});

/* ===== CARD TILT EFFECT ===== */
document.querySelectorAll('.project-card, .skill-category, .contact-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * -5;
    const rotateY = ((x - centerX) / centerX) * 5;

    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
  });
});

/* ===== INITIAL LOAD ANIMATION ===== */
window.addEventListener('load', () => {
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.5s ease';
  requestAnimationFrame(() => {
    document.body.style.opacity = '1';
  });

  // Animate hero content on load
  const heroElements = [
    document.querySelector('.hero-badge'),
    document.querySelector('.hero-title'),
    document.querySelector('.hero-role'),
    document.querySelector('.hero-description'),
    document.querySelector('.hero-cta'),
    document.querySelector('.hero-stats'),
  ];

  heroElements.forEach((el, i) => {
    if (!el) return;
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    setTimeout(() => {
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, 100 + i * 120);
  });

  const heroVisual = document.querySelector('.hero-visual');
  if (heroVisual) {
    heroVisual.style.opacity = '0';
    heroVisual.style.transform = 'translateX(30px)';
    heroVisual.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    setTimeout(() => {
      heroVisual.style.opacity = '1';
      heroVisual.style.transform = 'translateX(0)';
    }, 400);
  }
});
