const drawingLogCloseWrapper = document.getElementById(
  "drawing_log_close_panel_id"
);
const drawingLogClosePanel = document.getElementById("drawing_log_hidden_id");
drawingLogCloseWrapper.addEventListener("click", (e) => {
  e.preventDefault();
  const changeDrawingLogImg = document
    .querySelector("#drawing_log_close_panel_id img")
    .getAttribute("src");
  drawingLogClosePanel.classList.toggle("hidden");
  if (changeDrawingLogImg == "/static/images/up_direction_element.svg") {
    document
      .querySelector("#drawing_log_close_panel_id img")
      .setAttribute("src", "/static/images/direction_element_bottom.svg");
  } else {
    document
      .querySelector("#drawing_log_close_panel_id img")
      .setAttribute("src", "/static/images/up_direction_element.svg");
  }
});

const pageYoffset = window.pageYOffset;
const bidID = document.querySelector(".bidIdJs").getAttribute("value");
const linkQuery = window.location.search;
if (linkQuery) {
  document.documentElement.scrollTop = Number(linkQuery.split("=").pop());
  window.history.replaceState(
    {},
    document.title,
    "/" + "bidding/" + `${bidID}`
  );
}

// Sidebar
if (window.location.hash) {
  document.getElementById("projectGeneralLink_ID").classList.remove("active");
  document
    .querySelector(
      `#sidebar__nav-links-bidding li[id=\\${window.location.hash}_id]`
    )
    .classList.add("active");
}
// endsidebar

const clientCloseWrapper = document.getElementById(
  "client_and_job_close_panel_id"
);
const clientClosePanel = document.getElementById("client_job_hidden_id");
clientCloseWrapper.addEventListener("click", (e) => {
  e.preventDefault();
  const changeClientImg = document
    .querySelector("#client_and_job_close_panel_id img")
    .getAttribute("src");
  clientClosePanel.classList.toggle("hidden");
  if (changeClientImg == "/static/images/up_direction_element.svg") {
    document
      .querySelector("#client_and_job_close_panel_id img")
      .setAttribute("src", "/static/images/direction_element_bottom.svg");
  } else {
    document
      .querySelector("#client_and_job_close_panel_id img")
      .setAttribute("src", "/static/images/up_direction_element.svg");
  }
});

const groupCloseWrapper = document.querySelectorAll("#bid_group_id");
groupCloseWrapper.forEach((element) => {
  element.addEventListener("click", (e) => {
    const groupId = e.currentTarget.dataset["group_panel_id"];
    const groupClosePanel = document.querySelector(
      `#group_panel_id-${groupId}`
    );
    e.preventDefault();
    const changeGroupImg = element.getAttribute("src");
    groupClosePanel.classList.toggle("hidden");
    if (changeGroupImg == "/static/images/up_direction_element.svg") {
      element.setAttribute(
        "src",
        "/static/images/direction_element_bottom.svg"
      );
    } else {
      element.setAttribute("src", "/static/images/up_direction_element.svg");
    }
  });
});

// scroll
const projectGeneralBlock = document.querySelector(
  ".main-container__project_general"
);
const projectScopeOfWorkBlock = document.getElementById("bid_scope_of_work");
const projectExclusionBlock = document.getElementById("bid_exclusion");
const projectClarificationBlock = document.getElementById("bid_clarification");
const projectAlternateBlock = document.getElementById("bid_alternates");

