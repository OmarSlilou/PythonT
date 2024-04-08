import pymongo
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

root = Tk()
root.title("Gestion des utilisateurs")
root.geometry("1500x720")
my_tree = ttk.Treeview(root)
storeName = "Gestion des utilisateurs"

client = pymongo.MongoClient("mongodb://localhost/")
db = client["user_management"]
collection = db["users"]

def insert(id, nom, prenom, telephone, email, date_naissance):
    user_data = {
        "userID": id,
        "nom": nom,
        "prenom": prenom,
        "telephone": telephone,
        "email": email,
        "date_naissance": date_naissance
    }
    collection.insert_one(user_data)

def delete(data):
    collection.delete_one({"userID": data})

def update(id, nom, prenom, telephone, email, date_naissance, idName):
    query = {"userID": idName}
    new_values = {"$set": {
        "userID": id,
        "nom": nom,
        "prenom": prenom,
        "telephone": telephone,
        "email": email,
        "date_naissance": date_naissance
    }}
    collection.update_one(query, new_values)

def read():
    results = collection.find().sort("userID", pymongo.DESCENDING)
    return results

def delete_data():
    selected_item = my_tree.selection()
    if selected_item:
        values = my_tree.item(selected_item, 'values')
        delete(values[0])  

        for data in my_tree.get_children():
            my_tree.delete(data)
        display_data()
    else:
        messagebox.showinfo("Erreur", "Veuillez sélectionner un élément à supprimer.")

def insert_data():
    userID = entryID.get()
    nom = entryNom.get()
    prenom = entryPrenom.get()
    telephone = entryTelephone.get()
    email = entryEmail.get()
    date_naissance = entryDateNaissance.get()  
    if userID == "" or nom == "" or prenom == "":
        messagebox.showinfo("Erreur", "L'ID, le Nom et le Prénom ne peuvent pas être vides.")
        return
    insert(userID, nom, prenom, telephone, email, date_naissance)
    for data in my_tree.get_children():
        my_tree.delete(data)
    display_data()

def update_data():
    selected_item = my_tree.selection()
    if selected_item:
        selected_id = my_tree.item(selected_item, 'values')[0]
        new_id = entryID.get()
        new_nom = entryNom.get()
        new_prenom = entryPrenom.get()
        new_telephone = entryTelephone.get()
        new_email = entryEmail.get()
        new_date_naissance = entryDateNaissance.get()  

        if new_id == "" or new_nom == "" or new_prenom == "":
            messagebox.showinfo("Erreur", "L'ID, le Nom et le Prénom ne peuvent pas être vides.")
            return

        query = {"userID": selected_id}
        new_values = {"$set": {
            "userID": new_id,
            "nom": new_nom,
            "prenom": new_prenom,
            "telephone": new_telephone,
            "email": new_email,
            "date_naissance": new_date_naissance
        }}
        collection.update_one(query, new_values)


        for data in my_tree.get_children():
            my_tree.delete(data)
        display_data()
    else:
        messagebox.showinfo("Erreur", "Veuillez sélectionner un élément à mettre à jour.")

def display_data():
    counter = 0
    results = read()
    sorted_results = sorted(results, key=lambda x: x['userID'], reverse=True)
    for result in sorted_results:
        my_tree.insert(parent='', index='end', iid=counter, text="", values=(result['userID'], result['nom'], result['prenom'], result['telephone'], result['email'], result['date_naissance']), tag="orow")
        counter += 1
    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial bold', 15))
    my_tree.grid(row=1, column=5, columnspan=6, rowspan=5, padx=10, pady=10)

def on_tree_select(event):
    selected_item = my_tree.selection()
    if selected_item:
        values = my_tree.item(selected_item, 'values')
        entryID.delete(0, END)
        entryNom.delete(0, END)
        entryPrenom.delete(0, END)
        entryTelephone.delete(0, END)
        entryEmail.delete(0, END)
        entryDateNaissance.set_date(values[5])  
        entryID.insert(0, values[0])
        entryNom.insert(0, values[1])
        entryPrenom.insert(0, values[2])
        entryTelephone.insert(0, values[3])
        entryEmail.insert(0, values[4])

my_tree.bind('<ButtonRelease-1>', on_tree_select)

titleLabel = Label(root, text=storeName, font=('Arial bold', 30), bd=2)
titleLabel.grid(row=0, column=0, columnspan=8, padx=20, pady=20)

idLabel = Label(root, text="ID", font=('Arial bold', 15))
nomLabel = Label(root, text="Nom", font=('Arial bold', 15))
prenomLabel = Label(root, text="Prénom", font=('Arial bold', 15))
telephoneLabel = Label(root, text="Téléphone", font=('Arial bold', 15))
emailLabel = Label(root, text="Email", font=('Arial bold', 15))
dateNaissanceLabel = Label(root, text="Date de Naissance", font=('Arial bold', 15))

idLabel.grid(row=1, column=0, padx=10, pady=10)
nomLabel.grid(row=2, column=0, padx=10, pady=10)
prenomLabel.grid(row=3, column=0, padx=10, pady=10)
telephoneLabel.grid(row=4, column=0, padx=10, pady=10)
emailLabel.grid(row=5, column=0, padx=10, pady=10)
dateNaissanceLabel.grid(row=6, column=0, padx=10, pady=10)

entryID = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryNom = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryPrenom = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryTelephone = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryEmail = Entry(root, width=25, bd=5, font=('Arial bold', 15))
entryDateNaissance = DateEntry(root, width=25, bd=5, font=('Arial bold', 15))

entryID.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
entryNom.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
entryPrenom.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
entryTelephone.grid(row=4, column=1, columnspan=3, padx=5, pady=5)
entryEmail.grid(row=5, column=1, columnspan=3, padx=5, pady=5)
entryDateNaissance.grid(row=6, column=1, columnspan=3, padx=5, pady=5)

buttonEnter = Button(
    root, text="Enter", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="green", command=insert_data)
buttonEnter.grid(row=7, column=1, columnspan=1)

buttonUpdate = Button(
    root, text="Update", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="#ffff00", command=update_data)
buttonUpdate.grid(row=7, column=2, columnspan=1)

buttonDelete = Button(
    root, text="Delete", padx=5, pady=5, width=5,
    bd=3, font=('Arial', 15), bg="#ff0000", command=delete_data)
buttonDelete.grid(row=7, column=3, columnspan=1)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial bold', 15))

my_tree['columns'] = ("ID", "Nom", "Prénom", "Téléphone", "Email", "Date de Naissance")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=100)
my_tree.column("Nom", anchor=W, width=150)
my_tree.column("Prénom", anchor=W, width=150)
my_tree.column("Téléphone", anchor=W, width=150)
my_tree.column("Email", anchor=W, width=200)
my_tree.column("Date de Naissance", anchor=W, width=150)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Nom", text="Nom", anchor=W)
my_tree.heading("Prénom", text="Prénom", anchor=W)
my_tree.heading("Téléphone", text="Téléphone", anchor=W)
my_tree.heading("Email", text="Email", anchor=W)
my_tree.heading("Date de Naissance", text="Date de Naissance", anchor=W)

display_data()

root.mainloop()
