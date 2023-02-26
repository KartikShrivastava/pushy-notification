// payload expects list of subscriber_id and payload_id
function triggerBulkPushNotification(payload) {
    return fetch('http://127.0.0.1:8000/notifications/records', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    })
    .then(function (response) {

    })
}