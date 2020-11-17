$(document).ready(function() {
    $('#workItemsTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0,
        "drawCallback": function( settings ) {
            $("#workItemsTable thead").remove();
        }
    });
    $('#selectedWorkItemsTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0
    });

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
        const buttonId = e.currentTarget.id
        const areaToShow = document.querySelector(`#groupTableWrapper-${buttonId}`)
        let changeLineImg = document.querySelector(`#${buttonId}_img_id`).getAttribute('src');
        areaToShow.classList.toggle('hidden');
        if (changeLineImg == "/static/images/up_direction_element.svg") {
            $(`#${buttonId}_img_id`).attr('src', "/static/images/direction_element_bottom.svg");
          } else {
            $(`#${buttonId}_img_id`).attr('src', "/static/images/up_direction_element.svg");
          };
    });
});


// SideBar close/show-panel
// const sidebarWrapper = document.getElementById('sidebar-wrapper');
// const barToggle = document.getElementById('ddb-background');
// barToggle.addEventListener('click', (e) => {
//     e.preventDefault();
//     sidebarWrapper.classList.toggle('hidden');
// });

const href_work_items_ = document.getElementsByClassName('__text-decor-active');

if ( href_work_items_[0].href == window.location.href ) {
  document.getElementById('bidding_id').classList.toggle('active-tab');
};
