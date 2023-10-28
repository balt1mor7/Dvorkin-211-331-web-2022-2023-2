'use strict';

function imagePreviewHandler(event) {
    if (event.target.files && event.target.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            let img = document.querySelector('.background-preview > img');
            img.src = e.target.result;
            if (img.classList.contains('d-none')) {
                let label = document.querySelector('.background-preview > label');
                label.classList.add('d-none');
                img.classList.remove('d-none');
            }
        }
        reader.readAsDataURL(event.target.files[0]);
    }
}

function openLink(event) {
    if (event.target.tagName == 'BUTTON') return;
    let row = event.target.closest('.card');
    if (row.dataset.url) {
        window.location = row.dataset.url;
    }
}



// function deleteBookHandler(event) {  
//     let form = document.querySelector('form');
//     console.log(event.relatedTarget);
//     form.action = event.relatedTarget.dataset.url;
// }

let textReview = document.getElementById('text_review')
if (textReview) {
    const easymde = new EasyMDE({textReview},);
}

let shortDesk = document.getElementById('short_desc')
if (shortDesk) {
    const easymde = new EasyMDE({shortDesk},);
}

window.onload = function() {
    // let deleteModal = document.querySelector('#delete');
    // if (deleteModal) {
    //     deleteModal.addEventListener('show.bs.modal', deleteBookHandler)
    // }
    let background_img_field = document.getElementById('background_img');
    if (background_img_field) {
        background_img_field.onchange = imagePreviewHandler;
    }
    for (let course_elm of document.querySelectorAll('.books-list .card')) {
        course_elm.onclick = openLink;
    }
}