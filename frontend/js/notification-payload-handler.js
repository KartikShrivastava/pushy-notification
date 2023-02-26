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

notificationPayloadsStore = []
let selectedPayloadListItem = null

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
    // Save notification payload for later processing
    notificationPayloadsStore = payloads

    const payloadOrderedList = document.getElementById('payload-ordered-list')

    // Clear the list
    payloadOrderedList.innerHTML = ''

    payloads.forEach((payload, index) => {
      const listItem = document.createElement('li')

      // Add click event listener to select only one payload at a time as click event
      listItem.addEventListener('click', () => {
        // De-select previously selected payload
        if (selectedPayloadListItem) {
          selectedPayloadListItem.classList.remove('selected')
          selectedPayloadListItem.style.border = 'none'
        }

        listItem.classList.add('selected')
        listItem.style.border = '2px solid green'
        selectedPayloadListItem = listItem
      })

      listItem.textContent = payload.title
      listItem.dataset.index = index

      payloadOrderedList.appendChild(listItem)
    })
  })
  .catch(function (err) {
    console.error('Unable to get payloads from database.', err)
  })
}

document.getElementById('refresh-payloads')
        .addEventListener('click', getAllNotificationPayloadsFromDatabse)
