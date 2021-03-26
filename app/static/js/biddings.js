bid_href_id.classList.remove("menu__item");
bid_href_id.classList.toggle("active-tab");

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
  const tablePages = ["paginate_button ", "paginate_button previous", "paginate_button next"]
  function redirectToBid() {
    const rows = Array.from(document.querySelectorAll("#biddingsTableId tr")).slice(1)
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
  redirectToBid();
  document.getElementById("biddingsTableId_wrapper").addEventListener('click', (event) => {
    if (tablePages.includes(event.target.className))
    redirectToBid();
  })
  document.getElementById("biddingsSearch").addEventListener('change', redirectToBid)
  // endredirect
});
