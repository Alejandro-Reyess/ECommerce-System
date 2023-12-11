import tkinter as tk
from tkinter import messagebox
from control.user_control import UserControl
from control.admin_user_control import AdminUserControl
from control.product_control import ProductControl


class AuthenticationView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")  # Definindo o tamanho da janela

        self.user_control = UserControl()

        # Login Window
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Username").pack()  # Nome do campo de usuário
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        tk.Label(self.login_frame, text="Password").pack()  # Nome do campo de senha
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(
            self.login_frame, text="Login", command=self.login
        )
        self.login_button.pack()

        self.register_button = tk.Button(
            self.login_frame, text="Register", command=self.show_register
        )
        self.register_button.pack()

        # Registration Window
        self.register_frame = tk.Frame(self.root)

        tk.Label(
            self.register_frame, text="Full Name"
        ).pack()  # Nome do campo de nome completo
        self.name_entry = tk.Entry(self.register_frame)
        self.name_entry.pack()

        tk.Label(self.register_frame, text="E-mail").pack()  # Nome do campo de e-mail
        self.email_entry = tk.Entry(self.register_frame)
        self.email_entry.pack()

        tk.Label(
            self.register_frame, text="Address"
        ).pack()  # Nome do campo de endereço
        self.address_entry = tk.Entry(self.register_frame)
        self.address_entry.pack()

        tk.Label(
            self.register_frame, text="Username"
        ).pack()  # Nome do campo de usuário
        self.new_username_entry = tk.Entry(self.register_frame)
        self.new_username_entry.pack()

        tk.Label(self.register_frame, text="Password").pack()  # Nome do campo de senha
        self.new_password_entry = tk.Entry(self.register_frame, show="*")
        self.new_password_entry.pack()

        self.finish_button = tk.Button(
            self.register_frame, text="Create Account", command=self.register_user
        )
        self.finish_button.pack()

        self.register_frame.pack_forget()
        self.admin_control = AdminUserControl()

        # Admin Login Button
        self.admin_login_button = tk.Button(
            self.root, text="Admin Login", command=self.admin_login
        )
        self.admin_login_button.place(x=10, y=10)  # Ajustando as coordenadas do botão

    def admin_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.admin_control.authenticate_admin(username, password):
            print("Admin Login successful!")
            self.root.withdraw()

            def return_to_login():
                self.root.deiconify()
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)

            root_manage_products = tk.Tk()
            AdminManageProductView(root_manage_products, return_to_login)
            root_manage_products.mainloop()
        else:
            print("Invalid admin credentials!")

    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_control.authenticate(username, password):
            print("User Login successful!")
        else:
            print("Invalid username or password!")

    def register_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        # Verifica se algum campo está vazio
        if not all([name, email, address, username, password]):
            messagebox.showerror("Error", "All fields are required")
            return

        # Verifica se algum campo possui apenas espaços em branco
        if any(
            [
                field.strip() == ""
                for field in [name, email, address, username, password]
            ]
        ):
            messagebox.showerror("Error", "Fields cannot be blank")
            return

        self.user_control.create_user(name, email, address, username, password)
        messagebox.showinfo(
            "Success", "Account registered successfully"
        )  # Popup de sucesso
        self.register_frame.pack_forget()
        self.login_frame.pack()

        # Limpa os campos após o registro
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.new_username_entry.delete(0, tk.END)
        self.new_password_entry.delete(0, tk.END)


