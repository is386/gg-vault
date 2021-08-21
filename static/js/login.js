let login_url = "api/login"

// Colors the user input red to show an error
function resetUserLogin() {
    let userInput = $("#user-input-login");
    userInput.removeClass("is-invalid");
}

// Colors the password input red to show an error
function resetPassLogin() {
    let passInput = $("#pass-input-login");
    passInput.removeClass("is-invalid");
}

// If the user did not fill one of the fields, it colors the fields red
function loginError() {
    let userInput = $("#user-input-login");
    let passInput = $("#pass-input-login");
    userInput.addClass("is-invalid");
    passInput.addClass("is-invalid");
}

// Sends a request to create an account
function sendLogin() {
    $("#login-error").prop("hidden", true);
    let userInput = $("#user-input-login");
    let passInput = $("#pass-input-login");
    let user = userInput.val();
    let pass = passInput.val();

    if (!user && !pass) {
        userInput.addClass("is-invalid");
        passInput.addClass("is-invalid");
        return;
    } else if (!user) {
        userInput.addClass("is-invalid");
        return;
    } else if (!pass) {
        passInput.addClass("is-invalid");
        return;
    }

    formData = {"username": user, "password": pass};
    $.ajax({
        url: login_url,
        type: "POST",
        dataType: "json",
        data: formData,
        complete: function(data) {
            let status = data.status;
            if (status != 200) {
                $("#login-error").prop( "hidden", false);
            } else {
                let token = data.responseJSON.token;
                localStorage.ggToken = token;
                location.href="/";
            }
        }
    });
}
