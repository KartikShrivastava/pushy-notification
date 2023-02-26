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
        const subscriberUList = document.querySelector('.subscriber-unordered-list')
        
        // clear the list first
        subscriberUList.innerHTML = ''
        
        subscribers.forEach(subscriber => {
            const markup = `<li>${JSON.stringify(subscriber)}</li>`
            subscriberUList.insertAdjacentHTML('beforeend', markup)
        })
    })
    .catch(function (err) {
        console.error('Unable to get subscribers from database.', err)
    })
}

document.getElementById('refresh-subscribers').addEventListener('click', getAllSubscribers)
