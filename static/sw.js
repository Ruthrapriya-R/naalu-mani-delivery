// ✅ Naalu Mani Delivery - Service Worker (Offline Safe Version)
const CACHE_NAME = "naalu-mani-v4";

const ASSETS_TO_CACHE = [
  "/",
  "/catalog",
  "/contact",
  "/static/style.css",
  "/static/ui.js",
  "/static/images/logo.png"
];

// 🔹 INSTALL EVENT
self.addEventListener("install", (event) => {
  console.log("Installing service worker & caching assets...");
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS_TO_CACHE))
      .then(() => self.skipWaiting())
  );
});

// 🔹 ACTIVATE EVENT
self.addEventListener("activate", (event) => {
  console.log("Service worker activated ✅");
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log("Deleting old cache:", key);
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
});

// 🔹 FETCH EVENT (safe offline fallback)
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Cache fresh responses
        const clone = response.clone();
        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        return response;
      })
      .catch(async () => {
        const cached = await caches.match(event.request);
        if (cached) return cached;

        // Fallback for HTML pages (avoid error)
        if (event.request.destination === "document") {
          return new Response(
            "<h1 style='text-align:center;font-family:Poppins;color:#6C63FF;margin-top:40px;'>😕 You’re Offline<br><small>Please check your connection.</small></h1>",
            { headers: { "Content-Type": "text/html" } }
          );
        }
      })
  );
});
