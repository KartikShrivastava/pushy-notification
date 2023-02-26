function fetchNotificationPayloadFromUi(event) {
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
notificationPayloadForm.addEventListener('submit', fetchNotificationPayloadFromUi)

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

function getAllNotificationPayloadsFromDatabse() {
  return fetch('http://127.0.0.1:8000/notifications/payloads/', {
    method: 'GET',
  })
  .then(function (response) {
    if(!response.ok)
      throw new Error('Bad status code from server.')
    return response.json()
  })
  .then(function (payloads) {
    const payloadOrderedList = document.querySelector('.payload-ordered-list')

    // clear the list first
    payloadOrderedList.innerHTML = ''

    payloads.forEach(payload => {
      const markup = `<li>${JSON.stringify(payload)}</li>`
      payloadOrderedList.insertAdjacentHTML('beforeend', markup)
    })
  })
  .catch(function (err) {
    console.error('Unable to get payloads from database.', err)
  })
}

document.getElementById('refresh-payloads')
        .addEventListener('click', getAllNotificationPayloadsFromDatabse)
