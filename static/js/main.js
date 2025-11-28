/**
 * Al Jannah Academy - Main JavaScript
 * Handles Sliders, Animations, and UI interactions.
 */

document.addEventListener("DOMContentLoaded", function () {
    // -------------------------------------------------------
    // 1. Initialize AOS (Animate On Scroll)
    // -------------------------------------------------------
    // Checks if the AOS library is loaded before initializing
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 800,
            easing: "slide",
            once: true,
            offset: 50,
        });
    }

    // -------------------------------------------------------
    // 2. Hero Home Slider (Swiper.js)
    // -------------------------------------------------------
    const heroSlider = document.getElementById("heroSlider");
    if (heroSlider) {
        const swiperHero = new Swiper("#heroSlider", {
            // Optional parameters
            direction: "horizontal",
            loop: true,
            effect: "fade", // Smooth fade transition
            speed: 1000,

            fadeEffect: {
                crossFade: true,
            },

            // Auto-scroll
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },

            // Pagination dots
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },

            // Navigation arrows
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
        });
    }

    // -------------------------------------------------------
    // 3. "Explore" / Feature Links Slider (Optional)
    // -------------------------------------------------------
    // If you decide to carousel the 'Explore' cards on mobile
    const featureSlider = document.querySelector(".feature-slider");
    if (featureSlider) {
        new Swiper(".feature-slider", {
            slidesPerView: 1,
            spaceBetween: 20,
            breakpoints: {
                768: { slidesPerView: 2 },
                1024: { slidesPerView: 4 },
            },
            pagination: { el: ".swiper-pagination", clickable: true },
        });
    }

    // -------------------------------------------------------
    // 4. Navbar Scroll Effect (Optional Polish)
    // -------------------------------------------------------
    // Adds a shadow to the navbar when scrolling down
    const navbar = document.querySelector(".header-wrap");
    if (navbar) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 50) {
                navbar.classList.add("shadow-sm");
            } else {
                navbar.classList.remove("shadow-sm");
            }
        });
    }

    // -------------------------------------------------------
    // 5. Bootstrap Alerts Auto-Dismiss
    // -------------------------------------------------------
    // Automatically fades out success messages after 5 seconds
    const alerts = document.querySelectorAll(".alert-success");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
