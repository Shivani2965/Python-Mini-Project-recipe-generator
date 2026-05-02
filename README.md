# 🍪 Smart Recipe Generator

A Python desktop application that helps you discover recipes based on ingredients you already have at home. Built with Tkinter and powered by the Spoonacular API.

---

## ✨ Features

- **Ingredient-Based Search** — Enter ingredients you have and get matching recipe suggestions instantly
- **Filter Options** — Narrow results by cuisine type, cooking time, and difficulty level
- **Recipe Details** — View full recipe info including ingredients, step-by-step instructions, and a dish image
- **Save Recipes** — Store your favourite recipes locally using SQLite
- **Export to PDF** — Export any saved recipe (with image, ingredients, and instructions) as a PDF file
- **Delete Saved Recipes** — Manage your saved recipe collection

---

## 🖥️ Screenshots

> *(Add screenshots of the Home, Explore, and Saved Recipes pages here)*

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| Tkinter | GUI framework |
| Spoonacular API | Recipe data |
| Pillow (PIL) | Image loading & display |
| SQLite3 | Local recipe storage |
| fpdf | PDF export |
| Requests | HTTP calls |

---

## 📦 Installation

**1. Clone the repository**
```bash
git clone https://github.com/Shivani2965/Python-Mini-Project-recipe-generator.git
cd Python-Mini-Project-recipe-generator
```

**2. Install dependencies**
```bash
pip install requests pillow fpdf
```

**3. Add your Spoonacular API key**

Open `main.py` and replace the API key on line 14:
```python
API_KEY = "your_api_key_here"
```
> Get a free API key at [spoonacular.com/food-api](https://spoonacular.com/food-api)

**4. Run the app**
```bash
python main.py
```

---

## 🚀 How to Use

1. **Home Page** — Welcome screen with an overview of the app
2. **Explore Recipes** — Type in ingredients (e.g. `chicken, garlic`) and optionally select cuisine, time, and difficulty filters, then click **Get Recipes**
3. **View Details** — Click any recipe in the list to see its image, ingredients, and instructions
4. **Save** — Hit **Save Recipe** to store it locally
5. **Saved Recipes** — Navigate to the Saved Recipes page to view, export to PDF, or delete saved recipes

---

## 📁 Project Structure

```
Python-Mini-Project-recipe-generator/
│
├── main.py           # Main application file
├── recipes.db        # SQLite database (auto-created on first run)
└── README.md
```

---

## ⚠️ Notes

- A valid [Spoonacular API key](https://spoonacular.com/food-api) is required for the app to fetch recipes
- The free tier of the Spoonacular API has a daily request limit
- An active internet connection is needed to load recipes and images

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

*Made with 🍳 by [Shivani](https://github.com/Shivani2965)*
