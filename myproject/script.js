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
});
