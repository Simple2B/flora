// custom javascript

"use strict";

function changeMainTab(evt, cityName) {
  var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontentm");
  for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

//
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

const bid_href_id = document.getElementById('bidding_id');

$(document).ready( function() {
  const lineList = document.querySelectorAll(".btnLine_element_direction_js")
  lineList.forEach(element =>{
      element.addEventListener('click',
      (e)=> {
          e.preventDefault();
          const lineId = e.currentTarget.dataset["line_id"]
          const areaToShow = document.querySelector(`#${lineId}`)
          areaToShow.classList.toggle('hidden');
      });
  });
});
