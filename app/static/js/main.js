// custom javascript

"use strict";

    // $( "#select_ul_id li a" ).on('click', function(e) {
    //     // e.preventDefault();
    //     // $('.contentMenu').each((i, item) => $(item).removeClass('ddb-underline'));
    //     $("#select_ul_id li a").removeClass('ddb-underline');
    //     $(this).addClass('ddb-underline');
    //     // $(this).addClass('ddb-underline');
    // });
    // // });
const indicator = document.querySelector('.nav-indicator');
const items = document.querySelectorAll('.menu__item');

const handleIndicator = (el) => {
  items.forEach(function (item) {
    item.classList.remove('is-active');
    item.removeAttribute('style');
  });
  indicator.style.width = "".concat(el.offsetWidth, "px");
  indicator.style.left = "".concat(el.offsetLeft, "px");
  indicator.style.backgroundColor = el.getAttribute('active-color');
  el.classList.add('is-active');
  el.style.color = el.getAttribute('active-color');
}

items.forEach((item) => {
  item.addEventListener('click', function (e) {
    handleIndicator(e.target);
  });
  item.classList.contains('is-active') && handleIndicator(item);
});

$("#ddb-background").click(function (e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
});
