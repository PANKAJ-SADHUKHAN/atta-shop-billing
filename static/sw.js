const CACHE_NAME = "atta-shop-v1";

self.addEventListener("install", event => {

    event.waitUntil(

        caches.open(CACHE_NAME)

        .then(cache => {

            return cache.addAll([
                "/",
                "/login",
                "/menu",
                "/atta",
                "/dashboard"
            ]);

        })
    );
});
