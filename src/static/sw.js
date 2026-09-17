// Teenustöötaja: äpp avaneb ka ilma võrguta (leht ja Firebase'i skriptid vahemälust).
const CACHE = "lehekogu-v1";
const CORE = ["./", "./index.html", "./manifest.webmanifest"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  const isGstatic = url.hostname === "www.gstatic.com";
  if (url.origin !== location.origin && !isGstatic) return;
  if (isGstatic) {
    // skriptid: enne vahemälu, siis võrk
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); return r; })));
    return;
  }
  // oma failid: enne võrk (uuendused jõuavad kohale), võrguta vahemälu
  e.respondWith(fetch(req).then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); return r; })
    .catch(() => caches.match(req).then(hit => hit || caches.match("./index.html"))));
});
