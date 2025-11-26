document.addEventListener('DOMContentLoaded', () => {
    console.log('BlackIce HackerSpace System Initialized...');

    // Simple typing effect for the subtitle
    const subtitle = document.querySelector('.hero p');
    if (subtitle) {
        const text = subtitle.textContent;
        subtitle.textContent = '';
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                subtitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 30);
            }
        };
        typeWriter();
    }

    // Add hover effect for hardware cards via JS for more complex interactions if needed
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            card.style.setProperty('--x', `${x}px`);
            card.style.setProperty('--y', `${y}px`);
        });
    });

    // Generic Carousel Logic
    const setupCarousel = (trackId, prevBtn, nextBtn) => {
        const track = document.getElementById(trackId);
        if (!track) return;

        const cardWidth = 380; // Approximate card width + gap

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                track.scrollBy({
                    left: cardWidth,
                    behavior: 'smooth'
                });
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                track.scrollBy({
                    left: -cardWidth,
                    behavior: 'smooth'
                });
            });
        }
    };

    // Initialize Carousels
    // 1. Hardware Carousel (Legacy IDs)
    setupCarousel('track', document.getElementById('prevBtn'), document.getElementById('nextBtn'));

    // 2. News Carousel
    const newsPrev = document.querySelector('#news-carousel .prev');
    const newsNext = document.querySelector('#news-carousel .next');
    setupCarousel('news-track', newsPrev, newsNext);

    // 3. Events Carousel
    const eventsPrev = document.querySelector('#events-carousel .prev');
    const eventsNext = document.querySelector('#events-carousel .next');
    setupCarousel('events-track', eventsPrev, eventsNext);


    // User Dropdown Logic
    const userAvatarBtn = document.getElementById('userAvatarBtn');
    const userDropdown = document.getElementById('userDropdown');

    if (userAvatarBtn && userDropdown) {
        userAvatarBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!userDropdown.contains(e.target) && !userAvatarBtn.contains(e.target)) {
                userDropdown.classList.remove('show');
            }
        });
    }

    // Cyberpunk Glitch Effect
    class CyberGlitch {
        constructor(el) {
            this.el = el;
            this.chars = '!<>-_\\/[]{}—=+*^?#________';
            this.originalText = el.innerText;
            this.update = this.update.bind(this);
            this.frame = 0;
            this.queue = [];
            
            for (let i = 0; i < this.originalText.length; i++) {
                const char = this.originalText[i];
                this.queue.push({
                    from: char,
                    to: char,
                    start: Math.floor(Math.random() * 40),
                    end: Math.floor(Math.random() * 40) + Math.floor(Math.random() * 40)
                });
            }
            
            cancelAnimationFrame(this.frameRequest);
            this.frame = 0;
            this.update();
        }
        
        update() {
            let output = '';
            let complete = 0;
            
            for (let i = 0, n = this.queue.length; i < n; i++) {
                let { from, to, start, end, char } = this.queue[i];
                
                if (this.frame >= end) {
                    complete++;
                    output += to;
                } else if (this.frame >= start) {
                    if (!char || Math.random() < 0.28) {
                        char = this.randomChar();
                        this.queue[i].char = char;
                    }
                    output += `<span class="glitch-char">${char}</span>`;
                } else {
                    output += from;
                }
            }
            
            this.el.innerHTML = output;
            
            if (complete === this.queue.length) {
                this.el.innerHTML = this.originalText; // Restore original to keep HTML structure if any
            } else {
                this.frameRequest = requestAnimationFrame(this.update);
                this.frame++;
            }
        }
        
        randomChar() {
            return this.chars[Math.floor(Math.random() * this.chars.length)];
        }
    }

    // Initialize Glitch on specific elements
    const glitchElements = document.querySelectorAll('.cyber-glitch');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                new CyberGlitch(entry.target);
                // Stop observing to run only once
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    glitchElements.forEach(el => observer.observe(el));

    // Random "Green Glitch" on text
    const randomGlitch = () => {
        const textElements = document.querySelectorAll('.about-text');
        if (textElements.length === 0) return;
        
        const randomEl = textElements[Math.floor(Math.random() * textElements.length)];
        const originalHTML = randomEl.innerHTML;
        
        // Don't glitch if already glitching
        if (randomEl.dataset.glitching === 'true') return;
        
        randomEl.dataset.glitching = 'true';
        
        // Simple visual glitch via CSS class
        randomEl.classList.add('glitch-active');
        
        setTimeout(() => {
            randomEl.classList.remove('glitch-active');
            randomEl.dataset.glitching = 'false';
        }, 200 + Math.random() * 300);
        
        setTimeout(randomGlitch, 2000 + Math.random() * 5000);
    };
    
    setTimeout(randomGlitch, 3000);

    // Cookie Banner Logic
    const banner = document.getElementById("welcome-banner");
    const closeBtn = document.getElementById("close-banner");

    // Check cookie
    if (banner && !document.cookie.split('; ').find(row => row.startsWith('welcome_banner_closed=true'))) {
        banner.style.display = "block";
    }

    if(closeBtn) {
        closeBtn.addEventListener("click", function() {
            if(banner) banner.style.display = "none";
            // Set cookie for 30 days
            document.cookie = "welcome_banner_closed=true; path=/; max-age=" + (60*60*24*30);
        });
    }
});
