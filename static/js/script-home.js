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

showSlide(currentSlide); // pokaż pierwszy slajd od razu
setInterval(nextSlide, 4000);
// GALERIA – zadziała po załadowaniu całej strony
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
  
    // Obsługa kliknięć
    photoArrowRight.addEventListener("click", nextPhotoSlide);
    photoArrowLeft.addEventListener("click", prevPhotoSlide);
    photoDots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        photoIndex = i;
        showPhotoSlide(i);
      });
    });
  };
  // Rok w stopce
  const yearSpan = document.getElementById("year");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }
  // Hamburger menu toggle
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("nav-links");

hamburger.addEventListener("click", () => {
  navLinks.classList.toggle("show");
});