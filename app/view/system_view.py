import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from control.user_control import UserControl
from control.admin_user_control import AdminUserControl
from control.product_control import ProductControl


class AuthenticationView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x300")

        self.user_control = UserControl()

        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Username").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        tk.Label(self.login_frame, text="Password").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(
            self.login_frame, text="Login", command=self.login
        )
        self.login_button.pack()

        self.admin_login_button = tk.Button(
            self.login_frame, text="Admin Login", command=self.admin_login
        )
        self.admin_login_button.pack()

        self.register_button = tk.Button(
            self.login_frame, text="Register", command=self.show_register
        )
        self.register_button.pack()

        self.register_frame = tk.Frame(self.root)

        tk.Label(self.register_frame, text="Full Name").pack()
        self.name_entry = tk.Entry(self.register_frame)
        self.name_entry.pack()

        tk.Label(self.register_frame, text="E-mail").pack()
        self.email_entry = tk.Entry(self.register_frame)
        self.email_entry.pack()

        tk.Label(self.register_frame, text="Address").pack()
        self.address_entry = tk.Entry(self.register_frame)
        self.address_entry.pack()

        tk.Label(self.register_frame, text="Username").pack()
        self.new_username_entry = tk.Entry(self.register_frame)
        self.new_username_entry.pack()

        tk.Label(self.register_frame, text="Password").pack()
        self.new_password_entry = tk.Entry(self.register_frame, show="*")
        self.new_password_entry.pack()

        self.finish_button = tk.Button(
            self.register_frame, text="Create Account", command=self.register_user
        )
        self.finish_button.pack()

        self.register_frame.pack_forget()
        self.admin_control = AdminUserControl()

        self.back_to_login_button = tk.Button(
            self.register_frame, text="Back to Login", command=self.show_login
        )
        self.back_to_login_button.pack()

    def show_login(self):
        self.register_frame.pack_forget()
        self.login_frame.pack()

    def admin_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.admin_control.authenticate_admin(username, password):
            messagebox.showinfo("Success", "Admin Login successful!")
            self.root.withdraw()

            def return_to_login():
                self.root.deiconify()
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)

            root_manage_products = tk.Tk()
            AdminManageProductView(root_manage_products, return_to_login)
            root_manage_products.mainloop()
        else:
            messagebox.showerror("Error", "Invalid admin credentials!")

    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_control.authenticate(username, password):
            messagebox.showinfo("Success", "User Login successful!")
            self.root.withdraw()

            def return_to_login():
                self.root.deiconify()
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)

            user_control = UserControl()
            root_browsing = tk.Tk()
            ProductBrowsingView(root_browsing, username, return_to_login, user_control)
            root_browsing.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def register_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if not all([name, email, address, username, password]):
            messagebox.showerror("Error", "All fields are required")
            return

        if any(
            [
                field.strip() == ""
                for field in [name, email, address, username, password]
            ]
        ):
            messagebox.showerror("Error", "Fields cannot be blank")
            return

        self.user_control.create_user(name, email, address, username, password)
        messagebox.showinfo("Success", "Account registered successfully")
        self.register_frame.pack_forget()
        self.login_frame.pack()

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

        self.products_frame = tk.Frame(self.root)
        self.products_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.products_frame)
        self.scrollbar = tk.Scrollbar(
            self.products_frame, orient=tk.VERTICAL, command=self.canvas.yview, width=25
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
        logout_button.pack(side=tk.BOTTOM, padx=20, pady=10)

    def show_products(self):
        self.product_control.load_products()

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
        tk.Label(
            self.new_product_window,
            text="Category (Notebook, Headset, Keyboard, Mouse)",
        ).grid(row=2, column=0)
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
        self.new_product_window.destroy()
        self.refresh_product_list()

    def refresh_product_list(self):
        for widget in self.product_list_frame.winfo_children():
            widget.destroy()

        # Exibe novamente os produtos atualizados
        self.show_products()

    def edit_product(self, product):
        self.edit_product_window = tk.Toplevel(self.root)
        self.edit_product_window.title("Edit Product")

        tk.Label(self.edit_product_window, text="Name").grid(row=0, column=0)
        tk.Label(
            self.edit_product_window,
            text="Category (Notebook, Headset, Keyboard, Mouse)",
        ).grid(row=1, column=0)
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
        self.root.destroy()
        self.return_to_login()


class ProductBrowsingView:
    def __init__(self, root, logged_user, return_to_login, user_control):
        self.root = root
        self.return_to_login = return_to_login
        self.filtered_products = None
        self.user_control = user_control
        self.root.title("Product Browsing")
        self.root.geometry("800x600")
        self.product_control = ProductControl(products=[])
        self.product_control.load_products()

        self.logged_user = self.user_control.get_user_info(logged_user)
        if not self.logged_user:
            messagebox.showerror("Error", "User not found!")

        self.product_listbox = tk.Listbox(self.root)
        self.product_listbox.place(x=10, y=100, width=780, height=450)
        self.show_products()

        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.place(x=10, y=10)

        self.edit_profile_button = tk.Button(
            self.root, text="Edit Profile", command=self.edit_profile
        )
        self.edit_profile_button.place(x=10, y=40)

        self.search_entry = tk.Entry(self.root)
        self.search_entry.place(x=100, y=55)
        self.search_button = tk.Button(
            self.root, text="Search", command=self.search_and_display
        )
        self.search_button.place(x=220, y=50)

        self.sort_direction = tk.BooleanVar()
        self.sort_direction.set(False)

        self.sort_options = tk.StringVar()
        self.sort_menu_label = tk.Label(self.root, text="Sort by:")
        self.sort_menu_label.place(x=280, y=30)
        self.sort_menu = tk.OptionMenu(
            self.root,
            self.sort_options,
            "Name",
            "Price",
            command=self.sort_products,
        )
        self.sort_menu.place(x=280, y=50)
        self.sort_menu.config(width=8)

        self.category_var = tk.StringVar()
        self.cateogry_menu = tk.Label(self.root, text="Select Category:")
        self.cateogry_menu.place(x=380, y=30)
        self.category_menu = tk.OptionMenu(
            self.root,
            self.category_var,
            "Notebook",
            "Mouse",
            "Headset",
            "Keyboard",
            command=self.filter_by_category,
        )
        self.category_menu.place(x=380, y=50)
        self.category_menu.config(width=12)

        self.min_price_entry = tk.Entry(self.root, width=8)
        self.min_price_tittle = tk.Label(self.root, text="Min Price:")
        self.min_price_tittle.place(x=508, y=30)
        self.min_price_entry.place(x=510, y=55)
        self.max_price_entry = tk.Entry(self.root, width=8)
        self.max_price_tittle = tk.Label(self.root, text="Max Price:")
        self.max_price_tittle.place(x=578, y=30)
        self.max_price_entry.place(x=580, y=55)
        self.filter_price_button = tk.Button(
            self.root, text="Filter by Price", command=self.filter_by_price
        )
        self.filter_price_button.place(x=650, y=50)

        self.clear_button = tk.Button(
            self.root, text="Clear", command=self.clear_filters
        )
        self.clear_button.place(x=750, y=50)

        self.cart_button = tk.Button(self.root, text="Cart", command=self.view_cart)
        self.cart_button.place(x=750, y=10)

    def sort_products(self, key):
        reverse_order = self.sort_direction.get()

        all_products = self.product_control.list_all_products()

        if self.filtered_products is None:
            sorted_products = sorted(
                all_products, key=lambda product: getattr(product, key.lower(), "")
            )
        else:
            sorted_products = sorted(
                self.filtered_products,
                key=lambda product: getattr(product, key.lower(), ""),
            )

        if key == "Price":
            sorted_products = sorted(
                sorted_products,
                key=lambda product: float(getattr(product, key.lower(), float("inf"))),
            )

        if reverse_order:
            sorted_products.reverse()

        self.display_products(sorted_products)
        self.sort_direction.set(not reverse_order)

    def display_all_products(self):
        self.filtered_products = None
        self.sort_products("Name")

    def search_and_display(self):
        search_term = self.search_entry.get()
        searched_products = self.product_control.search_product_by_name(search_term)
        self.filtered_products = searched_products if search_term else None
        self.sort_products(self.sort_options.get())

    def apply_filters(self):
        category = self.category_var.get()
        min_price = self.min_price_entry.get()
        max_price = self.max_price_entry.get()

        if category == "Select Category" and not min_price and not max_price:
            self.display_all_products()  # Se nenhum filtro aplicado, exibir todos os produtos
        else:
            # Aplicar filtro por categoria
            if category != "Select Category":
                self.filtered_products = self.product_control.filter_by_category(
                    category
                )

            # Aplicar filtro por preço
            if min_price or max_price:
                filtered_by_price = self.filter_by_price_range(min_price, max_price)
                if self.filtered_products:
                    self.filtered_products = [
                        product
                        for product in filtered_by_price
                        if product in self.filtered_products
                    ]
                else:
                    self.filtered_products = filtered_by_price

            self.sort_products(self.sort_options.get())

    def reset_filters(self):
        self.search_entry.delete(0, tk.END)
        self.category_var.set("Select Category")
        self.min_price_entry.delete(0, tk.END)
        self.max_price_entry.delete(0, tk.END)
        self.display_all_products()

    def filter_by_category(self, *args):
        category = self.category_var.get()
        if category == "Select Category":
            self.filtered_products = None  # Resetar filtro de categoria
        else:
            filtered_by_category = self.product_control.filter_by_category(category)
            if self.filtered_products:
                self.filtered_products = [
                    product
                    for product in filtered_by_category
                    if product in self.filtered_products
                ]
            else:
                self.filtered_products = filtered_by_category

        self.sort_products(self.sort_options.get())

    def filter_by_price(self):
        min_price = self.min_price_entry.get()
        max_price = self.max_price_entry.get()

        if min_price or max_price:
            filtered_products = self.filter_by_price_range(min_price, max_price)
            if self.filtered_products:
                self.filtered_products = [
                    product
                    for product in filtered_products
                    if product in self.filtered_products
                ]
            else:
                self.filtered_products = filtered_products
        else:
            self.apply_filters()  # Se nenhum preço especificado, aplicar outros filtros

        self.sort_products(self.sort_options.get())

    def filter_by_price_range(self, min_price, max_price):
        try:
            min_val = float(min_price) if min_price else float("-inf")
            max_val = float(max_price) if max_price else float("inf")
        except ValueError:
            return self.product_control.list_all_products()

        filtered_products = [
            product
            for product in self.product_control.list_all_products()
            if self.is_within_price_range(product, min_val, max_val)
        ]
        return filtered_products

    def is_within_price_range(self, product, min_val, max_val):
        try:
            product_price = float(product.price)
            return min_val <= product_price <= max_val
        except ValueError:
            return False

    def display_products(self, products):
        if products is None or not products:
            return

        self.product_listbox.delete(0, tk.END)
        for product in products:
            self.product_listbox.insert(
                tk.END,
                f"{product.name} - Price: ${product.price}",
            )

    def show_products(self):
        products = self.product_control.list_all_products()
        self.display_products(products)
        self.product_listbox.bind("<Double-Button-1>", self.on_product_selected)

    def clear_filters(self):
        self.search_entry.delete(0, tk.END)
        self.category_var.set("Select Category")
        self.min_price_entry.delete(0, tk.END)
        self.max_price_entry.delete(0, tk.END)
        self.filtered_products = None
        self.show_products()

    def logout(self):
        self.root.destroy()
        self.return_to_login()

    def edit_profile(self):
        if self.logged_user:
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Profile")
            edit_window.geometry("300x400")

            tk.Label(edit_window, text="Name:").pack()
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, self.logged_user.name)
            name_entry.pack()

            tk.Label(edit_window, text="Email:").pack()
            email_entry = tk.Entry(edit_window)
            email_entry.insert(0, self.logged_user.email)
            email_entry.pack()

            tk.Label(edit_window, text="Address:").pack()
            address_entry = tk.Entry(edit_window)
            address_entry.insert(0, self.logged_user.address)
            address_entry.pack()

            tk.Label(edit_window, text="Username:").pack()
            username_entry = tk.Entry(edit_window)
            username_entry.insert(0, self.logged_user.username)
            username_entry.pack()

            tk.Label(edit_window, text="Password:").pack()
            password_entry = tk.Entry(edit_window)
            password_entry.insert(0, self.logged_user.password)
            password_entry.pack()

            update_button = tk.Button(
                edit_window,
                text="Update",
                command=lambda: self.update_profile(
                    edit_window,
                    name_entry.get(),
                    email_entry.get(),
                    address_entry.get(),
                    username_entry.get(),
                    password_entry.get(),
                ),
            )
            update_button.pack()
        else:
            messagebox.showerror("Error", "User not found!")

    def update_profile(
        self,
        user,
        edit_window,
        new_name,
        new_email,
        new_address,
        new_username,
        new_password,
    ):
        updated = self.user_control.edit_user(
            user.username,
            {
                "name": new_name,
                "email": new_email,
                "address": new_address,
                "username": new_username,
                "password": new_password,
            },
        )
        if updated:
            messagebox.showinfo("Success", "Profile updated successfully!")
            edit_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to update profile!")

    def on_product_selected(self, event):
        selected_index = self.product_listbox.curselection()
        if selected_index:
            if self.filtered_products is None or len(self.filtered_products) == 0:
                selected_product = self.product_control.list_all_products()[
                    selected_index[0]
                ]
                self.open_product_details(selected_product)
            else:
                selected_product = self.filtered_products[selected_index[0]]
                self.open_product_details(selected_product)

    def open_product_details(self, product):
        details_window = tk.Toplevel(self.root)
        details_window.title("Product Details")
        details_window.geometry("400x300")

        if self.logged_user:
            tk.Label(details_window, text=f"Name: {product.name}").pack()
            tk.Label(details_window, text=f"Category: {product.category}").pack()
            tk.Label(details_window, text=f"Price: ${product.price}").pack()

            tk.Label(details_window, text=f"Rating: {product.rating}").pack()
            tk.Label(details_window, text=f"Review: {product.review}").pack()

            add_to_cart_button = tk.Button(
                details_window,
                text="Add to Cart",
                command=lambda: self.add_to_cart(product),
            )
            add_to_cart_button.place(x=300, y=10)
        else:
            messagebox.showerror("Error", "User not found!")

    def add_to_cart(self, product):
        if product in self.logged_user.cart:
            self.logged_user.cart[product] += 1
        else:
            self.logged_user.cart[product] = 1
        messagebox.showinfo("Success", "Product added to cart!")

    def view_cart(self):
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Shopping Cart")
        cart_window.geometry("600x400")

        tk.Label(cart_window, text="Shopping Cart", font=("Arial", 16)).pack()

        cart_listbox = tk.Listbox(cart_window)
        cart_listbox.pack(fill=tk.BOTH, expand=True)

        for product, quantity in self.logged_user.cart.items():
            total_price = float(product.price) * quantity
            cart_listbox.insert(
                tk.END,
                f"{product.name} - Quantity: {quantity} - Total Price: ${total_price:.2f}",
            )

        modify_quantity_button = tk.Button(
            cart_window,
            text="Modify Quantity",
            command=lambda: self.modify_quantity(cart_listbox),
        )
        modify_quantity_button.pack()

        remove_product_button = tk.Button(
            cart_window,
            text="Remove Product",
            command=lambda: self.remove_product(cart_listbox),
        )
        remove_product_button.pack()

        buy_button = tk.Button(
            cart_window,
            text="Buy",
            command=self.buy_products,
        )
        buy_button.pack()

    def modify_quantity(self, cart_listbox):
        selected_index = cart_listbox.curselection()
        if selected_index:
            selected_product = list(self.logged_user.cart.keys())[selected_index[0]]
            new_quantity = simpledialog.askinteger(
                "Modify Quantity", f"Enter new quantity for {selected_product.name}:"
            )
            if new_quantity is not None and new_quantity > 0:
                self.logged_user.cart[selected_product] = new_quantity
                self.update_cart_list(cart_listbox)

    def remove_product(self, cart_listbox):
        selected_index = cart_listbox.curselection()
        if selected_index:
            selected_product = list(self.logged_user.cart.keys())[selected_index[0]]
            del self.logged_user.cart[selected_product]
            self.update_cart_list(cart_listbox)

    def update_cart_list(self, cart_listbox):
        cart_listbox.delete(0, tk.END)
        for product, quantity in self.logged_user.cart.items():
            total_price = float(product.price) * quantity
            cart_listbox.insert(
                tk.END,
                f"{product.name} - Quantity: {quantity} - Total Price: ${total_price:.2f}",
            )
        if len(self.logged_user.cart) == 0:
            cart_listbox.destroy()

    def buy_products(self):
        # Logic to proceed with the purchase goes here
        pass
