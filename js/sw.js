var urlsToPrefetch = [
  '/',
  '/styles.css',
  '/normalize.css',
  '/manifest.json'
];

var version = '4'

self.addEventListener("install", function(event) {
  event.waitUntil(
    caches
      .open(version + 'fundamentals')
      .then(function(cache) {
        return cache.addAll(urlsToPrefetch);
      })
  );
});

self.addEventListener("fetch", function(event) {
  console.log('test')
    if (event.request.method !== 'GET') {
        return;
    } else {
        event.respondWith(
            caches.match(event.request)
            .then(response => {
                if (response === undefined) return fetch(event.request)
                else return response
            })
        )
    }
});

self.addEventListener("activate", function(event) {
  event.waitUntil(
    caches
      .keys()
      .then(function (keys) {
        return Promise.all(
          keys
            .filter(function (key) {
              return !key.startsWith(version);
            })
            .map(function (key) {
              return caches.delete(key);
            })
        );
      })
  );
});