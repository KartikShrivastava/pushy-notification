self.addEventListener('push', function(event) {
    console.log('Push event received hurray!')
    if (event.data) {
        console.log('Data: ', event.data.text())
    }
    else {
        console.log('No data received')
    }

    const pushInfoPromise = self.registration.showNotification(event.data.title, {
        body: event.data.body
    });

    event.waitUntil(pushInfoPromise);
})
