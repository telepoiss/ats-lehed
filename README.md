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

Projekt on olemas: `ats-lehed-qpu23-4cd68` (konsool: https://console.firebase.google.com/project/ats-lehed-qpu23-4cd68). Reeglid on kaustas `firebase/`, uuendamiseks:

```bash
cd firebase && npx -y firebase-tools deploy --only firestore:rules
```

Uue projekti loomiseks:

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

Kõik, kes avavad https://telepoiss.github.io/ats-lehed/, jagavad ühte kogu (`DEFAULT_KOGU` failis `src/config.js`). Eraldi kogu saab lingiga `#kogu=minukood`.
Päises olev nupp "Jaga" kopeerib lingi.
