// Create custom search
function setAttributes(el, attrs) {
    for(var key in attrs) {
      el.setAttribute(key, attrs[key]);
    }
};

const div = document.createElement('div');
const img = document.createElement('img');
const input = document.createElement('input');

div.setAttribute('class', '_form-search');
img.setAttribute('src', '/static/images/Search_icon.png');
setAttributes(input, {
    "class": "input_search",
    "placeholder": "Search",
    "aria-controls": "workItemsTable",
    "id": "customSearchId",
});
div.prepend(img);
div.append(input);
document.querySelector('.chart-left .form').before(div);


$.fn.dataTableExt.oApi.fnFilterAll = function (oSettings, sInput, iColumn, bRegex, bSmart) {
    let settings = $.fn.dataTableSettings;

    for (let i = 0; i < settings.length; i++) {
        settings[i].oInstance.fnFilter(sInput, iColumn, bRegex, bSmart);
    }
};

$(document).ready(function() {
    $('#workItemsTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0,
        "language": { search: "", searchPlaceholder: "Search"},
        sDom: 'lrtip',
        searching: true,
        "drawCallback": function( settings ) {
            $("#workItemsTable thead").remove();
        }
    });

    const workItemTable = $("#table1").dataTable();

    $('#customSearchId').on( 'keyup', function () {
        // workItemTable.search( this.value ).draw();
        workItemTable.fnFilterAll(this.value);
    });

    $('#selectedWorkItemsTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0,
        sDom: 'lrtip',
        searching: true,
    });

    const selectedWorkItems = $('#selectedWorkItemsTable').DataTable();

    $('#customSearchId').on( 'keyup', function () {
        selectedWorkItems.fnFilterAll(this.value);
    });

    document.getElementById("workItemsTable_info").classList.add("t-gray");
    document.getElementById("selectedWorkItemsTable_info").classList.add("t-gray");

    $('#modalEdit').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target_link');
      const code = button.data('code');
      const name = button.data('name');
      const modal = $(this);
      modal.find('.modal-body form').attr('action', target_link);
      modal.find('.modal-body #code').val(code);
      modal.find('.modal-body #name').val(name);
    });

    $('#modalDeleteWorkItem').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget); // Button that triggered the modal
        const target_link = button.data('target_link_work_item_delete');
        const code = button.data('delete_work_item');
        const name = button.data('work_item_name');
        const modal = $(this);
        modal.find('#delete_work_item').attr('action', target_link);
        modal.find('#_work_item_input_delete #title').val(code);
        modal.find('#_work_item_input_name_delete #title').val(name);
    });

    $('#modalDeleteGroup').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget); // Button that triggered the modal
        const target_link = button.data('target_link_group_delete');
        const name = button.data('group_name');
        const modal = $(this);
        modal.find('#_modal_delete_group').attr('action', target_link);
        modal.find('#_group_input_delete #_input_group_name').val(name);
    });

} );

// Group close/show-panel
const groupWrapper = document.getElementsByClassName('groupTableWrapper_js');
const groupToggle = document.getElementsByClassName('btnGroup_js');
const listArray = Array.from(groupToggle);

listArray.forEach( el => {
    el.addEventListener('click', (e) => {
        e.preventDefault();
        let buttonId = e.currentTarget.id;
        const areaToShow = document.querySelector(`#groupTableWrapper-${buttonId}`);
        let changeLineImg = document.getElementById(`${buttonId}_img_id`).getAttribute('src');
        areaToShow.classList.toggle('hidden');
        if (changeLineImg == "/static/images/up_direction_element.svg") {
            document.getElementById(`${buttonId}_img_id`).setAttribute('src', "/static/images/direction_element_bottom.svg");
          } else {
            document.getElementById(`${buttonId}_img_id`).setAttribute('src', "/static/images/up_direction_element.svg");
          };
    });
});

const href_work_items_ = document.getElementsByClassName('__text-decor-active');

if ( href_work_items_[0].href == window.location.href ) {
  document.getElementById('bidding_id').classList.toggle('active-tab');
};
