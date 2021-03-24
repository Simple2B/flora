// custom javascript

"use strict";

// const { tree } = require("gulp");

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

// side-bar scrolling and closing
$("#ddb-background").click(function (e) {
  e.preventDefault();
  $("#wrapper").toggleClass("toggled");
  $('#work-item-container').toggleClass("ddb_mr-auto");
});
// endscrolling


// change Bid status color
const changeStatus = document.querySelector('.status-change_color');
if (changeStatus) {
  switch(changeStatus.textContent) {
    case 'Submitted':
      changeStatus.classList.toggle('status-change_color_submitted');
      changeStatus.classList.remove('status-change_color_draft');
      changeStatus.classList.remove('status-change_color_archived');
      break;
    case "Archived":
      changeStatus.classList.toggle('status-change_color_archived');
      changeStatus.classList.remove('status-change_color_submitted');
      changeStatus.classList.remove('status-change_color_draft');
      break;
    default:
      changeStatus.classList.toggle('status-change_color_draft');
    }
}
// end change Bid status color


const bid_href_id = document.getElementById('bidding_id');

// begin My Profile
const previewUrl = document.getElementById('current_url');
const myProfileSubmitBtn = document.getElementById('my_profile_submit_id');
if (previewUrl) {previewUrl.setAttribute('value', window.location.href)};
myProfileSubmitBtn.setAttribute('value', window.location.href);
// end My Profile block

// scroll
const projectGeneralBlock = document.querySelector('.main-container__project_general');
const projectScopeOfWorkBlock = document.getElementById('bid_scope_of_work');
const projectExclusionBlock = document.getElementById('bid_exclusion');
const projectClarificationBlock = document.getElementById('bid_clarification');
const projectAlternateBlock = document.getElementById('bid_alternates');

let alternateLiClick = false

const scrollBlocks = function Scrolling() {

  // refactoring TODO: Switch
  if (projectGeneralBlock.offsetTop <= window.pageYOffset && window.pageYOffset <= projectGeneralBlock.offsetHeight)
    {
      document.querySelector('#sidebar__nav-links-bidding li.active').classList.remove('active');
      document.getElementById('projectGeneralLink_ID').classList.add('active');
    };
  if (projectScopeOfWorkBlock.offsetTop <= window.pageYOffset + 2
    && projectScopeOfWorkBlock.getBoundingClientRect().bottom >= window.innerHeight*0.55)
    {
      document.querySelector('#sidebar__nav-links-bidding li.active').classList.remove('active');
      document.getElementById('#bid_scope_of_work_id').classList.add('active');
    };

  if (!alternateLiClick &&  projectExclusionBlock.offsetTop <= window.pageYOffset + 2
    && projectExclusionBlock.getBoundingClientRect().bottom >= window.innerHeight*0.55
    || !alternateLiClick &&  window.pageYOffset > (projectGeneralBlock.getBoundingClientRect().height + projectScopeOfWorkBlock.getBoundingClientRect().height)
    - window.innerHeight * 0.25
    )
    {
      document.querySelector('#sidebar__nav-links-bidding li.active').classList.remove('active');
      document.getElementById('#bid_exclusion_id').classList.add('active');
    };

  if (!alternateLiClick && projectClarificationBlock.offsetTop <= window.pageYOffset + 2
    && projectClarificationBlock.getBoundingClientRect().bottom >= window.innerHeight*0.55
    || !alternateLiClick && window.pageYOffset > (projectGeneralBlock.getBoundingClientRect().height + projectScopeOfWorkBlock.getBoundingClientRect().height
    + projectExclusionBlock.getBoundingClientRect().height)
    - window.innerHeight * 0.25
    )
    {
      document.querySelector('#sidebar__nav-links-bidding li.active').classList.remove('active');
      document.getElementById('#bid_clarification_id').classList.add('active');
    };

  if (projectAlternateBlock.offsetTop <= window.pageYOffset + 2
    && projectAlternateBlock.getBoundingClientRect().bottom >= window.innerHeight*0.55
    || window.pageYOffset > (projectGeneralBlock.getBoundingClientRect().height + projectScopeOfWorkBlock.getBoundingClientRect().height
    + projectExclusionBlock.getBoundingClientRect().height + projectClarificationBlock.getBoundingClientRect().height
    - window.innerHeight * 0.25)
    )
    {
      document.querySelector('#sidebar__nav-links-bidding li.active').classList.remove('active');
      document.getElementById('#bid_alternates_id').classList.add('active');
    };
    alternateLiClick = false
};
window.addEventListener('scroll', scrollBlocks);
// endscroll

// Sidebar
const sideBarNavLinks = document.querySelectorAll('#sidebar__nav-links-bidding li');
sideBarNavLinks.forEach( (elem) => {
  elem.addEventListener('click', function(e) {
    document.querySelector('#sidebar__nav-links-bidding li.active').classList.remove('active');
    this.classList.add('active'); // add 'active' class to current link
    myProfileSubmitBtn.setAttribute('value', e.target.href); // source element
    if (previewUrl) {previewUrl.setAttribute('value', window.location.href)};
    if (e.target.hash == "#bid_alternates") {
      alternateLiClick = true
    }
  });
});
// endSidebar