// Portfolio Text Animator
// Add this script to your Django templates

class PortfolioAnimator {
  constructor() {
    this.observers = [];
    this.init();
  }

  init() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setupAnimations());
    } else {
      this.setupAnimations();
    }
  }

  setupAnimations() {
    this.animateHeroText();
    this.animateMainTitle();
    this.animateParagraphs();
    this.addHoverEffects();
    this.setupScrollAnimations();
  }

  // Animate the hero section "Hi, I'm Simon!"
  animateHeroText() {
    const heroTitle = document.querySelector('.hero-title, h1');
    const heroSubtitle = document.querySelector('.hero-subtitle, .tagline');
    
    if (heroTitle && heroTitle.textContent.includes("Hi, I'm Simon!")) {
      heroTitle.style.opacity = '0';
      heroTitle.style.transform = 'translateY(-30px)';
      heroTitle.style.transition = 'all 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
      
      setTimeout(() => {
        heroTitle.style.opacity = '1';
        heroTitle.style.transform = 'translateY(0)';
      }, 200);
    }

    if (heroSubtitle) {
      heroSubtitle.style.opacity = '0';
      heroSubtitle.style.transform = 'translateX(-20px)';
      heroSubtitle.style.transition = 'all 0.8s ease-out';
      
      setTimeout(() => {
        heroSubtitle.style.opacity = '1';
        heroSubtitle.style.transform = 'translateX(0)';
      }, 600);
    }
  }

  // Animate "My first programme as a developer" title
  animateMainTitle() {
    const titles = document.querySelectorAll('h1, h2, h3');
    
    titles.forEach((title, index) => {
      if (title.textContent.includes('My first programme') || 
          title.textContent.includes('Experience as a Developer')) {
        
        title.style.opacity = '0';
        title.style.transform = 'translateX(-50px)';
        title.style.transition = 'all 1s ease-out';
        
        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              setTimeout(() => {
                title.style.opacity = '1';
                title.style.transform = 'translateX(0)';
              }, index * 100);
              observer.unobserve(title);
            }
          });
        }, { threshold: 0.2 });
        
        observer.observe(title);
        this.observers.push(observer);
      }
    });
  }

  // Animate paragraphs with staggered fade-in
  animateParagraphs() {
    const paragraphs = document.querySelectorAll('p');
    
    paragraphs.forEach((p, index) => {
      p.style.opacity = '0';
      p.style.transform = 'translateY(20px)';
      p.style.transition = 'all 0.8s ease-out';
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              p.style.opacity = '1';
              p.style.transform = 'translateY(0)';
            }, index * 150);
            observer.unobserve(p);
          }
        });
      }, { threshold: 0.1 });
      
      observer.observe(p);
      this.observers.push(observer);
    });
  }

  // Add typing effect to specific text
  typeWriter(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    element.style.opacity = '1';
    
    const type = () => {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        i++;
        setTimeout(type, speed);
      }
    };
    
    type();
  }

  // Add hover effects to interactive elements
  addHoverEffects() {
    const links = document.querySelectorAll('a');
    const buttons = document.querySelectorAll('button');
    
    [...links, ...buttons].forEach(el => {
      el.style.transition = 'all 0.3s ease';
      
      el.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px)';
        this.style.filter = 'brightness(1.1)';
      });
      
      el.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.filter = 'brightness(1)';
      });
    });
  }

  // Setup scroll-triggered animations
  setupScrollAnimations() {
    const sections = document.querySelectorAll('section, .card, .content-block');
    
    sections.forEach((section, index) => {
      section.style.opacity = '0';
      section.style.transform = 'translateY(30px)';
      section.style.transition = 'all 0.8s ease-out';
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              section.style.opacity = '1';
              section.style.transform = 'translateY(0)';
            }, 100);
            observer.unobserve(section);
          }
        });
      }, { threshold: 0.15 });
      
      observer.observe(section);
      this.observers.push(observer);
    });
  }

  // Add gradient text animation
  addGradientTextAnimation(selector) {
    const elements = document.querySelectorAll(selector);
    
    elements.forEach(el => {
      el.style.background = 'linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%)';
      el.style.backgroundSize = '200% auto';
      el.style.color = 'transparent';
      el.style.backgroundClip = 'text';
      el.style.webkitBackgroundClip = 'text';
      el.style.animation = 'gradient-shift 3s ease infinite';
    });
    
    // Add keyframes if not already present
    if (!document.getElementById('gradient-animation-styles')) {
      const style = document.createElement('style');
      style.id = 'gradient-animation-styles';
      style.textContent = `
        @keyframes gradient-shift {
          0%, 100% { background-position: 0% center; }
          50% { background-position: 100% center; }
        }
        
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
        }
        
        @keyframes pulse-glow {
          0%, 100% { filter: brightness(1); }
          50% { filter: brightness(1.2); }
        }
      `;
      document.head.appendChild(style);
    }
  }

  // Add floating animation to profile image
  addFloatingAnimation(selector) {
    const elements = document.querySelectorAll(selector);
    
    elements.forEach(el => {
      el.style.animation = 'float 3s ease-in-out infinite';
    });
  }

  // Cleanup method
  destroy() {
    this.observers.forEach(observer => observer.disconnect());
    this.observers = [];
  }
}

// Initialize the animator
const portfolioAnimator = new PortfolioAnimator();

// Optional: Add gradient animation to the main title
setTimeout(() => {
  portfolioAnimator.addGradientTextAnimation('h1');
}, 1000);

// Optional: Add floating animation to profile picture
portfolioAnimator.addFloatingAnimation('.profile-image, img[alt*="Simon"]');

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PortfolioAnimator;
}