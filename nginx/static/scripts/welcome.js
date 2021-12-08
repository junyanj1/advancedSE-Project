const signinChanged = (signin) => {
    console.log("Signin changed:", signin);
}

const userChanged = (user) => {
    console.log("User changed:", user);
    let token = user.getAuthResponse().id_token;
    console.log("    token", token);
    if (token) {
        apiSignIn(
            token,
            data => {
                saveAuthInfo(data["user_id"], data["aapi-key"]);
                $("#user-id-text").html(data["user_id"]);
                $("#api-key-text").html(data["aapi-key"]);
                $("#account-section").show();
            },
            error => {
                removeAuthInfo();
                $("#account-section").hide();
                alert(error);
            }
        );
    }
};

const revokeAllScopes = () => {
    removeAuthInfo();
    $("#account-section").hide();
    gapi.auth2.getAuthInstance().disconnect();
}

window.onGapiLoadCallback = () => {
    gapi.load("auth2", () => {
        gapi.auth2.init({
            client_id: "228008718004-efglglqlouvggbkurnct52mh07kdufpl.apps.googleusercontent.com"
        }).then(auth2 => {
            // Listen for sign-in state changes.
            auth2.isSignedIn.listen(signinChanged);

            // Listen for changes to current user.
            auth2.currentUser.listen(userChanged);

            // Sign in the user if they are currently signed in.
            if (auth2.isSignedIn.get() == true) {
                auth2.signIn();
            }

            // Set signout button
            $(".signout-btn").click(event => {
                console.log("SignOut");
                event.preventDefault();
                revokeAllScopes();
            });
        }, error => {
            console.log('Init error', error);
        });
    });
};

$(document).ready(() => {
    let key = getKey(redirectOnNull=false);
    if (key === null) {
        console.log('Hide API Key section');
        $("#account-section").hide();
    } else {
        console.log('Show API Key section');
        $("#user-id-text").html(getEmail(redirectOnNull=false));
        $("#api-key-text").html(key);
        $("#account-section").show();
    }

    $("#test-signin-btn").click(event => {
        event.preventDefault();
        console.log("Test SignIn");
        saveAuthInfo("organizer1@gmail.com", "AJK/zfuuYiXAA5oq7GGKNzanxrQhPrpN69vNnHc0M9w=");
        $("#user-id-text").html("organizer1@gmail.com");
        $("#api-key-text").html("AJK/zfuuYiXAA5oq7GGKNzanxrQhPrpN69vNnHc0M9w=");
        $("#account-section").show();
    });

    $(".signout-btn").click(event => {
        console.log("SignOut");
        event.preventDefault();
        revokeAllScopes();
    });
});
