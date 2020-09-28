$(document).ready(function() {
    $('#exclusionsTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0
    });
    $('#selectedExclusionTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0
    });

    $('#exampleModal').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target_link');
      const title = button.data('title');
      const description = button.data('description');
      const modal = $(this);
      modal.find('.modal-body form').attr('action', target_link);
      modal.find('.modal-body #title').val(title);
      modal.find('.modal-body #description').val(description);

    });

    $('#modalDelete').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget); // Button that triggered the modal
        const target_link = button.data('target_link_delete');
        const title = button.data('delete');
        const modal = $(this);
        modal.find('.modal-body #title').val(title);
        modal.find('#delete_item').attr('action', target_link);
    });

} );