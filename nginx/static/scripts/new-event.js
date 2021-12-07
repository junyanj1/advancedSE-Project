$(document).ready(() => {
    console.log("event loaded");

    // Set time field (needed for Safari)
    let current = new Date();
    $("#start_date").val(getDateString(current));
    $("#start_time").val(getTimeString(current));
    current.setHours(current.getHours() + 1);  // +1 hour
    $("#end_date").val(getDateString(current));
    $("#end_time").val(getTimeString(current));


    $("#event-form").on("submit", event => {
        event.preventDefault();

        let data = $("#event-form").serializeArray().reduce((a, b) => 
                (a[b["name"]] = b["value"], a), {});

        // TODO: do something with these values
        data["lat"] = 1.1;
        data["long"] = 1.1;
        data["start_time"] = data["start_date"] + ' ' + data["start_time"];
        data["end_time"] = data["end_date"] + ' ' + data["end_time"];
        data["attendee_limit"] = +data["attendee_limit"]  // converts to number
        apiCreateNewEvent(
            data,
            () => alert('success'),
            () => alert('error'),
        );
    });
});
