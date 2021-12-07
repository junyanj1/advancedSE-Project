const createEventListItem = (event) => {
    let template = $($("#event-list-item").html());
    $("#event_name", template).text(event.event_name);
    $("#location", template).text(event.location);
    $("#start_time", template).text(event.start_time);
    template.attr("data-id", event.event_id);
    return template;
}

$(document).ready(() => {
    console.log("Document loaded");

    // Get list of events
    apiGetEvents(data => {
        // Append each event to the event table
        data.forEach(event => {
            $("#event-table").append(createEventListItem(event));
        });

        // Set click listener
        $("#event-table .clickable-event-row").click(function() {
            const id = $(this).attr("data-id");
            console.log(id);
            window.location.href = `event.html?event_id=${id}`
        });
    });
});
