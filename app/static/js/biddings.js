if (document.getElementById("bidding_id").href == window.location.href) {
  bid_href_id.classList.remove("menu__item");
  bid_href_id.classList.toggle("active-tab");
}

$(document).ready(function () {
  let table = $("#biddingsTableId").DataTable({
    pageLength: 15,
    order: [],
    displayStart: 0,
    bLengthChange: false,
    sDom: "lrtip",
    searching: true,
  });

  $("#biddingsSearch").on("keyup", function () {
    table.search(this.value).draw();
  });

  // redirect to bid

  // biddingsTableId_paginate
  function redirectToBid() {
    let rows = Array.from(document.querySelectorAll("#biddingsTableId tr")).slice(1)
    rows.forEach((e) => {
      e.addEventListener('mouseover', () => {
        e.classList.add('bid_link');
      })
      e.addEventListener('mouseout', () => {
        e.classList.remove('bid_link')
      })
      e.addEventListener('click', () => {
        window.location.href = e.querySelector('a').href;
      })
    })
  };
  redirectToBid()
  // endredirect
  const tablePages = document.querySelectorAll('#biddingsTableId_paginate a')
  tablePages.forEach((e) => {
    e.addEventListener('click', () => {
      console.log(e)
      redirectToBid()
    })
  })
  document.getElementById('biddingsTableId_info').addEventListener('change', (event) => {
    console.log('Again?');
  });
});
