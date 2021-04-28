bid_href_id.classList.remove("menu__item");
bid_href_id.classList.toggle("active-tab");


$(document).ready(function() {
    let table = $("#biddingsTableId").DataTable({
        pageLength: 15,
        order: [],
        displayStart: 0,
        bLengthChange: false,
        sDom: "lrtip",
        searching: true,
    });

    $("#biddingsSearch").on("keyup", function() {
        table.search(this.value).draw();
    });

    // redirect to bid
    const tablePages = ["paginate_button ", "paginate_button previous", "paginate_button next"];

    // const statusValuesColorNew = document.getElementsByClassName('statusValueColorNew');
    // const values = Array.from(statusValuesColorNew);
    // values.map(value => value.style.color = 'red');
    // values.map(value => value.style.fontWeight = '600');

    // console.log(values);

    //statusValueColorNew.style.color = 'red'

    function redirectToBid() {
        const rows = Array.from(document.querySelectorAll("#biddingsTableId tr")).slice(1)

        rows.forEach((e) => {
            const redirect = () => {
                window.location.href = e.querySelector('a').href;
            };
            e.addEventListener('mouseover', (event) => {
                e.classList.add('bid_link');
                if (event.target.className == "form-control") {
                    e.removeEventListener('click', redirect)
                } else {
                    e.addEventListener('click', redirect)
                }
            })
            e.addEventListener('mouseout', () => {
                e.classList.remove('bid_link')
            })
            e.addEventListener('click', redirect)
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