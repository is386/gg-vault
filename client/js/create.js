let create_url = "http://127.0.0.1:8080/create"

// Colors the user input red to show an error
function resetUserCreate() {
    let userInput = $("#user-input-create");
    userInput.removeClass("is-invalid");
}

// Colors the password input red to show an error
function resetPassCreate() {
    let passInput = $("#pass-input-create");
    passInput.removeClass("is-invalid");
}

// If the user did not fill one of the fields, it colors the fields red
function createError() {
    let userInput = $("#user-input-create");
    let passInput = $("#pass-input-create");
    userInput.addClass("is-invalid");
    passInput.addClass("is-invalid");
}

// Sends a request to create an account
function sendCreate() {
    $("#create-error").prop("hidden", true);
    $("#create-success").prop( "hidden", true);

    let userInput = $("#user-input-create");
    let passInput = $("#pass-input-create");
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
        url: create_url,
        type: "POST",
        dataType: "json",
        data: formData,
        complete: function(data) {
            let status = data.status;
            if (status != 200) {
                $("#create-error").prop( "hidden", false);
            } else {
                $("#create-success").prop( "hidden", false);
            }
        }
    });
}
