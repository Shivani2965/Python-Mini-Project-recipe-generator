# Python-Mini-Project-recipe-generator
Recipe generator based on ingredients available on hand. Recipes are generated using Spooncular API, food APIs. Includes Features with saving recipes, Exporting into pdf printable files or saving into local storage.

🍪 Smart Recipe Generator
A Python desktop application that helps you discover recipes based on ingredients you already have at home. Built with Tkinter and powered by the Spoonacular API.

✨ Features

Ingredient-Based Search — Enter ingredients you have and get matching recipe suggestions instantly
Filter Options — Narrow results by cuisine type, cooking time, and difficulty level
Recipe Details — View full recipe info including ingredients, step-by-step instructions, and a dish image
Save Recipes — Store your favourite recipes locally using SQLite
Export to PDF — Export any saved recipe (with image, ingredients, and instructions) as a PDF file
Delete Saved Recipes — Manage your saved recipe collection


🛠️ Tech Stack
ToolPurposePython 3Core languageTkinterGUI frameworkSpoonacular APIRecipe dataPillow (PIL)Image loading & displaySQLite3Local recipe storagefpdfPDF exportRequestsHTTP calls

📦 Installation
1. Clone the repository
bashgit clone https://github.com/Shivani2965/Python-Mini-Project-recipe-generator.git
cd Python-Mini-Project-recipe-generator
2. Install dependencies
bashpip install requests pillow fpdf
3. Add your Spoonacular API key
Open main.py and replace the API key on line 14:
pythonAPI_KEY = "your_api_key_here"

Get a free API key at spoonacular.com/food-api

4. Run the app
bashpython main.py

🚀 How to Use

Home Page — Welcome screen with an overview of the app
Explore Recipes — Type in ingredients (e.g. chicken, garlic) and optionally select cuisine, time, and difficulty filters, then click Get Recipes
View Details — Click any recipe in the list to see its image, ingredients, and instructions
Save — Hit Save Recipe to store it locally
Saved Recipes — Navigate to the Saved Recipes page to view, export to PDF, or delete saved recipes


📁 Project Structure
Python-Mini-Project-recipe-generator/
│
├── main.py           # Main application file
├── recipes.db        # SQLite database (auto-created on first run)
└── README.md

⚠️ Notes

A valid Spoonacular API key is required for the app to fetch recipes
The free tier of the Spoonacular API has a daily request limit
An active internet connection is needed to load recipes and images


📄 License
This project is open source and available under the MIT License.

Made with 🍳 by Shivani
