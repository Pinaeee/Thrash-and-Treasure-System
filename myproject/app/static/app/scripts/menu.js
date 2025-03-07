document.addEventListener('DOMContentLoaded', function() {
    const banner = document.querySelector('.banner');
    const images = banner.querySelectorAll('img');
    let currentImageIndex = 0;

    // Initially show only the first image
    images.forEach((img, index) => {
        img.style.display = index === 0 ? 'block' : 'none';
    });

    function showNextImage() {
        // Hide the current image
        images[currentImageIndex].style.display = 'none';

        // Calculate the index of the next image
        currentImageIndex = (currentImageIndex + 1) % images.length;

        // Show the next image
        images[currentImageIndex].style.display = 'block';
    }

    // Set interval to change image every 3 seconds
    setInterval(showNextImage, 3000);

    // Add smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add animation on scroll
    const cards = document.querySelectorAll('.card');
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    cards.forEach(card => {
        observer.observe(card);
        card.classList.add('opacity-0');
    });

    // Add loading animation
    window.addEventListener('load', function() {
        document.body.classList.add('loaded');
    });
});
