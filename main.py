import UserRegistration
import ShoppingCart
import ProductManagement
import ProductBrowsing

while True:
  print("1. User Registration")
  print("2. Login")
  print("3. Add Product")
  print("4. Edit Product")
  print("5. Remove Product")
  print("6. View Cart")
  print("7. Search Products")
  print("8. Filter Products")
  print("9. Sort Products")
  print("0. Exit")

  choice = int(input("Enter your choice: "))

  if choice == 1:
    UserRegistration.create_account()
  elif choice == 2:
    UserRegistration.login()
  elif choice == 3:
    ProductManagement.add_product()
  elif choice == 4:
    ProductManagement.edit_product()
  elif choice == 5:
    ProductManagement.remove_product()
  elif choice == 6:
    ShoppingCart.view_cart()
  elif choice == 7:
    ProductBrowsing.search_products()
  elif choice == 8:
    ProductBrowsing.filter_products()
  elif choice == 9:
    ProductBrowsing.sort_products()
  elif choice == 0:
    break
  else:
    print("Invalid choice. Please try again.")

