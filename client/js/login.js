const my_url = "http://127.0.0.1:8080/login"

function resetUserLogin() {
    let userInput = $("#user-input-login");
    userInput.removeClass("is-invalid");
}

function resetPassLogin() {
    let passInput = $("#pass-input-login");
    passInput.removeClass("is-invalid");
}

function loginError() {
    let userInput = $("#user-input-login");
    let passInput = $("#pass-input-login");
    userInput.addClass("is-invalid");
    passInput.addClass("is-invalid");
}

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
        url: my_url,
        type: 'POST',
        dataType: 'json',
        data: formData,
        complete: function(data) {
            let status = data.status;
            if (status != 200) {
                $("#login-error").prop( "hidden", false);
            } else {
                let token = data.responseJSON.token;
                localStorage.ggToken = token;
                location.href="/client/home.html";
            }
        }
    });
}