const scrollBlocks = function Scrolling() {
  function removeActiveLink() {
    document
    .querySelector("#sidebar__nav-links-bidding li.active")
    .classList.remove("active");
  };
  // refactoring TODO: Switch
  if (!window.anchorClick) {
    if (
      projectGeneralBlock.offsetTop <= window.pageYOffset &&
      window.pageYOffset <= projectGeneralBlock.offsetHeight
    ) {
      removeActiveLink();
      document.getElementById("projectGeneralLink_ID").classList.add("active");
    }
    if (
      (projectScopeOfWorkBlock.offsetTop <= window.pageYOffset + 2 &&
        projectScopeOfWorkBlock.getBoundingClientRect().bottom >=
          window.innerHeight * 0.55) ||
      projectGeneralBlock.getBoundingClientRect().bottom < window.pageYOffset
    ) {
      removeActiveLink();
      document.getElementById("#bid_scope_of_work_id").classList.add("active");
    }

    if (
      (projectExclusionBlock.offsetTop <= window.pageYOffset + 2 &&
        projectExclusionBlock.getBoundingClientRect().bottom >=
          window.innerHeight * 0.55) ||
      window.pageYOffset >
        projectGeneralBlock.getBoundingClientRect().height +
          projectScopeOfWorkBlock.getBoundingClientRect().height -
          window.innerHeight * 0.25
    ) {
      removeActiveLink();
      document.getElementById("#bid_exclusion_id").classList.add("active");
    }

    if (
      (projectClarificationBlock.offsetTop <= window.pageYOffset + 2 &&
        projectClarificationBlock.getBoundingClientRect().bottom >=
          window.innerHeight * 0.55) ||
      window.pageYOffset >
        projectGeneralBlock.getBoundingClientRect().height +
          projectScopeOfWorkBlock.getBoundingClientRect().height +
          projectExclusionBlock.getBoundingClientRect().height -
          window.innerHeight * 0.25
    ) {
      removeActiveLink();
      document.getElementById("#bid_clarification_id").classList.add("active");
    }

    if (
      (projectAlternateBlock.offsetTop <= window.pageYOffset + 2 &&
        projectAlternateBlock.getBoundingClientRect().bottom >=
          window.innerHeight * 0.55) ||
      window.pageYOffset >
        projectGeneralBlock.getBoundingClientRect().height +
          projectScopeOfWorkBlock.getBoundingClientRect().height +
          projectExclusionBlock.getBoundingClientRect().height +
          projectClarificationBlock.getBoundingClientRect().height -
          window.innerHeight * 0.25
    ) {
      removeActiveLink();
      document.getElementById("#bid_alternates_id").classList.add("active");
    }
  }
  window.anchorClick = false;
};
window.addEventListener("scroll", scrollBlocks);
// endscroll

// Scrolling Scope of work block
const links = document.querySelectorAll("#bid_scope_of_work a");
links.forEach((e) => {
  e.addEventListener("click", () => {
    e.href += `?pageYOffset=${window.pageYOffset}`;
  });
});
// endScrolling

const lineList = document.querySelectorAll(".btnLine_element_direction_js");
lineList.forEach((element) => {
  element.addEventListener("click", (e) => {
    e.preventDefault();
    const lineId = e.currentTarget.dataset["line_id"];
    const areaToShow = document.querySelector(`#${lineId}`);
    const changeLineImg = document
      .querySelector(`#${lineId}_img_id`)
      .getAttribute("src");
    areaToShow.classList.toggle("hidden");
    if (changeLineImg == "/static/images/up_direction_element.svg") {
      $(`#${lineId}_img_id`).attr(
        "src",
        "/static/images/direction_element_bottom.svg"
      );
    } else {
      $(`#${lineId}_img_id`).attr(
        "src",
        "/static/images/up_direction_element.svg"
      );
    }
  });
});

const closeWrapper = document.getElementById("subtotal_close_panel_id");
const subtotalClosePanel = document.getElementById("subtotal_inputs_fields_id");
closeWrapper.addEventListener("click", (e) => {
  const changeImg = $("#subtotal_img_id").attr("src");
  e.preventDefault();
  subtotalClosePanel.classList.toggle("hidden");
  if (changeImg == "/static/images/up_direction_element.svg") {
    $("#subtotal_img_id").attr(
      "src",
      "/static/images/direction_element_bottom.svg"
    );
  } else {
    $("#subtotal_img_id").attr(
      "src",
      "/static/images/up_direction_element.svg"
    );
  }
});

// begin async functions

const bidGrandSubtotal = document.getElementById("grand_subtotal_id");
const bidSubtotal = document.getElementById("subtotal_id");
const subtotalProjectGeneral = document.getElementById(
  "subtotal_project_general_id"
);
const addsOn = document.getElementById("addson_project_general_id");
const grandSubtotalProjectGeneral = document.getElementById(
  "grand_subtotal_project_general_id"
);

