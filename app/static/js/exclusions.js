$(document).ready(function() {
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
        modal.find('#_exclusion_input_delete #title').val(title);
        modal.find('#delete_item').attr('action', target_link);
    });

    $('#exclusionsTable').DataTable({
        "pageLength": 10,
        "order": [],
        "displayStart": 0,
        "drawCallback": function( settings ) {
            $("#exclusionsTable thead").remove();
        }
    });
    // $('#selectedExclusionTable').DataTable({
    //     "pageLength": 10,
    //     "order": [],
    //     "displayStart": 0
    // });

} );