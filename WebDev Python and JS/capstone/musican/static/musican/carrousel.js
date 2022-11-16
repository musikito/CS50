"use strict";
// current slide counter
let curSlide = 0;
// Select all slides
const slides = document.querySelectorAll(".slide");
// maximum number of slides
let maxSlide = slides.length - 1;
// Call the slides
showSlides();


function showSlides(){
 
    if (curSlide === maxSlide) {
    curSlide = 0;
  } else {
    curSlide++;
  }

   // loop through slides and set each slides translateX
   slides.forEach((slide, indx) => {
    slide.style.transform = `translateX(${100 * (indx - curSlide)}%)`;
  });
  

  setTimeout(showSlides, 2000);

}