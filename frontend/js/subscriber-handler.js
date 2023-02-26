subscribersStore = []

function getAllSubscribers() {
    return fetch('http://127.0.0.1:8000/subscribers/', {
        method: 'GET',
    })
    .then(function (response) {
        if(!response.ok)
            throw new Error('Bad status code from server.')
        return response.json()
    })
    .then(function (subscribers) {
        subscribersStore = subscribers

        const subscriberOrderedList = document.getElementById('subscriber-ordered-list')
        
        // clear the list
        subscriberOrderedList.innerHTML = ''
        
        subscribers.forEach((subscriber, index) => {
            const listItem = document.createElement('li')

            // Add click event listener and select subscriber as click event
            listItem.addEventListener('click', () => {
                listItem.classList.toggle('selected')

                if (listItem.classList.contains('selected'))
                    listItem.style.border = '2px solid green'
                else
                    listItem.style.border = 'none'
            })

            listItem.textContent = subscriber.subscriber_id
            listItem.dataset.index = index

            subscriberOrderedList.appendChild(listItem)
        })
    })
    .catch(function (err) {
        console.error('Unable to get subscribers from database.', err)
    })
}

document.getElementById('refresh-subscribers').addEventListener('click', getAllSubscribers)
