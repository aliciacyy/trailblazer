document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.stat-number, .stat-box-no-decimal');
    
    const animate = (counter) => {
        const target = parseFloat(counter.getAttribute('data-target'));
        const count = parseFloat(counter.innerText || 0);
        
        // Use a small epsilon for floating point comparison
        const epsilon = 0.1; // Smaller epsilon for 2 decimal precision
        if (Math.abs(target - count) < epsilon) {
            counter.innerText = counter.classList.contains('stat-box-no-decimal') ? 
                Math.floor(target).toString() : 
                target.toFixed(2);
            return;
        }
        
        if (counter.classList.contains('stat-box-no-decimal')) {
            // Faster increment for non-decimal numbers
            const increment = Math.max(1, Math.floor(target / 20));
            const newValue = Math.min(count + increment, target);
            counter.innerText = Math.floor(newValue).toString();
            // add 0 in front if less than 10
            if (newValue < 10) {
                counter.innerText = '0' + counter.innerText;
            }
            
            if (newValue < target) {
                setTimeout(() => animate(counter), 50);
            }
        } else {
            const increment = target / 100;
            const decimalValue = Math.min(count + increment, target);
            counter.innerText = decimalValue.toFixed(2); // Always show 2 decimal places
            if (decimalValue < target) {
                setTimeout(() => animate(counter), 10);
            }
        }
    };

    // Start animation when element is in viewport
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.innerText = entry.target.classList.contains('stat-box-no-decimal') ? 
                    '0' : 
                    '0.00';
                animate(entry.target);
                // Stop observing this element after first animation
                observer.unobserve(entry.target);
            }
        });
    });

    counters.forEach(counter => {
        counter.innerText = counter.classList.contains('stat-box-no-decimal') ? 
            '0' : 
            '0.00';
        observer.observe(counter);
    });
    
    const statBox = document.querySelector('.stat-box');
    let count = 10;

    if (statBox) {
        // Initial display
        statBox.textContent = count;

        // Update every second
        const countdown = setInterval(() => {
            count--;
            statBox.textContent = count;

            // Stop when we reach 0
            if (count <= 0) {
                clearInterval(countdown);
                statBox.textContent = "Countdown complete!";
            }
        }, 1000); // 1000ms = 1 second
    }
}); 