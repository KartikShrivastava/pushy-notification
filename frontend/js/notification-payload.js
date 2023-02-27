function fetchNotificationPayload(event) {
    event.preventDefault()

    const data = new FormData(event.target)
    const payload = Object.fromEntries(data.entries())

    saveNotificationPayloadToDatabase(payload)

    // Reset the title and body
    title = document.getElementById('ttl')
    body = document.getElementById('bdy')
    title.value = ''
    body.value = ''

    return false
}

// Add click event handler to notification-payload submit button
const notificationPayloadForm = document.querySelector('.payload-form')
notificationPayloadForm.addEventListener('submit', fetchNotificationPayload)

function saveNotificationPayloadToDatabase(payload) {
    return fetch('http://127.0.0.1:8000/notifications/payloads/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    })
    .then(function (response) {
      if (!response.ok)
        throw new Error('Bad status code from server.')
      return response
    })
    .then(function (serverResponse) {
      console.log(serverResponse)
    })
    .catch(function (err) {
      console.error('Unable to send push subscription to database.', err)
    })
}
