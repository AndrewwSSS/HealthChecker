function chane_password() {
    let formData = {
        old_password: document.getElementById("currentPassword").value,
        new_password1: document.getElementById("newPassword").value,
        new_password2: document.getElementById("renewPassword").value,
    };
    let done_callback = response => show_toast("Password change successfully", "success")

    ajax_post("/api/user/me/update_password", formData, done_callback, FAIL_CALLBACK, "PUT")
}

function update_user(){
    let sex_select = document.getElementById("sex")
    let formData = {
        email: document.getElementById("Email").value,
        username: document.getElementById("username").value,
        first_name: document.getElementById("first_name").value,
        last_name: document.getElementById("last_name").value,
        sex: sex_select.options[sex_select.selectedIndex].value,
        birth_date: document.getElementById("birth_date").value,
        weight: document.getElementById("weight").value,
        height: document.getElementById("height").value,
    };

    let done_callback =
            response => show_toast("User updated successfully.", "success");

    ajax_post("/api/user/me", formData, done_callback, FAIL_CALLBACK, "PUT")
}