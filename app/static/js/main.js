// custom javascript

"use strict";

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
          let changeLineImg = document.querySelector(`#${lineId}_img_id`).getAttribute('src');
          areaToShow.classList.toggle('hidden');
          if (changeLineImg == "/static/images/up_direction_element.svg") {
            $(`#${lineId}_img_id`).attr('src', "/static/images/direction_element_bottom.svg");
          } else {
            $(`#${lineId}_img_id`).attr('src', "/static/images/up_direction_element.svg");
          };
      });
  });
});


// change Bid status color

$(document).ready( function() {
  let changeStatus = document.querySelector('.status-change_color');
  if (changeStatus.textContent == 'Draft') {
    changeStatus.classList.toggle('status-change_color_draft');
    changeStatus.classList.remove('status-change_color_submitted');
    changeStatus.classList.remove('status-change_color_archived');
  };
  if (changeStatus.textContent == 'Submitted') {
    changeStatus.classList.toggle('status-change_color_submitted');
    changeStatus.classList.remove('status-change_color_draft');
    changeStatus.classList.remove('status-change_color_archived');
  } 
  if (changeStatus.textContent == 'Archived') {
    changeStatus.classList.toggle('status-change_color_archived');
    changeStatus.classList.remove('status-change_color_submitted');
    changeStatus.classList.remove('status-change_color_draft');
  };
});
// end change Bid status color


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
