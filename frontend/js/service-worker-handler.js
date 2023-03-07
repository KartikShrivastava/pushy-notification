function startWebPushNotificationFlow() {
  // Check if browser support web push and notifications
  if(!('serviceWorker' in navigator) || !('PushManager' in window)) {
      return
  }

  // Register service worker
  const registerServiceWorkerPromise = registerServiceWorker()

  // Request for user permission if not asked before
  if (Notification.permission === 'default') {
    Promise.all([registerServiceWorkerPromise, requestNotificationPermission()])
      .then(function (values) {
        registrationObject = values[0]
        permissionResult = values[1]
        
        if (permissionResult === 'granted')
          return Promise.resolve(registrationObject)
        else
          return Promise.reject(new Error(permissionResult))
      })
      // Subscriber browser once user grants the permission
      .then(function (registrationObject) {
        return subscribeBrowser(registrationObject)
      })
      // Save pushSubscription object to the database
      .then(function (pushSubscriptionObject) {
        payloadData = convertPushSubscriptionToDBPayload(pushSubscriptionObject)
        return postPushSubscriptionToDatabase(payloadData)
      })
      // Throw error if permission is not granted
      .catch(function (err) {
        console.error('Notification permission not granted with', err)
      })
  }
}

// add event listener to button to start notification flow
document.getElementById('request-notification-permission')
        .addEventListener('click', startWebPushNotificationFlow)

function registerServiceWorker() {
  return navigator.serviceWorker
    .register('/frontend/js/service-worker.js')
    .then(function (registrationObject) {
        return registrationObject
    })
    .catch(function (err) {
        console.error('Unable to register service worker.', err)
    })
}

function requestNotificationPermission() {
  if (isRequestPermissionPromiseSupported()) {
    return Notification.requestPermission()
  }
  else {
    return new Promise(function (resolve, reject) {
      Notification.requestPermission(function (permissionResult) {
        resolve(permissionResult)
      })
    })
  }
}

function isRequestPermissionPromiseSupported() {
  try {
    Notification.requestPermission().then();
  } catch (e) {
    return false;
  }
  return true;
}

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function subscribeBrowser(registrationObject) {
  const subscribeOptions = {
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(
      // TODO: find a better way to fetch public vapid key from constants.py?
      'BMRyBDaAbT6TVIBhfqzlb392KYoTVbUqgBDS8Z9uUFA5h6YHtlWsxwXskXkiX6LNRuh0yOsw-zAbfiEMfBZncA8',
    ),
  }

  return registrationObject.pushManager.subscribe(subscribeOptions);
}

function convertPushSubscriptionToDBPayload(pushSubscriptionObject) {
  jsonData = JSON.parse(JSON.stringify(pushSubscriptionObject))
  return {
    'endpoint_url': jsonData.endpoint,
    'expiration_time': jsonData.expirationTime,
    'p256dh_key': jsonData.keys.p256dh,
    'auth_key': jsonData.keys.auth
  }
}

function postPushSubscriptionToDatabase(pushSubscriptionObject) {
  return fetch('http://127.0.0.1:8000/subscribers/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(pushSubscriptionObject)
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
