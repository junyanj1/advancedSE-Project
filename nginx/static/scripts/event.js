// Populate and return a event-detail-key-value
const createEventDetailItem = (key, value) => {
    let template = $($("#event-detail-key-value").html());
    $("#key", template).text(key);
    $("#value", template).text(value);
    return template;
}

const createAttendeeItem = (attendee) => {
    let template = $($("#attendee-item").html());
    $("#user_email", template).text(attendee.user_email);
    $("#is_invited", template).text(attendee.is_invited);
    $("#is_rsvped", template).text(attendee.is_rsvped);
    $("#is_checked_in", template).text(attendee.is_checked_in);
    return template;
}

$(document).ready(() => {
    console.log("Event document loaded");

    // Get eventID
    const eventID = new URLSearchParams(window.location.search).get('event_id');

    // Get event detail
    apiGetEvent(eventID, eventDetail => {
        // Set title
        $("#event_name").text(eventDetail.event_name);

        // Set rest of the detail
        let container = $("#event-detail");
        for (const [ key, value ] of Object.entries(eventDetail)) {
            container.append(createEventDetailItem(key, value));
        }
        $('#Map').attr('src', "https://www.google.com/maps/embed/v1/view?key=AIzaSyAavntvfgcU9xJ8yWGGOYxSGd9sHJ30QAk&zoom=18" + "&center=" + eventDetail.lat + "," + eventDetail.long);
    });

    // Get attendees
    apiGetAttendees(eventID, attendees => {
        attendees.forEach(attendee => {
            $("#attendee-table").append(createAttendeeItem(attendee));
        });
    });

    // Send invite on submit
    $("#invitation-form").on("submit", event => {
        event.preventDefault();

        const emails = $("#invite-field").val().split(";").map(x => x.trim());
        apiSendInvitations(
            eventID,
            emails,
            () => alert('success'),
            () => alert('error'),
        );
    });
});
