// Main site script (module-compatible behavior). This file reproduces the
// behavior from your previous standalone HTML: particle network, custom
// cursor, magnetic buttons, typing effect, GSAP animations, mobile menu and
// contact form handling.

// Note: the base template includes an importmap for `three` so we can import it.
import * as THREE from 'three';

function safeQuery(selector) {
  return document.querySelector(selector);
}

document.addEventListener('DOMContentLoaded', () => {
  // ---------- Theme initialization (dark / light) ----------
  (function() {
    const STORAGE_KEY = 'site_theme';
    const saved = localStorage.getItem(STORAGE_KEY);
    const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
    const defaultTheme = saved || (prefersLight ? 'light' : 'dark');

    const applyTheme = (theme) => {
      if (theme === 'light') {
        document.body.classList.add('light-theme');
      } else {
        document.body.classList.remove('light-theme');
      }
      try { localStorage.setItem(STORAGE_KEY, theme); } catch (e) { /* ignore */ }
    };

    const toggle = document.getElementById('theme-toggle');
    if (toggle) {
      // set initial checked state
      toggle.checked = (defaultTheme === 'light');
      toggle.addEventListener('change', () => applyTheme(toggle.checked ? 'light' : 'dark'));
    }

    applyTheme(defaultTheme);
  })();

  // ---------- Particle Network (2D canvas) ----------
  const particleCanvas = safeQuery('#particle-network');
  if (particleCanvas && particleCanvas.getContext) {
    const pctx = particleCanvas.getContext('2d');

    function resizeCanvas() {
      particleCanvas.width = window.innerWidth;
      particleCanvas.height = window.innerHeight;
    }

    resizeCanvas();

    const particles = [];
    const particleCount = 80;

    class Particle {
      constructor() {
        this.x = Math.random() * particleCanvas.width;
        this.y = Math.random() * particleCanvas.height;
        this.vx = (Math.random() - 0.5) * 0.3;
        this.vy = (Math.random() - 0.5) * 0.3;
        this.radius = Math.random() * 1.2 + 0.5;
        this.color = `rgba(99, 102, 241, ${Math.random() * 0.3 + 0.1})`;
      }
      update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > particleCanvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > particleCanvas.height) this.vy *= -1;
      }
      draw() {
        pctx.beginPath();
        pctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        pctx.fillStyle = this.color;
        pctx.fill();
      }
    }

    for (let i = 0; i < particleCount; i++) particles.push(new Particle());

    function drawConnections() {
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          if (distance < 120) {
            pctx.beginPath();
            pctx.strokeStyle = `rgba(99, 102, 241, ${0.1 * (1 - distance / 120)})`;
            pctx.lineWidth = 0.3;
            pctx.moveTo(particles[i].x, particles[i].y);
            pctx.lineTo(particles[j].x, particles[j].y);
            pctx.stroke();
          }
        }
      }
    }

    function animateParticles() {
      pctx.clearRect(0, 0, particleCanvas.width, particleCanvas.height);
      for (const particle of particles) {
        particle.update();
        particle.draw();
      }
      drawConnections();
      requestAnimationFrame(animateParticles);
    }

    animateParticles();

    window.addEventListener('resize', resizeCanvas);
  }

  // ---------- Custom Cursor ----------
  const cursor = safeQuery('#cursor');
  const cursorFollower = safeQuery('#cursor-follower');
  const isTouch = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;

  if (!isTouch && cursor && cursorFollower) {
    // Activate custom cursor and use requestAnimationFrame + interpolation
    // for smooth movement (no setTimeout, no layout thrash).
    document.body.classList.add('custom-cursor-active');

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let cursorX = mouseX;
    let cursorY = mouseY;
    let followerX = mouseX;
    let followerY = mouseY;

    const onMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };

    document.addEventListener('mousemove', onMove, { passive: true });

    // animation loop: small cursor instant, follower eases for trailing
    const animate = () => {
      // cursor follows exactly (instant) for responsive feel
      cursorX = mouseX;
      cursorY = mouseY;

      // follower eases slower for trailing effect
      const fEase = 0.16;
      followerX += (mouseX - followerX) * fEase;
      followerY += (mouseY - followerY) * fEase;

      // apply transforms (translate3d to keep it GPU-accelerated)
      cursor.style.transform = `translate3d(${cursorX - 4}px, ${cursorY - 4}px, 0)`;
      cursorFollower.style.transform = `translate3d(${followerX - 17}px, ${followerY - 17}px, 0)`;

      requestAnimationFrame(animate);
    };

    requestAnimationFrame(animate);
  }

  // ---------- Magnetic Buttons ----------
  const magneticBtns = document.querySelectorAll('.magnetic-btn');
  magneticBtns.forEach(btn => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const deltaX = (x - centerX) / 4;
      const deltaY = (y - centerY) / 4;
      btn.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
      if (cursor) cursor.style.transform = 'scale(1.5)';
      if (cursorFollower) cursorFollower.style.transform = 'scale(1.2)';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'translate(0, 0)';
      if (cursor) cursor.style.transform = 'scale(1)';
      if (cursorFollower) cursorFollower.style.transform = 'scale(1)';
    });
  });

  // ---------- Mobile menu ----------
  const mobileMenuBtn = safeQuery('#mobile-menu-btn');
  const mobileMenu = safeQuery('#mobile-menu');
  const closeMobileMenu = safeQuery('#close-mobile-menu');

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.remove('translate-x-full');
    });
  }
  if (closeMobileMenu && mobileMenu) {
    closeMobileMenu.addEventListener('click', () => {
      mobileMenu.classList.add('translate-x-full');
    });
  }

  // ---------- Typing effect ----------
  const typingText = safeQuery('.typing-text');
  if (typingText) {
    const texts = [
      "Android Developer",
      "IoT Specialist",
      "Problem Solver",
      "Tech Innovator"
    ];
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
      const currentText = texts[textIndex];
      if (isDeleting) {
        typingText.textContent = currentText.substring(0, charIndex - 1);
        charIndex--;
      } else {
        typingText.textContent = currentText.substring(0, charIndex + 1);
        charIndex++;
      }
      if (!isDeleting && charIndex === currentText.length) {
        isDeleting = true;
        setTimeout(type, 2000);
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        textIndex = (textIndex + 1) % texts.length;
        setTimeout(type, 500);
      } else {
        setTimeout(type, isDeleting ? 100 : 150);
      }
    }
    type();
  }

  // ---------- GSAP Animations ----------
  try {
    if (window.gsap && window.gsap.registerPlugin && window.ScrollTrigger) {
      gsap.registerPlugin(ScrollTrigger);

      gsap.utils.toArray('.section-reveal').forEach(section => {
        gsap.fromTo(section, { opacity: 0, y: 50 }, {
          opacity: 1, y: 0, duration: 1,
          scrollTrigger: { trigger: section, start: 'top 80%', end: 'bottom 20%', toggleActions: 'play none none reverse' }
        });
      });

      gsap.utils.toArray('.glass').forEach((card, i) => {
        gsap.fromTo(card, { opacity: 0, scale: 0.9 }, {
          opacity: 1, scale: 1, duration: 0.8, delay: i * 0.1,
          scrollTrigger: { trigger: card, start: 'top 85%', toggleActions: 'play none none reverse' }
        });
      });
    }
  } catch (e) {
    // If GSAP isn't available, skip animations silently
    console.warn('GSAP animations skipped:', e);
  }

  // ---------- Contact form handling ----------
  // Let the browser submit the form to the Django view so the data
  // is saved to the database server-side. Do not intercept the submit
  // here; the view at `portfolio.views.home` will save and redirect.
  // If you prefer AJAX submission, we can implement a fetch-based
  // POST handler instead. For now, keep the default behavior.

  // ---------- Floating background elements ----------
  const floatingElements = document.querySelectorAll('.floating');
  if (floatingElements.length && window.gsap) {
    floatingElements.forEach(el => {
      gsap.to(el, {
        y: -10,
        duration: 2 + Math.random() * 2,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
      });
    });
  }

});

