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
          let changeLineImg = document.querySelector(`#line_img_id`).getAttribute('src');
          areaToShow.classList.toggle('hidden');
          if (changeLineImg == "/static/images/up_direction_element.svg") {
            $('#subtotal_img_id').attr('src', "/static/images/direction_element_bottom.svg");
          } else {
            $('#subtotal_img_id').attr('src', "/static/images/up_direction_element.svg");
          };
      });
  });
});

const closeWrapper = document.getElementById('subtotal_close_panel_id');
const subtotalClosePanel = document.getElementById('subtotal_inputs_fields_id');
closeWrapper.addEventListener('click', (e) => {
  let changeImg = $('#subtotal_img_id').attr('src');
  e.preventDefault();
  subtotalClosePanel.classList.toggle('hidden');
  if (changeImg == "/static/images/up_direction_element.svg") {
    $('#subtotal_img_id').attr('src', "/static/images/direction_element_bottom.svg");
  } else {
    $('#subtotal_img_id').attr('src', "/static/images/up_direction_element.svg");
  };
});

const clientCloseWrapper = document.getElementById('client_and_job_close_panel_id');
const clientClosePanel = document.getElementById('client_job_hidden_id');
clientCloseWrapper.addEventListener('click', (e) => {
  e.preventDefault();
  clientClosePanel.classList.toggle('hidden');
});

const drawingLogCloseWrapper = document.getElementById('drawing_log_close_panel_id');
const drawingLogClosePanel = document.getElementById('drawing_log_hidden_id');
drawingLogCloseWrapper.addEventListener('click', (e) => {
  e.preventDefault();
  drawingLogClosePanel.classList.toggle('hidden');
});
