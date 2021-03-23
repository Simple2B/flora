if ( document.getElementById('bidding_id').href == window.location.href ) {
  bid_href_id.classList.remove('menu__item');
  bid_href_id.classList.toggle('active-tab');
};

$(document).ready(function() {

  let table = $('#biddingsTableId').DataTable({
    "pageLength": 15,
    "order": [],
    "displayStart": 0,
    "bLengthChange": false,
    sDom: 'lrtip',
    searching: true,
    });

  $('#biddingsSearch').on( 'keyup', function () {
    table.search( this.value ).draw();
  });
});
