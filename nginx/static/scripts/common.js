// Environment
const BASE_ENDPOINT = "http://localhost:3000"

// APIS
const apiGetEvents = (email, success, error) => {
    console.log("--> apiGetEvents");
    $.ajax({
        url: `${BASE_ENDPOINT}/users/${email}/events`,
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
    $.ajax({
        method: "POST",
        url: `${BASE_ENDPOINT}/events`,
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