function updateSubtotalValues(subtotalValue, grandSubtotalValue, addsOnValue) {
  bidGrandSubtotal.innerText = "$ " + grandSubtotalValue;
  bidSubtotal.innerText = "$ " + subtotalValue;
  subtotalProjectGeneral.innerHTML = `Subtotal: &nbsp; &nbsp; ${subtotalValue}`;
  addsOn.innerHTML = `Adds-on: &nbsp; &nbsp; ${addsOnValue}`;
  grandSubtotalProjectGeneral.innerHTML = `<strong> Grand Total &nbsp; &nbsp; ${grandSubtotalValue}</strong>`;
}

// edit work item line
const updateWorkItemLine = async (el) => {
  const lineID = el.dataset.wil_id;
  const linePrice = document.querySelector(`#line-${lineID} #wIl-price`);
  const lineQuantity = document.querySelector(`#line-${lineID} #wIl-quantity`);
  const lineGroupPrice = document.querySelector(`#line-${lineID} #wIgL-price`);
  const lineGroupQuantity = document.querySelector(
    `#line-${lineID} #wIgL-quantity`
  );

  let formData = new FormData();
  formData.append(`submit`, true);
  if (el.name.startsWith("g-")) {
    el.name = el.name.slice([2]);
    if (el.name === "quantity") {
      formData.append("price", `${lineGroupPrice.value}`);
    }
    if (el.name === "price") {
      formData.append("quantity", `${lineGroupQuantity.value}`);
    } else {
      formData.append("price", `${lineGroupPrice.value}`);
      formData.append("quantity", `${lineGroupQuantity.value}`);
    }
  } else {
    if (el.name === "quantity") {
      formData.append("price", `${linePrice.value}`);
    }
    if (el.name === "price") {
      formData.append("quantity", `${lineQuantity.value}`);
    } else {
      formData.append("price", `${linePrice.value}`);
      formData.append("quantity", `${lineQuantity.value}`);
    }
  }
  formData.append(`${el.name}`, `${el.value}`);
  const test = fetch(
    `/edit_work_item_line/${bidID}/${lineID}?pageYOffset=${pageYoffset}`,
    {
      body: formData,
      method: "POST",
    }
  )
    .then((response) => response.json())
    .then((resData) => {
      const grandSubtotalValue =
        Math.round((resData.grandSubtotal + Number.EPSILON) * 100) / 100;
      const subtotalValue =
        Math.round((resData.subtotal + Number.EPSILON) * 100) / 100;
      const addsOnValue =
        Math.round((grandSubtotalValue - subtotalValue) * 100) / 100;

      // work item line subtotal
      const linkSubtotal = document.getElementById(
        `link_subtotal-${resData.linkWorkItemID}`
      );
      if (linkSubtotal) {
        linkSubtotal.value = "$ " + `${resData.linkWorkItemSubtotal}`;
        setParamValues(resData.bidParamValues);
      }
      // end
      updateSubtotalValues(subtotalValue, grandSubtotalValue, addsOnValue);
    });
};
// endedit block

// Due Date
const dueDate = document.getElementById("due_date_id");
dueDate.addEventListener("change", () => {
  const updateDueDate = async () => {
    const response = await fetch(`/update_due_date/${bidID}/${dueDate.value}`, {
      method: "GET",
    });
    if (!response.ok) {
      console.error("Error update due date!");
    }
  };
  updateDueDate();
});

// Revision
const revision = document.getElementById("revision_id");
revision.addEventListener("change", () => {
  const updateRevision = async () => {
    const response = await fetch(
      `/update_revision/${bidID}/${revision.value}`,
      { method: "GET" }
    );
    if (!response.ok) {
      console.error("Error update revision!");
    }
  };
  updateRevision();
});

// Project Type

document.querySelectorAll('input[name="project_type"]').forEach((elem) => {
  elem.addEventListener("change", function (event) {
    const updateProjectType = async () => {
      const response = await fetch(
        `/project_type/${bidID}/${event.target.value}`,
        { method: "GET" }
      );
      if (!response.ok) {
        console.error("Error update project type!");
      }
    };
    updateProjectType();
  });
});

// TBD Choice

const inputs = document.querySelectorAll('input[type="checkbox"]');

inputs.forEach((el) => {
  const myResponse = async () => {
    const response = await fetch(
      `/check_tbd/${bidID}/${el.getAttribute(
        "name"
      )}?pageYOffset=${pageYoffset}`,
      { method: "GET" }
    );
    if (response.ok) {
      console.log("new response");
      const responseData = await response.text();
      console.log("Response Data: ", responseData);
      if (responseData === "True" || responseData == "tbd_work_item_line_on") {
        el.checked = true;
      } else {
        el.checked = false;
      }
    }
  };
  myResponse();
});

