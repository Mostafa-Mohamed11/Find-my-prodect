import customtkinter as ctk
import threading
import webbrowser
import requests
from PIL import Image
from io import BytesIO

from data_collection import search_products
from data_processing import clean_data
from graph_analysis import build_graph, draw_graph, remove_isolated_nodes
from heatmap_analysis import kde_heatmap
from model_3d import plot_3d
from tkinter import filedialog

# =============================
# CONFIG
# =============================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1200x700")
app.title("Product Analyzer")

products = []
view_mode = "grid"

# 🔥 cache للصور
image_cache = {}

# =============================
# IMAGE LOADER (FAST + CACHE)
# =============================
def load_image(url):
    if not url:
        return None

    if url in image_cache:
        return image_cache[url]

    try:
        response = requests.get(url, timeout=3)
        img = Image.open(BytesIO(response.content))
        ctk_img = ctk.CTkImage(light_image=img, size=(120, 120))

        image_cache[url] = ctk_img
        return ctk_img
    except:
        return None

# =============================
# CLEAR
# =============================
def clear():
    for w in app.winfo_children():
        w.destroy()

#######################################################################################
# =============================
# RATE FUNCTION (NEW FEATURE)
# =============================
def show_rate_window():
    rate_win = ctk.CTkToplevel(app)
    rate_win.geometry("400x300")
    rate_win.title("Rate Us")
    rate_win.attributes("-topmost", True)

    ctk.CTkLabel(rate_win, text="Do you like the app?", font=("Arial", 20)).pack(pady=30)

    def display_bonus_image():
        
        img_win = ctk.CTkToplevel(app)
        img_win.title("Bonus View")
        try:
            
            raw_img = Image.open("bonus.jpeg")
            ctk_bonus = ctk.CTkImage(light_image=raw_img, size=(450, 450))
            ctk.CTkLabel(img_win, image=ctk_bonus, text="").pack(padx=20, pady=20)
            rate_win.destroy() 
        except Exception as e:
            ctk.CTkLabel(img_win, text="Could not find bonus.jpeg").pack(pady=20)

    btn_frame = ctk.CTkFrame(rate_win, fg_color="transparent")
    btn_frame.pack(pady=20)

    ctk.CTkButton(btn_frame, text="Yes", width=100, command=display_bonus_image).pack(side="left", padx=20)
    ctk.CTkButton(btn_frame, text="No", width=100, command=display_bonus_image).pack(side="right", padx=20)
#######################################################################################

# =============================
# SEARCH PAGE
# =============================
def build_search_page():
    clear()

    frame = ctk.CTkFrame(app)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(frame, text="🔍 Product Search", font=("Arial", 30)).pack(pady=40)

    entry = ctk.CTkEntry(frame, width=400, height=40)
    entry.pack(pady=10)

    def start_search():
        query = entry.get()
        if not query:
            return

        show_loading()

        def run():
            global products

            data = search_products(query)
            products = clean_data(data)

            for p in products:
                load_image(p.get("image", ""))

            app.after(0, build_options_page)

        threading.Thread(target=run).start()

    ctk.CTkButton(frame, text="Search", command=start_search, width=200, height=40).pack(pady=20)
    entry.bind("<Return>", lambda event: start_search())

# =============================
# LOADING
# =============================
def show_loading():
    clear()

    frame = ctk.CTkFrame(app)
    frame.pack(expand=True, fill="both")

    center = ctk.CTkFrame(frame, fg_color="transparent")
    center.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(center, text="Loading...", font=("Arial", 28)).pack(pady=20)

    bar = ctk.CTkProgressBar(center, width=700, height=25)
    bar.pack(pady=10)
    bar.start()

