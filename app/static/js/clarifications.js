$(document).ready(function() {
    $('#clarificationsTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0
    });
    $('#selectedClarificationTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0
    });

    $('#exampleModal').on('show.bs.modal', function (event) {
      const button = $(event.relatedTarget); // Button that triggered the modal
      const target_link = button.data('target_link');
      const note = button.data('note');
      const description = button.data('description');
      const modal = $(this);
      modal.find('.modal-body form').attr('action', target_link);
      modal.find('.modal-body #note').val(note);
      modal.find('.modal-body #description').val(description);
    });
} );