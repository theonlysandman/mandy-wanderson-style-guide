# 👔 Style Agent – Outfit Picker

A fun, visual outfit planner that lets you mix and match your wardrobe right in the browser. Flip through tops, bottoms, shoes, and outerwear to build the perfect look — or hit shuffle and let fate decide.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![No frameworks](https://img.shields.io/badge/Frontend-vanilla%20HTML%2FJS-orange)

---

## What it does

- **Browse your wardrobe** — cycle through clothing items arranged in a person-shaped silhouette (outerwear → top → bottom → shoes).
- **Shuffle outfits** — randomize everything with one click.
- **Add new items** — snap a photo, pick a color, tag the occasion and season, and it's saved to your wardrobe.
- **Upload your face** — click the avatar circle to add your photo at the top of the outfit card.
- **Everything persists** — your wardrobe and photos are saved locally so they're there next time you open the app.

---

## Quick start

You only need **Python 3.8+** (no pip installs, no npm, no build step).

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/mandy-wanderson-style-guide.git
cd mandy-wanderson-style-guide

# 2. Start the server
python server.py

# 3. Open your browser
#    http://localhost:8123
```

That's it! The app opens on **port 8123** by default.

---

## Project structure

```
├── index.html        ← The entire front-end (HTML + CSS + JS, single file)
├── server.py         ← Lightweight Python server with REST API
├── wardrobe.json     ← Your saved wardrobe data (auto-generated)
├── uploads/          ← Uploaded clothing & face photos
├── screenshots/      ← For your own screenshots (git-ignored)
├── .gitignore
└── README.md
```

### How the pieces fit together

| Layer | Tech | Notes |
|-------|------|-------|
| **Front-end** | Vanilla HTML, CSS, JS | Single `index.html`, no build tools needed |
| **Back-end** | Python `http.server` | Zero dependencies — uses only the standard library |
| **Storage** | JSON file + filesystem | `wardrobe.json` for data, `uploads/` for images |

---

## Using the app

### Browse outfits
Use the **◀ ▶** arrows next to each clothing slot to cycle through your items.

### Shuffle
Click **🎲 Shuffle Everything** to randomize all four slots at once.

### Add clothing
1. Click **＋ Add Clothing** in the header.
2. Fill in the name, category, color, and optionally attach a photo.
3. Check the occasions (casual / work / formal) and seasons that apply.
4. Click **Add to Wardrobe** — the item is saved and immediately shown.

### Upload your face
Click the avatar circle at the top of the outfit card to upload a photo of yourself.

---

## API reference

The Python server exposes a small REST API (used by the front-end):

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/wardrobe` | Returns the full wardrobe JSON |
| `POST` | `/api/wardrobe` | Saves wardrobe JSON (body: JSON) |
| `POST` | `/api/upload` | Uploads a clothing photo (multipart form) |
| `POST` | `/api/face` | Uploads a face photo (multipart form) |

---

## Customization

- **Change the port** — edit `PORT = 8123` at the top of `server.py`.
- **Reset your wardrobe** — delete `wardrobe.json` and restart; the app will load built-in defaults.
- **Add default items** — edit the `defaultWardrobe` object inside `index.html`.

---

## License

This is a personal project. Feel free to fork and make it your own!
