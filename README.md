# Atsi lehekogu

Telefonisõbralik veebiäpp kooli lehekogu jaoks: 15 puud, äratundmise tunnused, pildid,
linnukesed kogutud osade kohta ja sildi andmed (koht, korjaja, kuupäev).

Äpp: **https://telepoiss.github.io/ats-lehed/**

## Failid

- `src/data.js` – puude nimekiri ja tekstid. **Siin muuda sisu.**
- `src/app.html` – äpi paigutus ja loogika.
- `src/config.js` – Firebase'i seadistus (jagatud andmebaas). Kuni `null`, salvestub ainult seadmesse.
- `src/static/` – manifest, teenustöötaja (offline), ikoonid.
- `images/*.jpg` – fotod (Wikimedia Commons, autorid failis `images/credits.json`).
- `build.py` – paneb kõik kokku.
- `docs/` – valmis äpp, mida GitHub Pages serveerib. Ära muuda käsitsi, käivita `build.py`.

## Ehitamine ja avaldamine

```bash
python3 build.py
git add -A && git commit -m "Uuendus" && git push
```

GitHub Pages uuendab lehe paari minuti jooksul.

## Kohalik eelvaade

```bash
python3 -m http.server 8765 --directory docs
```

Ava http://localhost:8765

## Jagatud andmebaas (Firebase)

1. Loo projekt aadressil https://console.firebase.google.com (Google'i kontoga).
2. Build → Firestore Database → Create database → asukoht `europe-west` → **test mode**.
3. Project settings (hammasratas) → Your apps → `</>` Web → registreeri äpp → kopeeri `firebaseConfig`.
4. Kleebi see faili `src/config.js` (`window.FIREBASE_CONFIG = {...}`), ehita ja pushi.
5. Firestore → Rules, asenda reeglid:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /kogud/{kogu}/items/{item} {
      allow read, write: if true;
    }
  }
}
```

Iga kogul on oma kood lingis (`#kogu=abc123`). Kes avab sama lingi, näeb ja muudab sama nimekirja.
Päises olev nupp "Jaga" kopeerib selle lingi.
