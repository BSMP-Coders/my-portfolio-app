import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "entries.json")


def load_entries():
    """Load all journal entries from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_entries(entries):
    """Save entries to the JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=2)


@app.route("/")
def home():
    entries = load_entries()
    return render_template("index.html", entries=entries)


@app.route("/entry/<int:entry_id>")
def entry(entry_id):
    entries = load_entries()
    if entry_id < 0 or entry_id >= len(entries):
        return "Entry not found", 404
    return render_template("entry.html", entry=entries[entry_id], entry_id=entry_id)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        summary = request.form.get("summary", "").strip()
        learned = request.form.get("learned", "").strip()
        coolest = request.form.get("coolest", "").strip()
        screenshot = request.form.get("screenshot", "").strip()
        entry_date = request.form.get("date", "").strip()

        if not title or not summary:
            return render_template("add.html", error="Title and summary are required.")

        entries = load_entries()
        entries.append({
            "title": title,
            "date": entry_date,
            "summary": summary,
            "learned": learned,
            "coolest": coolest,
            "screenshot": screenshot
        })
        save_entries(entries)
        return redirect(url_for("home"))

    return render_template("add.html", error=None)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
