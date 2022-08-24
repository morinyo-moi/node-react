const cacheName = 'insurance-v1';
const staticAssets = [
  '/static/style00001.css',
  '/static/script40.js',
  '/static/script10.js',
  '/static/script20.js',
  '/static/script30.js',  
  '/static/model_map.csv',
  '/static/source_quotes.py',
  '/static/quotes/trident_ins.py',
  '/static/quotes/pioneer_ins.py',
  '/static/quotes/madison_ins.py',
  '/static/quotes/jubilee_ins.py',
  '/static/quotes/sanlam_ins.py',
  '/static/quotes/directline.py',
  '/static/quotes/britam_ins.py',
   '/static/quotes/uap_ins.py',
  '/static/quotes/corporate_ins.py',
  '/static/images/bg-intro-desktop.png',
  '/static/images/bg-intro-mobile.png',
  'static/images/sortmycarke-logo.png',
  'static/images/maskable_icon_x192.png',
  'static/images/maskable_icon_x384.png',
  'static/images/maskable_icon_x512.png',
];

self.addEventListener('install', async e => {
  const cache = await caches.open(cacheName);
  await cache.addAll(staticAssets);
  return self.skipWaiting();
});

self.addEventListener('activate', e => {
  self.clients.claim();
});

self.addEventListener('fetch', async e => {
  const req = e.request;
  const url = new URL(req.url);

  if (url.origin === location.origin) {
    e.respondWith(cacheFirst(req));
  } else {
    e.respondWith(networkAndCache(req));
  }
});

async function cacheFirst(req) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  return cached || fetch(req);
}

async function networkAndCache(req) {
  const cache = await caches.open(cacheName);
  try {
    const fresh = await fetch(req);
    await cache.put(req, fresh.clone());
    return fresh;
  } catch (e) {
    const cached = await cache.match(req);
    return cached;
  }
}
