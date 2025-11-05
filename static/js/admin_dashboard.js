document.addEventListener('DOMContentLoaded', () => {
    const iframe = document.getElementById('content-frame');
    const navLinks = document.querySelectorAll('.nav-link');

    // Function to handle link clicks and update iframe source
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const newSrc = this.getAttribute('href');
            iframe.src = newSrc;

            // Update active link styling
            navLinks.forEach(l => {
                // Remove active styling from all links
                l.classList.remove('active-link');
                l.classList.remove('bg-indigo-600', 'hover:bg-indigo-700');
                l.classList.add('text-gray-300');
            });

            // Apply active styling to the clicked link
            this.classList.add('active-link');
            this.classList.remove('text-gray-300');
        });
    });

    // --- Initialization ---

    // 1. Get the default link (Dashboard)
    const defaultLink = document.querySelector('.nav-link[data-default="true"]');

    // 2. Apply initial active styling to the default link
    // Note: The HTML already uses active-link styling, this reinforces it via JS.
    navLinks.forEach(l => {
        l.classList.remove('active-link', 'bg-indigo-600', 'hover:bg-indigo-700');
        l.classList.add('text-gray-300');
    });

    defaultLink.classList.add('active-link', 'bg-indigo-600');
    defaultLink.classList.remove('text-gray-300');

    // 3. Ensure the iframe loads the default content (redundant but safe)
    iframe.src = defaultLink.getAttribute('href');
});