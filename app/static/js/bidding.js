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
      console.log('Hello');
    } else {
      document.querySelector('#client_and_job_close_panel_id img').setAttribute('src', "/static/images/up_direction_element.svg");
    };
  });


  // Active decoration on header menu-item by border-bottom
  bid_href_id.classList.remove('menu__item');
  bid_href_id.classList.toggle('active-tab');
  // end decoration


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
        response.text().then(result => {
          console.log(response.ok)
          if (result == "0.0" || result == "0") { el.checked = true }
          else { el.checked = false };
        });
      }
    };
    myResponse();

    el.addEventListener('click', () => {
      if (el.checked) {
        const myRequest = async () => {
          try {
            const request = await fetch(`/save_tbd/${bidID}?=${el.getAttribute('name')}`, {method: 'GET'})
            if (request.ok) {
              const resData = await request.json()
            }
          }
          catch (err){
            console.warn(err)
          }
        };
        myRequest()
      }
      else {
        const tbdUnchecked = async () => {
          try {
            const request = await fetch(`/save_tbd/${bidID}?false=${el.getAttribute('name')}`, {method: 'GET'})
            if (request.ok) {
              const resData = await request.json()
            }
          }
          catch (err){
            console.warn(err)
          }
        };
        tbdUnchecked()
      }
    });
  });
});

// Active decoration on header menu-item by border-bottom
// bid_href_id.classList.remove('menu__item');
bid_href_id.classList.add('active-tab');
// end decoration
