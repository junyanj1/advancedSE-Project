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
            },
            error => alert(error),
        );
    }
};

const revokeAllScopes = () => {
    removeAuthInfo();
    gapi.auth2.getAuthInstance().disconnect();
}

window.onLoadCallback = () => {
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
            $("#signout-btn").click(event => {
                event.preventDefault();
                revokeAllScopes();
            });
        });
    });
};
