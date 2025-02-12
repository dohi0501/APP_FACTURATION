document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("id_username").placeholder = "Entrez le nom d'utilisateur";
    document.getElementById("id_password").placeholder = "Entrez le mot de passe";
});

document.getElementById("id_username").classList.add("form-control")
document.getElementById("id_password").classList.add("form-control")
document.getElementById("id_username").classList.add("form-control-user")
document.getElementById("id_password").classList.add("form-control-user")