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


} );

const groupWrapper = document.getElementById('groupTableWrapper');
const groupToggle = document.getElementById('btnGroup');
groupToggle.addEventListener('click', (e) => {
    e.preventDefault();
    groupWrapper.classList.toggle('hidden');
});

const sidebarWrapper = document.getElementById('wrapper');
const barToggle = document.getElementById('ddb-background');
barToggle.addEventListener('click', (e) => {
    e.preventDefault();
    sidebarWrapper.classList.toggle('hidden');
});


// if (location.href == 'http://localhost:3000/work_items') {
//     document.getElementById('wrapper').classList.toggle('test-class');
// };