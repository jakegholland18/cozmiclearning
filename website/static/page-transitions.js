/**
 * Smooth Page Transitions
 * Adds fade-out effect when navigating to new pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth exit transition on link clicks
    const links = document.querySelectorAll('a:not([target="_blank"]):not([href^="#"]):not(.no-transition)');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Only apply to internal navigation
            if (this.hostname === window.location.hostname) {
                const href = this.href;

                // Prevent default navigation
                e.preventDefault();

                // Add exit animation
                document.body.classList.add('page-exit');

                // Navigate after animation completes
                setTimeout(() => {
                    window.location.href = href;
                }, 300); // Match the CSS animation duration
            }
        });
    });

    // Add fade-in class to main content sections
    const contentSections = document.querySelectorAll('.planet-grid, .mode-grid, .dashboard-container, .content-section');
    contentSections.forEach((section, index) => {
        section.style.animationDelay = `${index * 0.1}s`;
        section.classList.add('fade-in');
    });
});

// Handle browser back/forward buttons
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        // Page was loaded from cache (back/forward button)
        document.body.classList.remove('page-exit');
    }
});
