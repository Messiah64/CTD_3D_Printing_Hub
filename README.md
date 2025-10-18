# 🖨️ 3D Printing Hub POS 🤖

Welcome to the **3D Printing Hub**! This is a slick, modern Point-of-Sale (POS) system and e-commerce front-end built with the magic of Python and Streamlit. ✨

It's more than just a sales app—it's a complete toolkit for any 3D printing business, featuring a beautiful filament store and a brilliant **AI Assistant** to guide users from idea to perfect print.



---

## ⭐ Core Features

* **🛒 Gorgeous Filament Store:** A clean, grid-based product catalog with a seamless add-to-cart experience.
* **🧠 AI 3D Printing Assistant:** Powered by GPT-4o mini, this expert AI helps with material selection, print settings, and troubleshooting.
* **🧾 Slick Checkout & Invoicing:** Automatically handles taxes, shipping, and fun discount codes, then generates a beautiful, printable invoice.
* **🎨 Stunning Custom UI:** With custom CSS, the app feels premium, featuring gradient buttons, sleek metric cards, and a fully responsive layout.
* **🚀 Built with Streamlit:** The entire app is a single, fast Python script. It's incredibly easy to run and modify.

---

## 🛠️ Tech Stack

* **Language:** Python 🐍
* **Framework:** Streamlit 🎈
* **AI:** OpenAI API (GPT-4o mini) 🤖
* **Styling:** Custom CSS 💅

---

## 🚀 Get Running in Under 3 Minutes!

1.  **Clone the Repo**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Install Dependencies**
    ```bash
    pip install streamlit openai
    ```

3.  **Add Your API Key**
    Create a file at `.streamlit/secrets.toml` and add your OpenAI key:
    ```toml
    OpenAI_Key = "your-secret-api-key-here"
    ```

4.  **Launch!** 🎉
    Make sure your product images are in the root folder, then run:
    ```bash
    streamlit run your_script_name.py
    ```

---

## 💡 How It Works

The app's logic is beautifully simple:

* **`st.session_state`:** Acts as the app's "memory," tracking the current page, shopping cart, and AI chat history.
* **Function-Based Routing:** A simple `main()` function calls different page-drawing functions (`show_home()`, `show_filament_store()`) to navigate the app. No complex frameworks needed!

---

## 🤝 Contribute

Have an idea or found a bug? Fork the repo, make your changes, and submit a pull request. Let's build the coolest 3D printing software together!
