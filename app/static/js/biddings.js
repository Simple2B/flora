const biddings_ = document.getElementById('bidding_id');

if ( biddings_.href == window.location.href ) {
  document.getElementById('bidding_id').classList.toggle('test-class');
};

const draft = document.querySelector('#bids_draft_id');
const submitted = document.querySelector('#bids_submitted_id');
const archived = document.querySelector('#bids_archived_id');
const all = document.querySelector('#bids_all_id');

// submitted.addEventListener('click', (e) => {
//   submitted.classList.add('status-active');
//   draft.classList.remove('status-active');
//   archived.classList.remove('status-active');
//   all.classList.remove('status-active');
// });

