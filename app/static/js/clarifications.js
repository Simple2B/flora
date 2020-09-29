$(document).ready(function() {
    $('#clarificationsTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0,
        "drawCallback": function( settings ) {
            $("#clarificationTable thead").remove();
        }
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

    $('#modalDeleteClarification').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget); // Button that triggered the modal
        const target_link = button.data('target_link_clarification_delete');
        const note = button.data('delete');
        const modal = $(this);
        modal.find('#_clarification_input_delete #title').val(note);
        modal.find('#delete_clarification_item').attr('action', target_link);
    });

} );