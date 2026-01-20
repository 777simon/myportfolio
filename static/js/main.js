// ===================================
// SIMON'S PORTFOLIO ANIMATOR
// Responsive & Dynamic Animations
// ===================================

class PortfolioAnimator {
  constructor() {
    this.init();
  }

  init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.start());
    } else {
      this.start();
    }
  }

  start() {
    console.log('🚀 Portfolio Animator Started!');
    this.animateProfile();
    this.animateMainCard();
    this.animateSocials();
    this.setupScrollAnimations();
    this.addInteractivity();
    this.addParallax();
  }

  // ========== PROFILE CARD ANIMATION ==========
  animateProfile() {
    const profileWrapper = document.getElementById('profile-wrapper');
    const profilePic = document.getElementById('profile-pic');
    
    if (!profileWrapper || !profilePic) return;

    // Animate profile wrapper entrance
    profileWrapper.style.opacity = '0';
    profileWrapper.style.transform = 'scale(0.9) translateY(-20px)';
    
    setTimeout(() => {
      profileWrapper.style.transition = 'all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
      profileWrapper.style.opacity = '1';
      profileWrapper.style.transform = 'scale(1) translateY(0)';
    }, 100);

    // Add continuous floating to profile pic
    setTimeout(() => {
      profilePic.style.animation = 'float 3s ease-in-out infinite';
    }, 900);

    // Add glow effect on hover
    profilePic.addEventListener('mouseenter', function() {
      this.style.boxShadow = '0 0 30px rgba(102, 126, 234, 0.6)';
      this.style.transform = 'scale(1.1) rotate(5deg)';
    });

    profilePic.addEventListener('mouseleave', function() {
      this.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.1)';
      this.style.transform = 'scale(1) rotate(0deg)';
    });
  }

  // ========== MAIN CONTENT CARD ANIMATION ==========
  animateMainCard() {
    const mainCard = document.querySelector('.col-md-9 .card');
    const mainTitle = document.querySelector('.col-md-9 h4');
    const paragraphs = document.querySelectorAll('.col-md-9 p');
    
    if (!mainCard) return;

    // Animate main card
    mainCard.style.opacity = '0';
    mainCard.style.transform = 'translateX(30px)';
    
    setTimeout(() => {
      mainCard.style.transition = 'all 0.8s ease-out';
      mainCard.style.opacity = '1';
      mainCard.style.transform = 'translateX(0)';
    }, 300);

    // Animate title with gradient effect
    if (mainTitle) {
      mainTitle.style.opacity = '0';
      mainTitle.style.transform = 'translateY(20px)';
      
      setTimeout(() => {
        mainTitle.style.transition = 'all 0.6s ease-out';
        mainTitle.style.opacity = '1';
        mainTitle.style.transform = 'translateY(0)';
        
        // Add gradient text effect
        this.addGradientText(mainTitle);
      }, 700);
    }

    // Animate paragraphs with stagger
    paragraphs.forEach((p, index) => {
      p.style.opacity = '0';
      p.style.transform = 'translateY(15px)';
      
      setTimeout(() => {
        p.style.transition = 'all 0.6s ease-out';
        p.style.opacity = '1';
        p.style.transform = 'translateY(0)';
      }, 1000 + (index * 200));
    });
  }

  // ========== SOCIAL LINKS ANIMATION ==========
  animateSocials() {
    const socialLinks = document.querySelectorAll('.social-links li');
    
    socialLinks.forEach((link, index) => {
      const img = link.querySelector('img');
      
      link.style.opacity = '0';
      link.style.transform = 'scale(0) rotate(-180deg)';
      
      setTimeout(() => {
        link.style.transition = 'all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        link.style.opacity = '1';
        link.style.transform = 'scale(1) rotate(0deg)';
      }, 1800 + (index * 100));

      // Add bouncy hover effect
      link.addEventListener('mouseenter', function() {
        img.style.transition = 'all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        img.style.transform = 'scale(1.4) rotate(10deg)';
      });

      link.addEventListener('mouseleave', function() {
        img.style.transform = 'scale(1) rotate(0deg)';
      });
    });
  }

  // ========== SCROLL ANIMATIONS ==========
  setupScrollAnimations() {
    const cards = document.querySelectorAll('.row:not(:first-child) .card');
    
    if (!cards.length) return;

    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const card = entry.target;
          const delay = Array.from(cards).indexOf(card) * 150;
          
          setTimeout(() => {
            card.style.transition = 'all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0) scale(1)';
          }, delay);
          
          observer.unobserve(card);
        }
      });
    }, observerOptions);

    // Set initial state and observe
    cards.forEach(card => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(40px) scale(0.95)';
      observer.observe(card);
    });
  }

  // ========== INTERACTIVE EFFECTS ==========
  addInteractivity() {
    const allCards = document.querySelectorAll('.card');
    
    allCards.forEach(card => {
      // Add magnetic effect to cards
      card.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const moveX = (x - centerX) / 20;
        const moveY = (y - centerY) / 20;
        
        this.style.transform = `perspective(1000px) rotateX(${-moveY}deg) rotateY(${moveX}deg) translateZ(10px)`;
      });

      card.addEventListener('mouseleave', function() {
        this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
      });
    });

    // Add ripple effect to cards on click
    allCards.forEach(card => {
      card.addEventListener('click', function(e) {
        const ripple = document.createElement('div');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
          position: absolute;
          width: ${size}px;
          height: ${size}px;
          border-radius: 50%;
          background: rgba(102, 126, 234, 0.3);
          left: ${x}px;
          top: ${y}px;
          pointer-events: none;
          animation: ripple 0.6s ease-out;
        `;
        
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
      });
    });

    // Add smooth section titles animation
    const sectionTitles = document.querySelectorAll('h5');
    sectionTitles.forEach(title => {
      title.addEventListener('mouseenter', function() {
        this.style.transform = 'translateX(10px)';
        this.style.color = '#667eea';
      });

      title.addEventListener('mouseleave', function() {
        this.style.transform = 'translateX(0)';
        this.style.color = '#333';
      });
    });
  }

  // ========== PARALLAX EFFECT ==========
  addParallax() {
    let scrolled = 0;
    
    window.addEventListener('scroll', () => {
      scrolled = window.pageYOffset;
      
      const profileWrapper = document.getElementById('profile-wrapper');
      if (profileWrapper) {
        const speed = scrolled * 0.3;
        profileWrapper.style.transform = `translateY(${speed}px)`;
      }
    });
  }

  // ========== GRADIENT TEXT EFFECT ==========
  addGradientText(element) {
    element.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)';
    element.style.backgroundSize = '200% auto';
    element.style.color = 'transparent';
    element.style.backgroundClip = 'text';
    element.style.webkitBackgroundClip = 'text';
    element.style.animation = 'gradient-shift 3s ease infinite';
  }

  // ========== TYPING EFFECT ==========
  typeText(element, text, speed = 50) {
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
}

// ========== UTILITY FUNCTIONS ==========

// Add CSS animations if not present
function injectAnimations() {
  if (document.getElementById('custom-animations')) return;
  
  const style = document.createElement('style');
  style.id = 'custom-animations';
  style.textContent = `
    @keyframes ripple {
      0% {
        transform: scale(0);
        opacity: 1;
      }
      100% {
        transform: scale(2);
        opacity: 0;
      }
    }
    
    @keyframes float {
      0%, 100% {
        transform: translateY(0px);
      }
      50% {
        transform: translateY(-12px);
      }
    }
    
    @keyframes gradient-shift {
      0%, 100% {
        background-position: 0% center;
      }
      50% {
        background-position: 100% center;
      }
    }
    
    .card {
      transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    
    h5 {
      transition: all 0.3s ease !important;
    }
  `;
  document.head.appendChild(style);
}

// ========== INITIALIZE ==========
injectAnimations();
const animator = new PortfolioAnimator();

// Add smooth scroll for any anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

console.log('✨ Portfolio fully loaded and animated!');