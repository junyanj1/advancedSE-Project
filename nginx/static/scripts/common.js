// Environment
const BASE_ENDPOINT = "http://team-aapi.me"

// APIS
const commonHeaders = () => {
    return { 
        "aapi-key": getKey(),
    };
}

const apiSignIn = (token, success, error) => {
    console.log("--> apiSignIn")
    $.ajax({
        method: "POST",
        url: `${BASE_ENDPOINT}/signin`,
        headers: {"aapi-token": token},
        dataType: "json",
        contentType: "application/json",
        success: logSuccess(success),
        error: logError(error),
    });
}

const apiGetEvents = (success, error) => {
    console.log("--> apiGetEvents");
    const email = getEmail();
    $.ajax({
        url: `${BASE_ENDPOINT}/users/${email}/events`,
        headers: commonHeaders(),
        success: logSuccess(success),
        error: logError(error),
    });
}

const apiGetEvent = (eventID, success, error) => {
    console.log("--> apiGetEvents");
    $.ajax({
        url: `${BASE_ENDPOINT}/events/${eventID}`,
        success: logSuccess(success),
        error: logError(error),
    });
}

const apiGetAttendees = (eventID, success, error) => {
    console.log("--> apiGetAttendees");
    $.ajax({
        url: `${BASE_ENDPOINT}/events/${eventID}/attendances`,
        success: logSuccess(success),
        error: logError(error),
    });
}

const apiSendInvitations = (eventID, emails, success, error) => {
    console.log("--> apiSendInvitations");
    $.ajax({
        method: "POST",
        url: `${BASE_ENDPOINT}/events/${eventID}/invite`,
        headers: commonHeaders(),
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify({"emails": emails}),
        success: logSuccess(success),
        error: logError(error),
    });
}

const apiRsvp = (eventID, personalCode, success, error) => {
    console.log("--> apiRsvp");
    $.ajax({
        url: `${BASE_ENDPOINT}/events/${eventID}/rsvp/${personalCode}`,
        success: logSuccess(success),
        error: logError(error),
    });
}

const apiCheckIn = (eventID, personalCode, success, error) => {
    console.log("--> apiCheckIn");
    $.ajax({
        url: `${BASE_ENDPOINT}/events/${eventID}/check_in/${personalCode}`,
        success: logSuccess(success),
        error: logError(error),
    });
}

const apiCreateNewEvent = (data, success, error) => {
    console.log("--> apiCreateNewEvent");
    data["user_id"] = getEmail();
    $.ajax({
        method: "POST",
        url: `${BASE_ENDPOINT}/events`,
        headers: commonHeaders(),
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: logSuccess(success),
        error: logError(error),
    });
}

// Wrapper for console log
const logSuccess = (successCallback) => {
    return (...args) => {
        console.log(`<-- SUCCESS ${args[2].status}`, args[0]);
        if (successCallback) successCallback(...args);
    };
}

const logError = (errorCallback) => {
    return (...args) => {
        let msg = args[0]?.responseJSON?.description;
        console.log(`<-- ERROR ${args[0].status} ${msg}`, args[0]);
        if (errorCallback) errorCallback(...args);
    };
}

// Get date and time string
const getDateString = (date) => {
    return date.toISOString().slice(0, 10);
}

const getTimeString = (date) => {
    return date.toLocaleString("en-US",
        { hour: "numeric", minute: "numeric", hour12: false });
}

// Authentication
const getEmail = (redirectOnNull=true) => {
    email = window.localStorage.getItem("email");
    if (redirectOnNull && email === null) {
        window.location.href = "welcome.html";
        throw 'No email!'
    }
    return email
    // return window.localStorage.getItem("email");
}

const getKey = (redirectOnNull=true) => {
    key = window.localStorage.getItem("key");
    if (redirectOnNull && key === null) {
        window.location.href = "welcome.html";
        throw 'No key!'
    }
    return key
    // return window.localStorage.getItem("key");
}

const saveAuthInfo = (email, key) => {
    window.localStorage.setItem("email", email);
    window.localStorage.setItem("key", key);
}

const removeAuthInfo = () => {
    window.localStorage.removeItem("email");
    window.localStorage.removeItem("key");
}

$(document).ready(() => {
    console.log('Loading navbar');

    // From: https://materializecss.com/navbar.html
    const navbar = `
        <nav>
            <div class="nav-wrapper white">
            <a href="index.html" class="brand-logo ml1 black-text">Advanced API</a>
                <a href="#" data-target="mobile-demo" class="sidenav-trigger black-text"><i class="material-icons">menu</i></a>
                <ul class="right hide-on-med-and-down">
                    <li><a href="welcome.html" class="black-text">Account</a></li>
                    <li><a href="api.html" class="black-text">API</a></li>
                    <li><a href="https://github.com/junyanj1/advancedSE-Project" class="mr1 black-text">GitHub</a></li>
                </ul>
            </div>
        </nav>

        <ul class="sidenav" id="mobile-demo">
            <li><a href="welcome.html">Account</a></li>
            <li><a href="api.html">API</a></li>
            <li><a href="https://github.com/junyanj1/advancedSE-Project">GitHub</a></li>
        </ul>
    `;
    $("#nav-placeholder").html(navbar);
    $('.sidenav').sidenav();
});
