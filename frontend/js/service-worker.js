self.addEventListener('push', function(event) {
    let notification_data = {}
    if (event.data) {
        notification_data = JSON.parse(event.data.text())
    }
    else {
        console.error('No data received')
    }

    const options = {
        body: notification_data.message,
    };

    const pushInfoPromise = self.registration.showNotification(
        notification_data.title,
        options
    );

    event.waitUntil(pushInfoPromise);
})
