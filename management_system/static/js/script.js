const id_username = document.getElementById('id_username')
const id_password = document.getElementById('id_password')

if (id_username && id_password){
    id_username.classList.add("form-control","mt-2")
    id_password.classList.add("form-control","mt-2")
}

var alertElement = document.getElementById('auto-hide-alert');

if (alertElement) {
    setTimeout(function () {
        alertElement.classList.remove('show');
        alertElement.style.display = 'none';
    }, 2000);
}