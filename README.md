
-----

# 🖨️ 3D Printing Hub - A Streamlit Web App

Welcome to the **3D Printing Hub**\! This is a one-stop-shop web app for all things 3D printing. Whether you need a custom model printed or want to stock up on filament, this app has you covered. It's built entirely in Python using the magic of Streamlit.

## ✨ Features

This application is split into two main services:

### 1\. 🖨️ 3D Printing Service

  * **🚀 Instant Print Quotes:** Upload your `.stl` file, choose a material (like PLA, ABS, or PETG), and get an immediate price estimate.
  * **🧊 Interactive 3D Viewer:** See a live, rotatable preview of your uploaded model right in the browser.
  * **⚙️ Automatic Calculations:** The app automatically calculates your model's volume and weight to determine the cost.
  * **💳 Secure Stripe Checkout:** A seamless and secure payment process to get your model printed.

### 2\. 🧵 Filament Store

  * **🛒 E-Commerce Experience:** Browse a collection of premium 3D printing filaments.
  * **🔎 Filter & Sort:** Easily find what you're looking for by filtering by material or sorting by price and name.
  * **🛍️ Shopping Cart:** Add filaments to your cart, adjust quantities, and see your total update in real-time.
  * **💳 Secure Stripe Checkout:** A dedicated checkout flow for your filament order, complete with shipping and tax calculations.

-----

## 🛠️ How to Set Up and Run the Project

Getting the 3D Printing Hub running on your local machine is easy. Just follow these steps\!

### Step 1: Clone the Repository

First, get the project files onto your computer using Git.

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Step 2: Create a Virtual Environment

It's a best practice to keep project dependencies isolated. This creates a clean space for your project.

  * **On macOS/Linux:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

  * **On Windows:**

    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### Step 3: Install Dependencies

Install all the required Python packages at once using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### Step 4: Configure Your Secrets 🤫

Your app needs an API key from Stripe to handle payments. You should never save keys directly in your code. Streamlit uses a special **`.streamlit/secrets.toml`** file to keep them safe.

1.  **Create the `.streamlit` folder** from your terminal. This command works for all operating systems.

    ```bash
    mkdir .streamlit
    ```

2.  **Create the `secrets.toml` file** inside that new folder.

      * For **macOS or Linux**, use the `touch` command:
        ```bash
        touch .streamlit/secrets.toml
        ```
      * For **Windows**, use the `echo` command:
        ```bash
        echo. > .streamlit\secrets.toml
        ```

3.  **Add your keys to the file.** Open the new `secrets.toml` file in a text editor (like VS Code or Notepad) and paste the following content. **Remember to replace the placeholder with your actual Stripe secret key\!**

    ```toml
    # .streamlit/secrets.toml

    # Get your secret key from the Stripe Developer Dashboard
    stripe_secret_key = "sk_test_YOUR_SECRET_KEY_GOES_HERE"

    # The URLs Stripe will redirect to after payment
    success_url = "http://localhost:8501"
    cancel_url = "http://localhost:8501"
    ```

    > **Note:** You can find your Stripe API keys in your [Stripe Developer Dashboard](https://dashboard.stripe.com/test/apikeys). For testing, use the "secret key" that starts with `sk_test_`.

### Step 5: Run the App\! 🚀

You're all set\! Run the Streamlit app from your terminal.

```bash
streamlit run your_app_filename.py
```

Your web browser should automatically open a new tab with the 3D Printing Hub running. Enjoy\!

-----

## 💻 Technologies Used

  * **Framework:** [Streamlit](https://streamlit.io/)
  * **UI Components:** [streamlit-shadcn-ui](https://www.google.com/search?q=https://github.com/Observed-Observer/streamlit-shadcn-ui)
  * **3D Viewer:** [streamlit-stl](https://www.google.com/search?q=https://github.com/ko-build/streamlit-stl)
  * **STL File Processing:** [numpy-stl](https://github.com/WoLpH/numpy-stl)
  * **Payment Processing:** [Stripe API](https://stripe.com/)
  * **Language:** Python
