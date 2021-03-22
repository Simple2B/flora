const drawingLogCloseWrapper = document.getElementById('drawing_log_close_panel_id');
const drawingLogClosePanel = document.getElementById('drawing_log_hidden_id');
drawingLogCloseWrapper.addEventListener('click', (e) => {
  e.preventDefault();
  let changeDrawingLogImg = document.querySelector('#drawing_log_close_panel_id img').getAttribute('src');
  drawingLogClosePanel.classList.toggle('hidden');
  if (changeDrawingLogImg == "/static/images/up_direction_element.svg") {
    document.querySelector('#drawing_log_close_panel_id img').setAttribute('src', "/static/images/direction_element_bottom.svg");
  } else {
    document.querySelector('#drawing_log_close_panel_id img').setAttribute('src', "/static/images/up_direction_element.svg");
  };
});

$(document).ready(function() {

  const bidID = document.querySelector('.bidIdJs').getAttribute('value');
  if (window.location.search) {
    document.documentElement.scrollTop = Number(window.location.search.split("=").pop())
    window.history.replaceState({}, document.title, "/" + "bidding/" + `${bidID}`);
  }

  // Sidebar
  if (window.location.hash) {
    document.getElementById('projectGeneralLink_ID').classList.remove('active');
    document.querySelector(`#sidebar__nav-links-bidding li[id=\\${window.location.hash}_id]`).classList.add('active');
  };

  $('#modalWorkItemLineEdit').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target_link');
      const note = button.data('note');
      const description = button.data('description');
      const quantity = button.data('quantity');
      const unit = button.data('unit');
      const price = button.data('price');
      const tdb = button.data('tdb');
      const modal = $(this);
      modal.find('#modal_work_item_line_edit').attr('action', target_link);
      modal.find('#modal_note').val(note);
      modal.find('#modal_description').val(description);
      modal.find('#modal_quantity').val(quantity);
      modal.find('#modal_unit').val(unit);
      modal.find('#modal_price').val(price);
      modal.find('#modal_tdb').val(tdb);
  });

  const clientCloseWrapper = document.getElementById('client_and_job_close_panel_id');
  const clientClosePanel = document.getElementById('client_job_hidden_id');
  clientCloseWrapper.addEventListener('click', (e) => {
    e.preventDefault();
    let changeClientImg = document.querySelector('#client_and_job_close_panel_id img').getAttribute('src');
    clientClosePanel.classList.toggle('hidden');
    if (changeClientImg == "/static/images/up_direction_element.svg") {
      document.querySelector('#client_and_job_close_panel_id img').setAttribute('src', "/static/images/direction_element_bottom.svg");
    } else {
      document.querySelector('#client_and_job_close_panel_id img').setAttribute('src', "/static/images/up_direction_element.svg");
    };
  });

  const groupCloseWrapper = document.querySelectorAll('#bid_group_id');
  groupCloseWrapper.forEach(element => {
      element.addEventListener('click', (e) => {
          const groupId = e.currentTarget.dataset["group_panel_id"]
          const groupClosePanel = document.querySelector(`#group_panel_id-${groupId}`)
          e.preventDefault();
          let changeGroupImg = element.getAttribute('src');
          groupClosePanel.classList.toggle('hidden');
          if (changeGroupImg == "/static/images/up_direction_element.svg") {
              element.setAttribute('src', "/static/images/direction_element_bottom.svg");
          } else {
              element.setAttribute('src', "/static/images/up_direction_element.svg");
          };
      });
  });

  // Scrolling Scope of work block

  const links = document.querySelectorAll("#bid_scope_of_work a")
  links.forEach((e) => {
    e.addEventListener('click', () => {
      e.href += `?pageYOffset=${window.pageYOffset}`
    })
  })
  // endScrolling

  // Due Date
  const dueDate = document.getElementById('due_date_id');
  dueDate.addEventListener('change', () => {
    const updateDueDate = async () => {
      const response = await fetch(`/update_due_date/${bidID}/${dueDate.value}`, {method: 'GET'})
      if (!response.ok) {
        console.error("Error update due date!")
      }
    };
    updateDueDate();
  });

  // Revision
  const revision = document.getElementById('revision_id');
  revision.addEventListener('change', () => {
    const updateRevision = async () => {
      const response = await fetch(`/update_revision/${bidID}/${revision.value}`, {method: 'GET'})
      if (!response.ok) {
        console.error("Error update revision!")
      }
    };
    updateRevision();
  });

  // Project Type

  document.querySelectorAll('input[name="project_type"]').forEach((elem) => {
    elem.addEventListener("change", function(event) {
      const updateProjectType = async () => {
        const response = await fetch(`/project_type/${bidID}/${event.target.value}`, {method: 'GET'})
        if (!response.ok) {
          console.error("Error update project type!")
        }
      };
      updateProjectType();
    });
  });

  // TBD Choice

  const inputs = document.querySelectorAll('input[type="checkbox"]');

  inputs.forEach( el => {
    const myResponse = async () => {
      const response = await fetch(`/check_tbd/${bidID}/${el.getAttribute('name')}`, {method: 'GET'})
      if (response.ok) {
        console.log('new response');
        const responseData = await response.text()
        console.log("Response Data: ", responseData);
        if (responseData === 'True' || responseData == "tbd_work_item_line_on") {
           el.checked = true
          }
        else {
          el.checked = false;
        };
      };
    };
    myResponse();
  });

  // async bid_param_tbd

  const bidGrandSubtotal = document.getElementById('grand_subtotal_id');
  const bidSubtotal = document.getElementById('subtotal_id');
  const subtotalProjectGeneral = document.getElementById('subtotal_project_general_id');
  const addsOn = document.getElementById('addson_project_general_id');
  const grandSubtotalProjectGeneral = document.getElementById('grand_subtotal_project_general_id');

  inputs.forEach( el => {
    el.addEventListener('click', () => {
      if (el.checked) {
        const myRequest = async () => {
          try {
            const response = await fetch(`/save_tbd/${bidID}?=${el.getAttribute('name')}`, {method: 'GET'})
            if (response.ok) {
              console.log(response);
              const resData = await response.json()
              console.log(resData);

              const grandSubtotalValue = Math.round(( resData.grandSubtotal + Number.EPSILON) * 100) / 100;
              const subtotalValue = Math.round(( resData.subtotal + Number.EPSILON) * 100) / 100;
              const addsOnValue = Math.round((grandSubtotalValue - subtotalValue) * 100) / 100;

              document.getElementById(`${resData.bid_param_name}_value`).value = '$ ' + '0.0';
              bidGrandSubtotal.innerText = '$ ' + grandSubtotalValue;
              bidSubtotal.innerText = '$ ' + subtotalValue;
              subtotalProjectGeneral.innerHTML = `Subtotal: &nbsp; &nbsp; ${subtotalValue}`;
              addsOn.innerHTML = `Adds-on: &nbsp; &nbsp; ${addsOnValue}`;
              grandSubtotalProjectGeneral.innerHTML = `<strong> Grand Total &nbsp; &nbsp; ${grandSubtotalValue}</strong>`;
            }
          }
          catch (err){
            console.warn(err)
          }
        };
        myRequest()
      }
      else {
        const tbdTurnOff = async () => {
          try {
            const response = await fetch(`/save_tbd/${bidID}?false=${el.getAttribute('name')}`, {method: 'GET'})
            if (response.ok) {
              const resData = await response.json()
              console.log(resData);

              const grandSubtotalValue = Math.round(( resData.grandSubtotal + Number.EPSILON) * 100) / 100;
              const subtotalValue = Math.round(( resData.subtotal + Number.EPSILON) * 100) / 100;
              const addsOnValue = Math.round((grandSubtotalValue - subtotalValue) * 100) / 100;

              document.getElementById(`${resData.bid_param_name}_value`).value = '$ ' + resData.bid_param_value;
              bidGrandSubtotal.innerText = '$ ' + grandSubtotalValue;
              bidSubtotal.innerText = '$ ' + subtotalValue;
              subtotalProjectGeneral.innerHTML = `Subtotal: &nbsp; &nbsp; ${subtotalValue}`;
              addsOn.innerHTML = `Adds-on: &nbsp; &nbsp; ${addsOnValue}`;
              grandSubtotalProjectGeneral.innerHTML = `<strong> Grand Total &nbsp; &nbsp; ${grandSubtotalValue}</strong>`;
            }
          }
          catch (err){
            console.warn(err)
          }
        };
        tbdTurnOff()
      }
    });
  });

  document.querySelectorAll(".percent_parameter").forEach( (e) => {
    e.addEventListener("change", () => {
      const value = parseFloat(e.value);
      if(!value) {
        e.value = "0.0%";
      } else {
        e.value = value + "%";
      }
      console.log("Percents " + e.id + " changed to " + e.value);
      // Update percent parameter value in the DB
      const storeInDB = async () => {
        const response = await fetch(`/set_percent_value/${bidID}/${e.id}/${e.value}`, {method: 'GET'})
        if (!response.ok) {
          console.error(`Cannot store parameter [${e.id}]`);
        }
      };
      storeInDB();
    });
  });

});

// Active decoration on header menu-item by border-bottom
bid_href_id.classList.add('active-tab');
// end decoration