class AdminManageProductView:
    def __init__(self, root, return_to_login):
        self.root = root
        self.root.title("Product Management")
        self.product_control = ProductControl([])
        self.root.geometry("600x400")
        self.return_to_login = return_to_login

        # Frame para a lista de produtos com barra de rolagem
        self.products_frame = tk.Frame(self.root)
        self.products_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.products_frame)
        self.scrollbar = tk.Scrollbar(
            self.products_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.show_products()

        add_button = tk.Button(
            self.root, text="Add New Product", command=self.add_product
        )
        add_button.pack(side=tk.BOTTOM, padx=20, pady=10)

        logout_button = tk.Button(self.root, text="Log Out", command=self.logout)
        logout_button.pack(
            side=tk.BOTTOM, padx=20, pady=10
        )  # Chamada para exibir os produtos na inicialização

    def show_products(self):
        self.product_control.load_products()  # Carrega os produtos

        for i, product in enumerate(self.product_control.products):
            tk.Label(
                self.scrollable_frame,
                text=f"ID: {product.product_id}, Name: {product.name}, "
                f"Category: {product.category}, Price: ${product.price}",
            ).grid(row=i, column=0, sticky=tk.W)

            edit_button = tk.Button(
                self.scrollable_frame,
                text="Edit",
                command=lambda prod=product: self.edit_product(prod),
            )
            edit_button.grid(row=i, column=1, padx=5)

            delete_button = tk.Button(
                self.scrollable_frame,
                text="Delete",
                command=lambda prod=product: self.delete_product(prod),
            )
            delete_button.grid(row=i, column=2, padx=5)

    def add_product(self):
        self.new_product_window = tk.Toplevel(self.root)
        self.new_product_window.title("Add New Product")

        tk.Label(self.new_product_window, text="ID").grid(row=0, column=0)
        tk.Label(self.new_product_window, text="Name").grid(row=1, column=0)
        tk.Label(self.new_product_window, text="Category").grid(row=2, column=0)
        tk.Label(self.new_product_window, text="Price").grid(row=3, column=0)

        self.new_product_id_entry = tk.Entry(self.new_product_window)
        self.new_product_id_entry.grid(row=0, column=1)
        self.new_name_entry = tk.Entry(self.new_product_window)
        self.new_name_entry.grid(row=1, column=1)
        self.new_category_entry = tk.Entry(self.new_product_window)
        self.new_category_entry.grid(row=2, column=1)
        self.new_price_entry = tk.Entry(self.new_product_window)
        self.new_price_entry.grid(row=3, column=1)

        add_button = tk.Button(
            self.new_product_window, text="Add Product", command=self.save_new_product
        )
        add_button.grid(row=4, columnspan=2, pady=10)

    def save_new_product(self):
        new_product_id = self.new_product_id_entry.get()
        new_name = self.new_name_entry.get()
        new_category = self.new_category_entry.get()
        new_price = self.new_price_entry.get()

        if not all([new_product_id, new_name, new_category, new_price]):
            messagebox.showerror("Error", "All fields are required")
            return

        if any(
            [
                field.strip() == ""
                for field in [new_product_id, new_name, new_category, new_price]
            ]
        ):
            messagebox.showerror("Error", "Fields cannot be blank")
            return

        if not self.product_control.create_product(
            new_product_id, new_name, new_category, new_price
        ):
            messagebox.showerror("Error", "Product ID or Name already exists")
            return

        messagebox.showinfo("Success", "Product created successfully")
        self.new_product_window.destroy()  # Fecha a janela de adição de produto
        self.refresh_product_list()  # Atualiza a lista de produtos

    def refresh_product_list(self):
        # Limpa a exibição atual dos produtos
        for widget in self.product_list_frame.winfo_children():
            widget.destroy()

        # Exibe novamente os produtos atualizados
        self.show_products()

    def edit_product(self, product):
        self.edit_product_window = tk.Toplevel(self.root)
        self.edit_product_window.title("Edit Product")

        tk.Label(self.edit_product_window, text="Name").grid(row=0, column=0)
        tk.Label(self.edit_product_window, text="Category").grid(row=1, column=0)
        tk.Label(self.edit_product_window, text="Price").grid(row=2, column=0)

        self.edit_name_entry = tk.Entry(self.edit_product_window)
        self.edit_name_entry.grid(row=0, column=1)
        self.edit_name_entry.insert(0, product.name)
        self.edit_category_entry = tk.Entry(self.edit_product_window)
        self.edit_category_entry.grid(row=1, column=1)
        self.edit_category_entry.insert(0, product.category)
        self.edit_price_entry = tk.Entry(self.edit_product_window)
        self.edit_price_entry.grid(row=2, column=1)
        self.edit_price_entry.insert(0, product.price)

        save_button = tk.Button(
            self.edit_product_window,
            text="Save",
            command=lambda: self.save_edited_product(product),
        )
        save_button.grid(row=3, columnspan=2, pady=10)

    def save_edited_product(self, product):
        edited_name = self.edit_name_entry.get()
        edited_category = self.edit_category_entry.get()
        edited_price = self.edit_price_entry.get()

        if not all([edited_name, edited_category, edited_price]):
            messagebox.showerror("Error", "All fields are required")
            return

        if any(
            [
                field.strip() == ""
                for field in [edited_name, edited_category, edited_price]
            ]
        ):
            messagebox.showerror("Error", "Fields cannot be blank")
            return

        if not self.product_control.edit_product(
            product.product_id, edited_name, edited_category, edited_price
        ):
            messagebox.showerror("Error", "Product not found")
            return

        messagebox.showinfo("Success", "Product edited successfully")
        self.edit_product_window.destroy()
        self.refresh_product_list()
        self.root.deiconify()

    def delete_product(self, product):
        confirmation = messagebox.askyesno(
            "Delete Product", "Are you sure you want to delete this product?"
        )
        if confirmation:
            if self.product_control.delete_product(product.product_id):
                messagebox.showinfo("Success", "Product deleted successfully")

                self.refresh_product_list()

    def logout(self):
        self.root.destroy()  # Fecha a janela de gerenciamento de produtos
        self.return_to_login()
