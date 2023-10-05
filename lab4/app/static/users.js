let deleteUserModal = document.querySelector('#deleteUser')

deleteUserModal.addEventListener('show.bs.modal', function(event){
    let form = document.querySelector('form')
    form.action = event.relatedTarget.dataset.url;
    let userLogin = document.querySelector('#userLogin');
    userLogin.innerHTML = event.relatedTarget.closest('tr').querySelector('#fullName').textContent;
});