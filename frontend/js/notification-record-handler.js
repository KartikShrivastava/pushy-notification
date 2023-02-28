var subscribersStore = window.subscriberStore
var notificationPayloadsStore = window.notificationPayloadsStore

// payload expects list of subscriber_ids and payload_id
function triggerBulkPushNotification() {
    const selectedSubscribersId = []
    document.querySelectorAll('#subscriber-ordered-list li.selected').forEach(listItem => {
        const index = parseInt(listItem.dataset.index)

        selectedSubscribersId.push(subscribersStore[index].subscriber_id)
    })

    var selectedNotificationPayloadId = null
    document.querySelectorAll('#payload-ordered-list li.selected').forEach(listItem => {
        const index = parseInt(listItem.dataset.index)
        selectedNotificationPayloadId = notificationPayloadsStore[index].payload_id
    })
    
    sendPayload = {}
    sendPayload.subscriber_ids = selectedSubscribersId
    sendPayload.payload_id = selectedNotificationPayloadId

    return fetch('http://127.0.0.1:8000/notifications/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(sendPayload),
    })
    .then(function (response) {
        if (response.ok) {
            return response.json()
        }
        else {
            return response.json().then(error => {
                throw new Error(JSON.stringify(error))
            })
        }
    })
    .then(responseData => {})
    .catch(function (error) {
        console.error('Unable to send bulk notification trigger request', error)
    })
}

document.getElementById('trigger-notifications')
        .addEventListener('click', triggerBulkPushNotification)