// async bid param tbd

function setParamValues(bidParamValues) {
  document.querySelectorAll(".bid_parameter_value").forEach((e) => {
    switch (e.id.split("_").shift()) {
      case "permit":
        e.value = "$ " + bidParamValues.permit;
        break;
      case "general":
        e.value = "$ " + bidParamValues.general;
        break;
      case "overhead":
        e.value = "$ " + bidParamValues.overhead;
        break;
      case "insurance":
        e.value = "$ " + bidParamValues.insurance;
        break;
      case "profit":
        e.value = "$ " + bidParamValues.profit;
        break;
      default:
        e.value = "$ " + bidParamValues.bond;
    }
  });
}

inputs.forEach((el) => {
  el.addEventListener("click", () => {
    if (el.checked) {
      const myRequest = async () => {
        try {
          const response = await fetch(
            `/save_tbd/${bidID}?=${el.getAttribute("name")}`,
            { method: "GET" }
          );
          if (response.ok) {
            const resData = await response.json();

            const grandSubtotalValue =
              Math.round((resData.grandSubtotal + Number.EPSILON) * 100) / 100;
            const subtotalValue =
              Math.round((resData.subtotal + Number.EPSILON) * 100) / 100;
            const addsOnValue =
              Math.round((grandSubtotalValue - subtotalValue) * 100) / 100;

            // work item line subtotal
            const linkSubtotal = document.getElementById(
              `link_subtotal-${resData.linkWorkItemID}`
            );
            if (linkSubtotal) {
              linkSubtotal.value = "$ " + `${resData.linkWorkItemSubtotal}`;
              setParamValues(resData.bidParamValues);
            } else {
              document.getElementById(`${resData.bid_param_name}_value`).value =
                "$ " + "0.0";
            }
            // end
            updateSubtotalValues(
              subtotalValue,
              grandSubtotalValue,
              addsOnValue
            );
          }
        } catch (err) {
          console.warn(err);
        }
      };
      myRequest();
    } else {
      const tbdTurnOff = async () => {
        try {
          const response = await fetch(
            `/save_tbd/${bidID}?false=${el.getAttribute("name")}`,
            { method: "GET" }
          );
          if (response.ok) {
            const resData = await response.json();

            const grandSubtotalValue =
              Math.round((resData.grandSubtotal + Number.EPSILON) * 100) / 100;
            const subtotalValue =
              Math.round((resData.subtotal + Number.EPSILON) * 100) / 100;
            const addsOnValue =
              Math.round((grandSubtotalValue - subtotalValue) * 100) / 100;

            // work item line subtotal
            const linkSubtotal = document.getElementById(
              `link_subtotal-${resData.linkWorkItemID}`
            );
            if (linkSubtotal) {
              linkSubtotal.value = "$ " + `${resData.linkWorkItemSubtotal}`;
              setParamValues(resData.bidParamValues);
            } else {
              document.getElementById(`${resData.bid_param_name}_value`).value =
                "$ " + resData.bid_param_value;
            }
            // end
            updateSubtotalValues(
              subtotalValue,
              grandSubtotalValue,
              addsOnValue
            );
          }
        } catch (err) {
          console.warn(err);
        }
      };
      tbdTurnOff();
    }
  });
});
// end async bid param tbd

document.querySelectorAll(".percent_parameter").forEach((e) => {
  e.addEventListener("change", () => {
    const value = parseFloat(e.value);
    if (!value) {
      e.value = "0.0%";
    } else {
      e.value = value + "%";
    }
    console.log("Percents " + e.id + " changed to " + e.value);
    // Update percent parameter value in the DB
    const storeInDB = async () => {
      const response = await fetch(
        `/set_percent_value/${bidID}?name=${e.id}&value=${e.value}`,
        { method: "GET" }
      );
      if (!response.ok) {
        console.error(`Cannot store parameter [${e.id}]`);
      }
    };
    storeInDB();
  });
});

// Active decoration on header menu-item by border-bottom
bid_href_id.classList.add("active-tab");
// end decoration
