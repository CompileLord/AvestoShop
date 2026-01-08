

# Avest-Shop

Avest-Shop is a Django-based e-commerce platform that allows users to create their own shops, list products, and sell them. It provides a complete marketplace with features like product search, filtering, a shopping cart, and a user-friendly dashboard for shop owners.

## Features

-   **User Authentication:** Users can register, login, and manage their accounts.
-   **Shop Management:** Registered users can create and manage their own shops, including adding a title, bio, and city.
-   **Product Management:** Shop owners can add, update, and delete products, including details like title, description, price, images, and quantity.
-   **Product Catalog:** Products are organized by categories, and users can browse products by category, search, and filter by price, city, and product state (new or used).
-   **Shopping Cart:** Users can add products to their shopping cart, manage the quantity of items, and proceed to checkout.
-   **Order Management:** The system records sales, including the customer, product, quantity, and total price.
-   **Social Features:** Users can like and comment on products.
-   **Shop Dashboard:** Shop owners have a dashboard to view their latest products, recent comments on their products, sales, and likes.
-   **Image Gallery:** Multiple images can be uploaded for each product.

## Technologies Used

-   **Backend:**
    -   [Django](https://www.djangoproject.com/): A high-level Python web framework.
-   **Database:**
    -   [SQLite](https://www.sqlite.org/index.html): A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
-   **Frontend:**
    -   [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
    -   [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3)
    -   [Bootstrap](https://getbootstrap.com/): A popular CSS framework for developing responsive and mobile-first websites.
-   **Other:**
    -   [Pillow](https.pypi.org/project/Pillow/): A Python Imaging Library.
    -   [python-dotenv](https://pypi.org/project/python-dotenv/): A Python library for managing environment variables.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/avest-shop.git
    cd avest-shop
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirments.txt
    ```

4.  **Apply the migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000/`.

## Usage

1.  **Register a new account** or **login** with an existing one.
2.  To create your own shop, navigate to the "Create Shop" page and fill in the required details.
3.  Once your shop is created, you can add products to it through your shop dashboard.
4.  Browse products on the main page, filter them by category, city, price, etc.
5.  Add products to your cart and proceed to checkout to "purchase" them.
6.  Interact with products by leaving comments and likes.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.
=======
