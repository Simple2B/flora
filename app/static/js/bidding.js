// const groupWrapper = document.getElementById('groupTableWrapper');
// const groupToggle = document.getElementById('btnGroup');
// groupToggle.addEventListener('click', (e) => {
//     e.preventDefault();
//     groupWrapper.classList.toggle('hidden');
// });

function changeLineElement(workItemLineId, fieldName) {
    console.log("changed: [" + fieldName + "] for work item line: [" + workItemLineId + "]" );
}

$('#modalWorkItemLineEdit').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget); // Button that triggered the modal
    const target_link = button.data('target_link');
    const note = button.data('note');
    const description = button.data('description');
    const quantity = button.data('quantity');
    const unit = button.data('unit');
    const price = button.data('price');
    const tdb = button.data('tdb');
    const modal = $(this);
    modal.find('#modal_work_item_line_edit').attr('action', target_link);
    modal.find('#modal_note').val(note);
    modal.find('#modal_description').val(description);
    modal.find('#modal_quantity').val(quantity);
    modal.find('#modal_unit').val(unit);
    modal.find('#modal_price').val(price);
    modal.find('#modal_tdb').val(tdb);

});
