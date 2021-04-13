// custom javascript

"use strict";

// const { tree } = require("gulp");

//
const indicator = document.querySelector(".nav-indicator");
const items = document.querySelectorAll(".menu__item");

const handleIndicator = (el) => {
    items.forEach(function(item) {
        item.classList.remove("is-active");
        item.removeAttribute("style");
    });
    indicator.style.width = "".concat(el.offsetWidth, "px");
    indicator.style.left = "".concat(el.offsetLeft, "px");
    indicator.style.backgroundColor = el.getAttribute("active-color");
    el.classList.add("is-active");
    el.style.color = el.getAttribute("active-color");
};

items.forEach((item) => {
    item.addEventListener("click", function(e) {
        handleIndicator(e.target);
    });
    item.classList.contains("is-active") && handleIndicator(item);
});

// side-bar scrolling and closing
$("#ddb-background").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    $("#work-item-container").toggleClass("ddb_mr-auto");
});
// endscrolling

// change Bid status color
const changeStatus = document.querySelector(".status-change_color");
if (changeStatus) {
    switch (changeStatus.textContent) {
        case "Submitted":
            changeStatus.classList.toggle("status-change_color_submitted");
            changeStatus.classList.remove("status-change_color_draft");
            changeStatus.classList.remove("status-change_color_archived");
            break;
        case "Archived":
            changeStatus.classList.toggle("status-change_color_archived");
            changeStatus.classList.remove("status-change_color_submitted");
            changeStatus.classList.remove("status-change_color_draft");
            break;
        default:
            changeStatus.classList.toggle("status-change_color_draft");
    }
}
// end change Bid status color

const bid_href_id = document.getElementById("bidding_id");

// begin My Profile
const previewUrl = document.getElementById("current_url");
const myProfileSubmitBtn = document.getElementById("my_profile_submit_id");
if (previewUrl) {
    previewUrl.setAttribute("value", window.location.href);
}
myProfileSubmitBtn.setAttribute("value", window.location.href);
// end My Profile block

// Sidebar
const sideBarNavLinks = document.querySelectorAll(
    "#sidebar__nav-links-bidding li"
);

/// part of bidding scroll
window.anchorClick = false;
/// end

sideBarNavLinks.forEach((elem) => {
    elem.addEventListener("click", function(e) {
        document
            .querySelector("#sidebar__nav-links-bidding li.active")
            .classList.remove("active");
        this.classList.add("active"); // add 'active' class to current link
        myProfileSubmitBtn.setAttribute("value", e.target.href); // source element
        if (previewUrl) {
            previewUrl.setAttribute("value", window.location.href);
        }
        window.anchorClick = true;
    });
});
// endSidebar