function startWebPushNotificationFlow() {
  // Check if browser support web push and notifications
  if(!('serviceWorker' in navigator) || !('PushManager' in window)) {
      return
  }

  // Register service worker
  const registerServiceWorkerPromise = registerServiceWorker()

  // Request for user permission if not asked before
  if (Notification.permission === 'default') {
    registerServiceWorkerPromise
      .then(function (registrationInfo) {
        return requestNotificationPermission()
      })
      .then(function (permissionResult) {
        handleNotificationPermission(permissionResult)
      })
  }
}

function registerServiceWorker() {
  return navigator.serviceWorker
    .register('./static/service-worker.js')
    .then(function (registrationInfo) {
        console.log('Service worker registered with registration info: ', registrationInfo)
        return registrationInfo
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

function handleNotificationPermission(permissionResult) {
  if (permissionResult !== 'granted') {
    console.log('Notification permission not granted.');
  }
  else if (permissionResult === 'granted') {
    console.log('Notification permission granted, bam!')
  }
}
