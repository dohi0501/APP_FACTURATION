document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("id_username").placeholder = "Entrez le nom de l'utilisateur";
    document.getElementById("id_password1").placeholder = "Entrez le mot de passe";
    document.getElementById("id_password2").placeholder = "Confirmez le mot de passe";
});
document.getElementById("id_username").classList.add("form-control")
document.getElementById("id_password1").classList.add("form-control")
document.getElementById("id_password2").classList.add("form-control")
document.getElementById("id_username").classList.add("form-control-user")
document.getElementById("id_password1").classList.add("form-control-user")
document.getElementById("id_password2").classList.add("form-control-user")
