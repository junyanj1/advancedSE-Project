// Populate and return a event-detail-key-value
const createEventDetailItem = (key, value) => {
    let template = $($("#event-detail-key-value").html());
    $("#key", template).text(key);
    $("#value", template).text(value);
    return template;
}

$(document).ready(() => {
    console.log("Attendee document loaded");

    const params = new URLSearchParams(window.location.search);
    const eventID = params.get('event_id');
    const personalCode = params.get('personal_code');

    // Get event detail
    apiGetEvent(eventID, eventDetail => {
        // Set title
        $("#event_name").text(eventDetail.event_name);

        // Set rest of the detail
        let container = $("#event-detail");
        for (const [ key, value ] of Object.entries(eventDetail)) {
            container.append(createEventDetailItem(key, value));
        }
    });

    // Get attendees
    apiGetAttendees(eventID, attendees => {
        attendees.forEach(attendee => {
            if (attendee.personal_code === personalCode) {
                $("#attendee_email").text(attendee.user_email)
                $("#is_invited").text(attendee.is_invited);
                $("#is_rsvped").text(attendee.is_rsvped);
                $("#is_checked_in").text(attendee.is_checked_in);
            }
        });
    });

    // RSVP on button click
    $("#rsvp-btn").click(event => {
        event.preventDefault();
        apiRsvp(
            eventID,
            personalCode,
            () => alert('success'),
            () => alert('error'),
        );
    });

    // Check-in on button click
    $("#checkin-btn").click(event => {
        event.preventDefault();
        apiCheckIn(
            eventID,
            personalCode,
            () => alert('success'),
            () => alert('error'),
        );
    });
});