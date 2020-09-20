// custom javascript

$(document).ready(function(){
    // $( ".i" ).click(function() {
    //     console.log(12);
    //     alert( "Handler for .click() called." );
    //   });
    var element_id = $(".ddb-active")[0];
    var a_element_id = $(".a_active_id");
    var ul_element_id = $("#select_ul_id li a");
    console.log(element_id);
    console.log(a_element_id);
    console.log(ul_element_id);
    // a_element_id.forEach(i => {
    //     console.log(i);
    // });
    // a_element_id.forEach(element => {

    $( "#select_ul_id li a" ).on('click', function(e) {
        e.preventDefault();
        $("#select_ul_id li a").removeClass('ddb-underline');
        $(this).addClass('ddb-underline');
    });
    // });
});
