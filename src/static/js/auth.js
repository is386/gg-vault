let auth_url = "api/auth"

// Checks if the user logged in before to skip the login screen
function authHome() {
    if (!localStorage.ggToken) {
        location.href="/";
        return;
    }

    $.ajax({
        url: auth_url,
        type: "POST",
        dataType: "json",
        headers: {"Authorization": "Bearer " + localStorage.ggToken},
        complete: function(data) {
            let status = data.status;
            if (status != 200) {
                location.href="/";
            }
        }
    });
}

// Sends a request to validate the user's login information
function authLogin() {
    if (!localStorage.ggToken) {
        return;
    }

    $.ajax({
        url: auth_url,
        type: "POST",
        dataType: "json",
        headers: {"Authorization": "Bearer " + localStorage.ggToken},
        complete: function(data) {
            let status = data.status;
            if (status == 200) {
                location.href="/games";
            }
        }
    });
}

// Logs the user out by removing their token
function logout() {
    localStorage.removeItem("ggToken");
    location.reload();
}