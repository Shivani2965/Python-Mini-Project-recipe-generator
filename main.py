import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
from io import BytesIO
import sqlite3
from fpdf import FPDF
import urllib.request
import webbrowser

# --- API Setup ---
API_KEY = "28329bd5c5a442b7a60f17940d2fff26"
SEARCH_URL = "https://api.spoonacular.com/recipes/complexSearch"
RECIPE_INFO_URL = "https://api.spoonacular.com/recipes/{id}/information"


# Database Setup
conn = sqlite3.connect("recipes.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        title TEXT,
        ingredients TEXT,
        instructions TEXT,
        source_url TEXT
    )
""")
conn.commit()
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🍪 Recipe Generator ")
        self.geometry("1200x900")
        self.configure(bg="#fffaf0")

        self.sidebar_bg = "#8B5E3C"
        self.init_sidebar()
        self.init_home_page()
        

    def init_sidebar(self):
        self.sidebar = tk.Frame(self, bg=self.sidebar_bg, width=200)
        self.sidebar.pack(side="left", fill="y")

        buttons = [
            ("🏠 Home", self.show_home),
            ("🍳 Explore Recipes", self.show_explore),
            ("📖 Saved Recipes", self.show_saved),
            ("🚪 Exit", self.confirm_exit) 
        ]

        for text, command in buttons:
            b = tk.Button(self.sidebar, text=text, bg=self.sidebar_bg, fg="white", font=("Baloo", 12), bd=0,
                          activebackground="#A67B5B", activeforeground="white", command=command)
            b.pack(fill="x", pady=10, padx=10, anchor="w")

    def init_home_page(self):
        self.content = tk.Frame(self, bg="#FFF2EC")
        self.content.pack(side="right", fill="both", expand=True)

        # Background Image
        bg_image_url = "https://i.pinimg.com/736x/10/00/d6/1000d60ae0ec5b439b3f71325264fafa.jpg"
        self.bg_image = ImageTk.PhotoImage(Image.open(requests.get(bg_image_url, stream=True).raw).resize((1500, 1000)))
        self.bg_label = tk.Label(self.content, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        overlay = tk.Frame(self.content, bg="#FFF2EC", bd=0)
        overlay.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        heading = tk.Label(overlay, text="Welcome to Smart Recipe Generator", font=("Baloo", 24, "bold"),
                           fg="#8B5E3C", bg="#FFF2EC")
        heading.pack(pady=20)

        subheading = tk.Label(overlay, text="Cook smarter, not harder!", font=("Fredoka One", 16), fg="#A0522D", bg="#FFF2EC")
        subheading.pack(pady=5)

        quote = tk.Label(overlay, text="\"Baking is love made edible!\"", font=("Quicksand", 14), fg="#D2691E", bg="#FFF2EC")
        quote.pack(pady=10)

        desc = tk.Label(overlay, text="Discover recipes based on your ingredients! Save your favorites, generate shopping lists, and even export them to PDF. A fun, easy-to-use app for all your culinary needs.",
                        font=("Quicksand", 12), wraplength=500, justify="center", bg="#F6E7D7", fg="#4B2E2B", bd=2,
                        relief="groove", padx=10, pady=10)
        desc.pack(pady=20)

        explore_btn = tk.Button(overlay, text="🍪 Explore Recipes", font=("Baloo", 12), bg="#F6E7D7", fg="#4B2E2B",
                                padx=20, pady=10, bd=0, relief="raised", command=self.show_explore)
        explore_btn.pack(pady=10)

    def show_home(self):
        self.content.destroy()
        self.init_home_page()

    def confirm_exit(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.quit()  # Or use root.quit()

    def show_explore(self):
        self.content.destroy()
        self.content = tk.Frame(self, bg="#FFF2EC")
        self.content.pack(side="right", fill="both", expand=True)
        
        input_panel = tk.LabelFrame(self.content, text="🌟 What ingredients do you have?", font=("Comic Sans MS", 12), bg="#fcecd6", fg="#4b2e2e", padx=10, pady=10)
        input_panel.pack(fill="x", padx=10, pady=5)
        
        ingredient_entry = tk.Entry(input_panel, font=("Comic Sans MS", 12), width=40)
        ingredient_entry.grid(row=0, column=0, padx=10)
        
        cuisine_box = ttk.Combobox(input_panel, values=["Any", "Italian", "Chinese", "Indian", "Mexican"]) 
        cuisine_box.set("Cuisine 🍝")
        cuisine_box.grid(row=0, column=1, padx=10)
        
        time_box = ttk.Combobox(input_panel, values=["Any", "< 20 min", "20-40 min", "> 40 min"])
        time_box.set("Time ⏱️")
        time_box.grid(row=0, column=2, padx=10)
        
        difficulty_box = ttk.Combobox(input_panel, values=["Any", "Easy", "Medium", "Hard"])
        difficulty_box.set("Difficulty 🫑")
        difficulty_box.grid(row=0, column=3, padx=10)

        for box in [cuisine_box, time_box, difficulty_box]:
            box.configure(state="readonly")

        recipe_data = {}
        
        # Suggested Recipe Cards
        suggested_frame = tk.Frame(self.content, bg="#fffaf0")
        suggested_frame.pack(fill="x", padx=10)
        tk.Label(suggested_frame, text="Suggested Recipes 🍰", font=("Comic Sans MS", 14, "bold"), bg="#fff8dc").pack(pady=5)

        
        recipe_listbox = tk.Listbox(suggested_frame, font=("Comic Sans MS", 12), height=5)
        recipe_listbox.pack(fill="x", pady=5)
        
        # Recipe Details
        details_frame = tk.LabelFrame(self.content, text="🌟 Recipe Details", font=("Comic Sans MS", 12), bg="#fcecd6", fg="#4b2e2e", padx=10, pady=10)
        details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create a canvas inside the LabelFrame
        canvas = tk.Canvas(details_frame, bg="#fcecd6", highlightthickness=0)
        scroll_y = tk.Scrollbar(details_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#fcecd6")
        
        scroll_frame.bind(
             "<Configure>",
             lambda e: canvas.configure(scrollregion=canvas.bbox("all"))     )
        
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        
        
        # --- Function to show recipe details ---
        def show_recipe_details(event):
            for widget in scroll_frame.winfo_children():
                widget.destroy()

            selected = recipe_listbox.get(tk.ACTIVE)
            recipe_id = recipe_data.get(selected)
            if not recipe_id:
                return
            
            response = requests.get(
                RECIPE_INFO_URL.format(id=recipe_id),params={"apiKey": API_KEY, "includeNutrition": "true"})
            data = response.json()

            
            # 🧑‍🍳 Title
            title = tk.Label(scroll_frame, text=data["title"], font=("Comic Sans MS", 16, "bold"), bg="#fcecd6", fg="#4b2e2e")
            title.pack(pady=5)
            
            #  Image
            try:
                img_url = data.get("image", "")
                response = requests.get(img_url)
                img_data = Image.open(BytesIO(response.content)).resize((300, 300))
                img = ImageTk.PhotoImage(img_data)
                image_label = tk.Label(scroll_frame, image=img, bg="#fcecd6")
                image_label.image = img
                image_label.pack(pady=5)
            except:
                image_label = tk.Label(scroll_frame, text="[Image not available]", bg="#fcecd6")
                image_label.pack()
                
            # 🕒 Info row: Time, Difficulty, Cuisine
            time = data.get("readyInMinutes", 0)
            if time < 20:
                diff = "Easy"
            elif time <= 40:
                diff = "Medium"
            else:
                diff = "Hard"
            cuisine = ', '.join(data.get("cuisines", ["Unknown"]))
            
            info_text = f"🕒 Time: {time} min     🧩 Difficulty: {diff}     🍽 Cuisine: {cuisine}"
            info_label = tk.Label(scroll_frame, text=info_text, font=("Comic Sans MS", 10, "italic"), bg="#fcecd6", fg="#5a3a00")
            info_label.pack(pady=5)
            
            # 🧾 Ingredients
            ingredients_label = tk.Label(scroll_frame, text="🧾 Ingredients:", font=("Comic Sans MS", 12, "underline"), bg="#fcecd6")
            ingredients_label.pack(anchor="w", padx=10, pady=2)
            
            ingredients_frame = tk.Frame(scroll_frame, bg="#fcecd6")
            ingredients_frame.pack(anchor="w", padx=20)
            
            ingredients = data.get("extendedIngredients", [])
            if ingredients:
                for ing in ingredients:
                    name = ing.get("original", "")
                    ing_label = tk.Label(ingredients_frame, text="• " + name, font=("Comic Sans MS", 10), bg="#fcecd6", justify="left", anchor="w", wraplength=900)
                    ing_label.pack(anchor="w", pady=1)
                else:
                    ing_label = tk.Label(ingredients_frame, text="No ingredients found.", font=("Comic Sans MS", 10), bg="#fcecd6")
                    ing_label.pack()
 
            #  Instructions
            instructions_label = tk.Label(scroll_frame, text="📜 Instructions:", font=("Comic Sans MS", 12, "underline"), bg="#fcecd6")
            instructions_label.pack(anchor="w", padx=10, pady=5)
            
            instructions = data.get("instructions", "No instructions provided.")
            instructions_label = tk.Label(scroll_frame, text=instructions, font=("Comic Sans MS", 10), bg="#fcecd6", wraplength=900, justify="left")
            instructions_label.pack(anchor="w", padx=20)

           
        # --- Recipe Generator Function ---
        def generate_recipes():
            ingredient_query = ingredient_entry.get()
            cuisine_filter = cuisine_box.get()
            time_filter = time_box.get()
            difficulty_filter = difficulty_box.get()

            if not ingredient_query:
                messagebox.showwarning("Input Required", "Please enter ingredients.")
                return
            
            params = {"apiKey": API_KEY,
                "includeIngredients": ingredient_query,
                "number": 10}

            if cuisine_filter != "Cuisine 🍝" and cuisine_filter != "Any":
                params["cuisine"] = cuisine_filter
                params["time"] = time_filter
                params["difficulty"] = difficulty_filter

            
            response = requests.get(SEARCH_URL, params=params)
            data = response.json()
            recipes = data.get("results", [])
            
            recipe_listbox.delete(0, tk.END)
            recipe_data.clear()
            
            for recipe in recipes:
                # Fetch detailed info for time/difficulty filtering
                recipe_id = recipe["id"]
                detail_response = requests.get(RECIPE_INFO_URL.format(id=recipe_id), params={"apiKey": API_KEY})
                detail_data = detail_response.json()
                
                ready_in = detail_data.get("readyInMinutes", 0)
                
                # Map ready time to difficulty
                if ready_in < 20:
                    difficulty = "Easy"
                elif ready_in <= 40:
                    difficulty = "Medium"
                else:
                    difficulty = "Hard"
                    
                # Apply time filter
                if time_filter != "Time ⏱️" and time_filter != "Any":
                    if time_filter == "< 20 min" and ready_in >= 20:
                        continue
                    elif time_filter == "20-40 min" and (ready_in < 20 or ready_in > 40):
                        continue
                    elif time_filter == "> 40 min" and ready_in <= 40:
                        continue
                    
                # Apply difficulty filter
                if difficulty_filter != "Difficulty 🫑" and difficulty_filter != "Any":
                    if difficulty_filter != difficulty:
                        continue
                    
                # Passed all filters — add to list
                title = detail_data["title"]
                recipe_listbox.insert(tk.END, title)
                recipe_data[title] = recipe_id

                
        get_button = tk.Button(input_panel, text="🍽️ Get Recipes", bg="#fff0d6", font=("Comic Sans MS", 10), command=generate_recipes)
        get_button.grid(row=0, column=4, padx=10)
        button_frame = tk.Frame(details_frame, bg="#fcecd6")
        button_frame.pack(pady=10)

        def save_recipe():
            selected = recipe_listbox.get(tk.ACTIVE)
            recipe_id = recipe_data.get(selected)
            if not recipe_id:
                return

            response = requests.get(RECIPE_INFO_URL.format(id=recipe_id), params={"apiKey": API_KEY})
            data = response.json()

            title = data.get("title", "Unknown")
            ingredients = ', '.join([ing['original'] for ing in data.get("extendedIngredients", [])])
            instructions = data.get("instructions", "No instructions provided.")
            source_url = data.get("sourceUrl", "")

            cursor.execute("INSERT INTO recipes (title, ingredients, instructions, source_url) VALUES (?, ?, ?, ?)",
                           (title, ingredients, instructions, source_url))
            conn.commit()
            messagebox.showinfo("Saved", f"{title} has been saved to your recipe book!")

        # Reset Inputs Button
        def reset_inputs():
            ingredient_entry.delete(0, tk.END)
            cuisine_box.set("Cuisine 🍝")
            time_box.set("Time ⏱️")
            difficulty_box.set("Difficulty 🫑")
            recipe_listbox.delete(0, tk.END)
            for widget in scroll_frame.winfo_children():
                widget.destroy()


        # Bind selection to details display
        recipe_listbox.bind("<<ListboxSelect>>", show_recipe_details)

        bottom_bar = tk.Frame(self.content, bg="#fcecd6")
        bottom_bar.pack(side="bottom", fill="x", padx=10, pady=5)
        
        button_frame = tk.Frame(bottom_bar, bg="#fcecd6")
        button_frame.pack()

        reset_btn = tk.Button(button_frame, text="🔄 Reset", bg="#f7c59f", font=("Comic Sans MS", 10), command=reset_inputs)
        reset_btn.pack(side="left", padx=10)

        save_button = tk.Button(button_frame, text="💾 Save Recipe", font=("Comic Sans MS", 10), bg="#d9f7be", command=save_recipe)
        save_button.pack(side="left", padx=20)


    def show_saved(self):
        self.content.destroy()
        self.content = tk.Frame(self, bg="#FFF2EC")
        self.content.pack(side="right", fill="both", expand=True)

        # 🍩 Background Image
        bg_url = "https://i.pinimg.com/736x/47/49/fc/4749fccbc993851cbe1f93950ee296ed.jpg"
        self.bg_image = ImageTk.PhotoImage(
            Image.open(requests.get(bg_url, stream=True).raw).resize((1500, 1000)))
        
        self.bg_label = tk.Label(self.content, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
    
        overlay = tk.Frame(self.content, bg="#fff2ec", bd=0)
        overlay.place(relx=0.5, rely=0.5, anchor="center", width=650, height=460)
        title = tk.Label(overlay, text="🍰 Saved Recipes", font=("Baloo", 26, "bold"),
        bg="#fff2ec", fg="#844C2C")
        title.pack(pady=20)
        
        listbox_saved = tk.Listbox(
            overlay, width=55, height=10, font=("Arial", 12),
            bg="#fffaf7", fg="#5A3E36", bd=2, relief="ridge",
            highlightbackground="#FFD4B2", selectbackground="#FCD5B0")
        listbox_saved.pack(pady=10)
        
        cursor.execute("SELECT title FROM recipes")
        for row in cursor.fetchall():
            listbox_saved.insert(tk.END, row[0])
            
        # Buttons Frame
        btn_frame = tk.Frame(overlay, bg="#fff2ec")
        btn_frame.pack(pady=15)
        
        btn_delete = tk.Button(
            btn_frame, text="🗑 Delete", bg="#f7c59f", font=("Comic Sans MS", 10),
            command=lambda: self.delete_recipe(listbox_saved))
        
        btn_delete.pack(side="left", padx=20)
        
        btn_export = tk.Button(
            btn_frame, text="📄 Export to PDF", bg="#f7c59f", font=("Comic Sans MS", 10),
            command=lambda: self.export_pdf(listbox_saved))
        btn_export.pack(side="left", padx=20)
        
    def delete_recipe(self, listbox):
        try:
            selected = listbox.get(listbox.curselection())
            cursor.execute("DELETE FROM recipes WHERE title = ?", (selected,))
            conn.commit()
            listbox.delete(listbox.curselection())
            messagebox.showinfo("Deleted", "Recipe deleted successfully!")
        except:
            messagebox.showwarning("Select a Recipe", "Please select a recipe to delete.")

    def export_pdf(self, listbox):
        try:
            selected = listbox.get(listbox.curselection())
            cursor.execute("SELECT * FROM recipes WHERE title = ?", (selected,))
            recipe = cursor.fetchone()
            
            if recipe:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", style="B", size=16)
                pdf.cell(200, 10, recipe[1], ln=True, align='C')
                pdf.ln(10)
                
                cursor.execute("SELECT source_url FROM recipes WHERE title = ?", (selected,))
                source_url = cursor.fetchone()[0]
                
                # Use Spoonacular API to get image
                url = f"https://api.spoonacular.com/recipes/extract?url={source_url}&apiKey={API_KEY}"
                response = requests.get(url)
                data = response.json()
                image_url = data.get("image", None)
                
                if image_url:
                    image_response = requests.get(image_url)
                    img = Image.open(BytesIO(image_response.content))
                    image_path = "temp_recipe_image.jpg"
                    img.save(image_path)
                    pdf.image(image_path, x=10, y=30, w=100)
                    pdf.ln(60)
                else:
                    print("No image found.")
                    
                # Ingredients
                pdf.ln(5)
                pdf.set_font("Arial", style="B", size=14)
                pdf.cell(0, 10, "Ingredients:", ln=True)
                pdf.set_font("Arial", size=12)
                ingredients = recipe[2].strip("[]").replace("', '", "\n- ").replace("'", "- ")
                pdf.multi_cell(0, 8, f"- {ingredients}")
                pdf.ln(5)
                
                # Instructions
                pdf.set_font("Arial", style="B", size=14)
                pdf.cell(0, 10, "Instructions:", ln=True)
                pdf.set_font("Arial", size=12)
                instructions = recipe[3].strip("[]").replace("', '", "\n").replace("'", "")
                pdf.multi_cell(0, 8, instructions)
                pdf.ln(5)
                
                # Source
                pdf.set_font("Arial", style="B", size=14)
                pdf.cell(0, 10, "Source:", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 8, source_url, ln=True, link=source_url)
                
                file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
                if file_path:
                    pdf.output(file_path)
                    messagebox.showinfo("Success", "Recipe exported successfully!")
        except:
            messagebox.showwarning("Select a Recipe", "Please select a recipe to export.")


if __name__ == "__main__":
    try:
        import requests
        app = App()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"{e}")
