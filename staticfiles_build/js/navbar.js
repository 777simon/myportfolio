// ===================================
// NAVBAR FUNCTIONALITY
// ===================================

class NavbarController {
  constructor() {
    this.navbar = document.getElementById('mainNavbar');
    this.mobileToggle = document.getElementById('mobileMenuToggle');
    this.mobileOverlay = document.getElementById('mobileMenuOverlay');
    this.mobileClose = document.getElementById('mobileMenuClose');
    this.scrollProgress = document.getElementById('scrollProgress');
    
    this.init();
  }

  init() {
    this.setupScrollEffects();
    this.setupMobileMenu();
    this.setupSmoothScroll();
    this.setupActiveLink();
    console.log('📱 Navbar initialized!');
  }

  // ========== SCROLL EFFECTS ==========
  setupScrollEffects() {
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
      const currentScroll = window.pageYOffset;
      
      // Add scrolled class
      if (currentScroll > 50) {
        this.navbar.classList.add('scrolled');
      } else {
        this.navbar.classList.remove('scrolled');
      }
      
      // Update progress bar
      this.updateProgressBar();
      
      // Hide navbar on scroll down, show on scroll up
      if (currentScroll > lastScroll && currentScroll > 100) {
        this.navbar.style.transform = 'translateY(-100%)';
      } else {
        this.navbar.style.transform = 'translateY(0)';
      }
      
      lastScroll = currentScroll;
    });
  }

  updateProgressBar() {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height);
    
    if (this.scrollProgress) {
      this.scrollProgress.style.transform = `scaleX(${scrolled})`;
    }
  }

  // ========== MOBILE MENU ==========
  setupMobileMenu() {
    if (!this.mobileToggle || !this.mobileOverlay) return;

    // Toggle mobile menu
    this.mobileToggle.addEventListener('click', () => {
      this.toggleMobileMenu();
    });

    // Close mobile menu
    if (this.mobileClose) {
      this.mobileClose.addEventListener('click', () => {
        this.closeMobileMenu();
      });
    }

    // Close on link click
    const mobileLinks = document.querySelectorAll('.mobile-nav-link, .mobile-btn-resume, .mobile-btn-hire');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        this.closeMobileMenu();
      });
    });

    // Close on overlay click (outside menu)
    this.mobileOverlay.addEventListener('click', (e) => {
      if (e.target === this.mobileOverlay) {
        this.closeMobileMenu();
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.mobileOverlay.classList.contains('active')) {
        this.closeMobileMenu();
      }
    });
  }

  toggleMobileMenu() {
    this.mobileToggle.classList.toggle('active');
    this.mobileOverlay.classList.toggle('active');
    document.body.style.overflow = this.mobileOverlay.classList.contains('active') ? 'hidden' : '';
  }

  closeMobileMenu() {
    this.mobileToggle.classList.remove('active');
    this.mobileOverlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  // ========== SMOOTH SCROLL ==========
  setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        
        if (target) {
          const offsetTop = target.offsetTop - 80;
          window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
          });
        }
      });
    });
  }

  // ========== ACTIVE LINK HIGHLIGHT ==========
  setupActiveLink() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');

    if (sections.length === 0) return;

    window.addEventListener('scroll', () => {
      let current = '';
      
      sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (window.pageYOffset >= sectionTop - 100) {
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
}

// ===================================
// ADDITIONAL NAVBAR FEATURES
// ===================================

// Add scroll animation to navbar items
function animateNavbarItems() {
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach((link, index) => {
    link.style.opacity = '0';
    link.style.transform = 'translateY(-20px)';
    
    setTimeout(() => {
      link.style.transition = 'all 0.5s ease';
      link.style.opacity = '1';
      link.style.transform = 'translateY(0)';
    }, 100 + (index * 50));
  });
}

// Add hover sound effect (optional)
function addHoverEffects() {
  const buttons = document.querySelectorAll('.btn-resume, .btn-hire');
  
  buttons.forEach(btn => {
    btn.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-3px) scale(1.05)';
    });
    
    btn.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });
}

// Search functionality (if you add search later)
function setupSearch() {
  const searchBtn = document.getElementById('searchBtn');
  
  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      // Create search overlay
      const searchOverlay = document.createElement('div');
      searchOverlay.className = 'search-overlay';
      searchOverlay.innerHTML = `
        <div class="search-container">
          <input type="text" placeholder="Search projects, blog posts..." class="search-input">
          <button class="search-close">&times;</button>
        </div>
      `;
      document.body.appendChild(searchOverlay);
      
      // Focus search input
      setTimeout(() => {
        searchOverlay.querySelector('.search-input').focus();
      }, 100);
      
      // Close search
      searchOverlay.querySelector('.search-close').addEventListener('click', () => {
        searchOverlay.remove();
      });
    });
  }
}

// Initialize everything
document.addEventListener('DOMContentLoaded', () => {
  const navbarController = new NavbarController();
  animateNavbarItems();
  addHoverEffects();
  setupSearch();
  
  console.log('✨ Navbar fully loaded!');
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = NavbarController;
}