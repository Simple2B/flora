const team_ = document.getElementById('myTeam_id');

if ( team_.href == window.location.href ) {
    team_.classList.remove('menu__item');
    team_.classList.toggle('active-tab');
};

$('#editTeamModal').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget); // Button that triggered the modal
    const editCardLink = button.data('edit_card-link');
    const username = button.data('username');
    const position = button.data('position');
    const email = button.data('email');
    const phone = button.data('phone');
    const modal = $(this);
    modal.find('.modal-body form').attr('action', editCardLink);
    modal.find('.modal-body #edit_card-username').val(username);
    modal.find('.modal-body #edit_card-position').val(position);
    modal.find('.modal-body #edit_card-email').val(email);
    modal.find('.modal-body #edit_card-phone').val(phone);
  });
