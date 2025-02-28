import tkinter as tk
from tkinter import messagebox, filedialog
import json

#update color previews
def update_color():
    r = r_slider.get()
    g = g_slider.get()
    b = b_slider.get()
    
    color = f"#{r:02x}{g:02x}{b:02x}"
    color_preview.config(bg=color)

#save colors to palette (important!)
def save_to_palette():
    r = r_slider.get()
    g = g_slider.get()
    b = b_slider.get()
    color = (r, g, b)
    
    #get palette
    palette_index = palette_listbox.curselection()
    if not palette_index:
        messagebox.showwarning("No Palette Selected", "Please select a palette to save the color to.")
        return
    
    palette_index = palette_index[0]
    
    #check for existence, otherwise make a new one
    if len(palettes) <= palette_index:
        palettes.append([])  

    #save color to the palette!
    palettes[palette_index].append(color)

    #update it
    update_palette_display(palette_index)
    save_palettes()

#function for updating, of course.
def update_palette_display(palette_index):
    #clear
    for widget in palette_frame.winfo_children():
        widget.destroy()
    
    palette = palettes[palette_index]
    
    #display colors for selected one
    for i, color in enumerate(palette):
        if color is None:
            continue

        #square to represent the color
        color_square = tk.Label(palette_frame, width=5, height=2, bg=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}", relief="solid")
        color_square.grid(row=i, column=palette_index)
        color_square.bind("<Button-1>", lambda event, i=i, palette_index=palette_index: open_edit_palette_window(palette_index, i))

    #empty square to show that there is room
    if len(palette) < 5:  #only allows 5 colors per palette
        empty_square = tk.Label(palette_frame, width=5, height=2, bg="white")
        empty_square.grid(row=len(palette), column=palette_index)

#save
def save_palettes():
    with open("palettes.json", "w") as f:
        json.dump(palettes, f)

#load
def load_palettes():
    try:
        with open("palettes.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [[] for _ in range(10)]  #you get 10 empty ones for free!

#deletion function
def delete_palette():
    selected_palette_index = palette_listbox.curselection()
    if not selected_palette_index:
        messagebox.showwarning("No Palette Selected", "Please select a palette to delete.")
        return

    selected_palette_index = selected_palette_index[0]
    palettes[selected_palette_index] = []  #for clearing the selected one so deleting is precise
    save_palettes()

    #show preview, update it
    update_palette_display(selected_palette_index)

    #clear selection
    palette_listbox.selection_clear(0, tk.END)
    palette_listbox.activate(selected_palette_index)

#basic features that every program needs!
def open_edit_palette_window(palette_index, color_index):
    
    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit Color in Palette {palette_index + 1}")
    
    
    color = palettes[palette_index][color_index]
    r, g, b = color

    
    r_slider_edit = tk.Scale(edit_window, from_=0, to=255, orient="horizontal", label="Red", command=lambda val: update_edit_color(r_slider_edit, g_slider_edit, b_slider_edit, color_preview_edit))
    g_slider_edit = tk.Scale(edit_window, from_=0, to=255, orient="horizontal", label="Green", command=lambda val: update_edit_color(r_slider_edit, g_slider_edit, b_slider_edit, color_preview_edit))
    b_slider_edit = tk.Scale(edit_window, from_=0, to=255, orient="horizontal", label="Blue", command=lambda val: update_edit_color(r_slider_edit, g_slider_edit, b_slider_edit, color_preview_edit))

    
    r_slider_edit.set(r)
    g_slider_edit.set(g)
    b_slider_edit.set(b)

    r_slider_edit.grid(row=0, column=1)
    g_slider_edit.grid(row=1, column=1)
    b_slider_edit.grid(row=2, column=1)

    
    color_preview_edit = tk.Label(edit_window, width=20, height=10, relief="solid", bg=f"#{r:02x}{g:02x}{b:02x}")
    color_preview_edit.grid(row=0, column=0, rowspan=3)

    
    save_button = tk.Button(edit_window, text="Save Changes", command=lambda: save_edited_color(palette_index, color_index, r_slider_edit, g_slider_edit, b_slider_edit, edit_window))
    save_button.grid(row=3, column=1)

#color previews when editing
def update_edit_color(r_slider_edit, g_slider_edit, b_slider_edit, color_preview_edit):
    r = r_slider_edit.get()
    g = g_slider_edit.get()
    b = b_slider_edit.get()
    color_preview_edit.config(bg=f"#{r:02x}{g:02x}{b:02x}")

#save edited color
def save_edited_color(palette_index, color_index, r_slider_edit, g_slider_edit, b_slider_edit, edit_window):
    r = r_slider_edit.get()
    g = g_slider_edit.get()
    b = b_slider_edit.get()
    color = (r, g, b)

    
    palettes[palette_index][color_index] = color
    save_palettes()

    #make sure to close the window!
    update_palette_display(palette_index)
    edit_window.destroy()

#export to txt
def export_selected_palette():
    selected_palette_index = palette_listbox.curselection()
    if not selected_palette_index:
        messagebox.showwarning("No Palette Selected", "Please select a palette to export.")
        return

    selected_palette_index = selected_palette_index[0]
    palette = palettes[selected_palette_index]

    
    content = f"Palette {selected_palette_index + 1} RGB Values:\n"
    for color in palette:
        if color:  #no need for the empty ones
            content += f"RGB({color[0]}, {color[1]}, {color[2]})\n"

    #file location
    file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file:
        with open(file.name, "w") as f:
            f.write(content)
        messagebox.showinfo("Export Complete", "Selected palette successfully exported!")

root = tk.Tk()
root.title("Color Palette Creator")


palettes = load_palettes()


r_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Red", command=lambda val: update_color())
g_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Green", command=lambda val: update_color())
b_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Blue", command=lambda val: update_color())

r_slider.grid(row=0, column=1)
g_slider.grid(row=1, column=1)
b_slider.grid(row=2, column=1)


color_preview = tk.Label(root, width=20, height=10, relief="solid")
color_preview.grid(row=0, column=0, rowspan=3)


save_button = tk.Button(root, text="Save to Palette", command=save_to_palette)
save_button.grid(row=3, column=1)


palette_frame = tk.Frame(root)
palette_frame.grid(row=4, column=0, columnspan=3)


instruction_label = tk.Label(root, text="Click a square to edit the color.", anchor="w")
instruction_label.grid(row=4, column=0, sticky="w")


palette_listbox = tk.Listbox(root, height=10, width=30)
palette_listbox.grid(row=4, column=2)
for i in range(10):  
    palette_listbox.insert(tk.END, f"Palette {i+1}")


def on_palette_select(event):
    selected_palette_index = palette_listbox.curselection()
    if selected_palette_index:
        update_palette_display(selected_palette_index[0])

palette_listbox.bind('<<ListboxSelect>>', on_palette_select)


delete_button = tk.Button(root, text="Delete Palette", command=delete_palette)
delete_button.grid(row=5, column=2)

export_button = tk.Button(root, text="Export Selected Palette", command=export_selected_palette)
export_button.grid(row=6, column=2)

root.mainloop()
#everything else functions amazingly