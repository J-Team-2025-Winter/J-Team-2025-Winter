document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript Loaded!"); 

  const icon = document.querySelector(".hamburger__icon"); 
  const menu = document.querySelector(".customer_hamburger_menu");

  if (icon && menu) {
    console.log("Elements Found!"); 

    icon.addEventListener("click", function () {
      menu.classList.toggle("active"); 
      console.log("Hamburger icon clicked!"); 
    });
  } else {
    console.log("Elements not found!"); 
  }
});
