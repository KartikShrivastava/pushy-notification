function checkWebPushNotificationSupport() {
    if(!('serviceWorker' in navigator)) {
        return
    }
    
    if(!('PushManager' in window)) {
        return
    }

    registerServiceWorker()
}

function registerServiceWorker() {
    return navigator.serviceWorker
        .register('./static/service-worker.js')
        .then(function (registration) {
            console.log('Service worker registered.', registration)
            askPermission()
            return registration
        })
        .catch(function (err) {
            console.error('Unable to register service worker.', err)
        })
}

function askPermission() {
    return new Promise(function (resolve, reject) {
      const permissionResult = Notification.requestPermission(function (result) {
        resolve(result);
      });
  
      if (permissionResult) {
        permissionResult.then(resolve, reject);
      }
    }).then(function (permissionResult) {
      if (permissionResult !== 'granted') {
        throw new Error("We weren't granted permission.");
      }
    });
  }
