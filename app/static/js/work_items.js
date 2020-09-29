$(document).ready(function() {
    $('#workItemsTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0
    });
    $('#selectedWorkItemsTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0
    });

    $('#exampleModal').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target_link');
      const code = button.data('code');
      const name = button.data('name');
      const modal = $(this);
      modal.find('.modal-body form').attr('action', target_link);
      modal.find('.modal-body #code').val(code);
      modal.find('.modal-body #name').val(name);
    });
} );
