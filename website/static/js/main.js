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

    // Carousel Logic
    const track = document.getElementById('track');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (track && prevBtn && nextBtn) {
        let scrollAmount = 0;
        const cardWidth = 330; // card width + gap (300 + 30)

        nextBtn.addEventListener('click', () => {
            const maxScroll = track.scrollWidth - track.clientWidth;
            scrollAmount += cardWidth;
            if (scrollAmount > maxScroll) {
                scrollAmount = 0; // Loop back to start
            }
            track.style.transform = `translateX(-${scrollAmount}px)`;
        });

        prevBtn.addEventListener('click', () => {
            scrollAmount -= cardWidth;
            if (scrollAmount < 0) {
                // Go to end
                const maxScroll = track.scrollWidth - track.clientWidth;
                scrollAmount = maxScroll; 
            }
            track.style.transform = `translateX(-${scrollAmount}px)`;
        });
    }
});