# =============================
# OPTIONS
# =============================
def build_options_page():
    clear()

    frame = ctk.CTkFrame(app)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    ctk.CTkLabel(frame, text="Choose Action", font=("Arial", 28)).pack(pady=30)

    threshold = ctk.CTkEntry(frame, placeholder_text="Threshold")
    threshold.pack(pady=10)

    def run_graph():
        try:
            th = int(threshold.get())
            G = build_graph(products, th)
            G = remove_isolated_nodes(G)
            draw_graph(G)
        except:
            pass

    ctk.CTkButton(frame, text="Show Products", command=build_results_page, width=300).pack(pady=10)
    ctk.CTkButton(frame, text="Graph", command=run_graph, width=300).pack(pady=10)
    ctk.CTkButton(frame, text="Heatmap", command=lambda: kde_heatmap(products), width=300).pack(pady=10)
    ctk.CTkButton(frame, text="3D", command=lambda: plot_3d(products), width=300).pack(pady=10)

#####################################################################################
#rate button
    ctk.CTkButton(frame, text="rate", command=show_rate_window, width=300, fg_color="#2ecc71", hover_color="#27ae60").pack(pady=10)
#######################################################################################

    ctk.CTkButton(frame, text="⬅ Back", command=build_search_page).pack(pady=20)

# =============================
# RECOMMEND
# =============================
def show_recommendations_fast(product):
    win = ctk.CTkToplevel(app)
    win.geometry("600x500")

    recs = [p for p in products if p != product][:3]

    for p in recs:
        card = ctk.CTkFrame(win, corner_radius=12)
        card.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(card, text=p["title"]).pack(anchor="w", padx=10)
        ctk.CTkLabel(card, text=f"${p['price']}", text_color="#4da6ff").pack(anchor="w", padx=10)

# =============================
# TOGGLE
# =============================
def toggle_view():
    global view_mode
    view_mode = "list" if view_mode == "grid" else "grid"
    build_results_page()

# =============================
# RESULTS
# =============================
def build_results_page():
    clear()

    main = ctk.CTkFrame(app)
    main.pack(expand=True, fill="both", padx=20, pady=20)

    top = ctk.CTkFrame(main, fg_color="transparent")
    top.pack(fill="x")

    ctk.CTkButton(top, text="Toggle View", command=toggle_view).pack(side="right")

    scroll = ctk.CTkScrollableFrame(main)
    scroll.pack(fill="both", expand=True)

    if view_mode == "grid":
        cols = 4

        for i, product in enumerate(products):
            card = ctk.CTkFrame(scroll, corner_radius=15)
            card.grid(row=i//cols, column=i%cols, padx=15, pady=15)

            img = load_image(product.get("image", ""))

            if img:
                ctk.CTkLabel(card, image=img, text="").pack(pady=10)
            else:
                ctk.CTkLabel(card, text="No Image").pack(pady=10)

            ctk.CTkLabel(card,
                text=product["title"][:40],
                wraplength=180
            ).pack(pady=5)

            ctk.CTkLabel(card,
                text=f"${product['price']}",
                text_color="#4da6ff"
            ).pack()

            ctk.CTkButton(card, text="View",
                command=lambda link=product["link"]: webbrowser.open(link)
            ).pack(pady=2)

            ctk.CTkButton(card, text="Recommend",
                command=lambda p=product: show_recommendations_fast(p)
            ).pack(pady=2)

    else:
        for product in products:
            card = ctk.CTkFrame(scroll, corner_radius=15)
            card.pack(fill="x", pady=10)

            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=10)

            img = load_image(product.get("image", ""))

            if img:
                ctk.CTkLabel(row, image=img, text="").pack(side="left", padx=10)
            else:
                ctk.CTkLabel(row, text="No Image").pack(side="left", padx=10)

            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="both", expand=True)

            ctk.CTkLabel(info, text=product["title"], font=("Arial", 14, "bold")).pack(anchor="w")
            ctk.CTkLabel(info, text=f"${product['price']}", text_color="#4da6ff").pack(anchor="w")

            btns = ctk.CTkFrame(row, fg_color="transparent")
            btns.pack(side="right")

            ctk.CTkButton(btns, text="View",
                command=lambda link=product["link"]: webbrowser.open(link)
            ).pack(pady=3)

            ctk.CTkButton(btns, text="Recommend",
                command=lambda p=product: show_recommendations_fast(p)
            ).pack(pady=3)

    ctk.CTkButton(main, text="⬅ Back", command=build_options_page).pack(pady=10)

# =============================
# START
# =============================
build_search_page()
app.mainloop()