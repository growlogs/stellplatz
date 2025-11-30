self.addEventListener("install", e => {
    e.waitUntil(
        caches.open("stellplatz-cache").then(cache => {
            return cache.addAll([
                "/",
                "/static/manifest.json"
            ]);
        })
    );
});

self.addEventListener("fetch", e => {
    e.respondWith(
        fetch(e.request).catch(() => caches.match(e.request))
    );
});
