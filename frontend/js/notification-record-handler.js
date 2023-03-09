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

    console.log(JSON.stringify(sendPayload))
}

document.getElementById('trigger-notifications')
        .addEventListener('click', triggerBulkPushNotification)
