// HERO slider
let currentSlide = 0;
const slides = document.querySelectorAll(".slide");

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.remove("active");
    if (i === index) {
      slide.classList.add("active");
    }
  });
}
function nextSlide() {
  currentSlide = (currentSlide + 1) % slides.length;
  showSlide(currentSlide);
}
showSlide(currentSlide);
setInterval(nextSlide, 4000);

// Galeria
window.onload = function () {
  let photoIndex = 0;
  const photoSlides = document.querySelectorAll(".gallery-slide");
  const photoDots = document.querySelectorAll(".dot");
  const photoArrowLeft = document.querySelector(".arrow.left");
  const photoArrowRight = document.querySelector(".arrow.right");
  const yearSpan = document.getElementById("year");

  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  function showPhotoSlide(index) {
    photoSlides.forEach((slide, i) => {
      slide.classList.remove("active");
      photoDots[i].classList.remove("active");
      if (i === index) {
        slide.classList.add("active");
        photoDots[i].classList.add("active");
      }
    });
  }

  function nextPhotoSlide() {
    photoIndex = (photoIndex + 1) % photoSlides.length;
    showPhotoSlide(photoIndex);
  }

  function prevPhotoSlide() {
    photoIndex = (photoIndex - 1 + photoSlides.length) % photoSlides.length;
    showPhotoSlide(photoIndex);
  }

  photoArrowRight.addEventListener("click", nextPhotoSlide);
  photoArrowLeft.addEventListener("click", prevPhotoSlide);
  photoDots.forEach((dot, i) => {
    dot.addEventListener("click", () => {
      photoIndex = i;
      showPhotoSlide(i);
    });
  });

  showPhotoSlide(photoIndex);
};

// Hamburger menu toggle
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("nav-links");

if (hamburger && navLinks) {
  hamburger.addEventListener("click", () => {
    navLinks.classList.toggle("show");
  });

  // NEW: Close menu on link click
  const navItems = navLinks.querySelectorAll("a");
  navItems.forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("show");
    });
  });
}
// Hero animation trigger przy scrollu (intersection observer)
const heroSection = document.querySelector(".hero-section");
const heroBg = document.querySelector(".hero-bg");
const heroTitle = document.querySelector(".hero-title");

if (heroSection && heroBg && heroTitle) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          heroBg.classList.remove("reanimate-bg");
          heroTitle.classList.remove("reanimate-title");

          // Trigger reflow
          void heroBg.offsetWidth;
          void heroTitle.offsetWidth;

          heroBg.classList.add("reanimate-bg");
          heroTitle.classList.add("reanimate-title");
        }
      });
    },
    {
      threshold: 0.5,
    }
  );

  observer.observe(heroSection);
}