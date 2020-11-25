const biddings_ = document.getElementById('bidding_id');

if ( biddings_.href == window.location.href ) {
  bid_href_id.classList.remove('menu__item');
  bid_href_id.classList.toggle('active-tab');
};

$(document).ready(function() {
  //   $("#biddingsSearch").keyup(function() {
  //   _this = this;

  //   $.each($("#biddingsTableId tbody tr"), function() {
  //       if($(this).text().toLowerCase().indexOf($(_this).val().toLowerCase()) === -1) {
  //           $(this).hide();
  //       } else {
  //           $(this).show();
  //       }});
  //     });
  // });

  let table = $('#biddingsTableId').DataTable({
    "pageLength": 5,
    "order": [],
    "displayStart": 0,
    "bLengthChange": false,
    sDom: 'lrtip',
    searching: true,
    // "drawCallback": function( settings ) {
    //     $("#workItemsTable thead").remove();
    // }
    });

  $('#biddingsSearch').on( 'keyup', function () {
  table.search( this.value ).draw();
  });
});