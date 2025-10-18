import streamlit as st
from datetime import datetime
import random
from openai import OpenAI

# Page Configuration
st.set_page_config(
    page_title="3D Printing Hub - POS System",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS Styling
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Button styling */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Product image styling */
    .product-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 500;
    }
    
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-card p {
        margin: 0;
        font-size: 0.85rem;
        opacity: 0.85;
    }
    
    /* Invoice header */
    .invoice-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .invoice-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .invoice-header p {
        margin: 0.5rem 0;
        opacity: 0.95;
    }
    
    /* Section headers */
    .section-header {
        color: #4f46e5;
        border-bottom: 3px solid #4f46e5;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Info boxes */
    .info-box {
        background: #f8fafc;
        border-left: 4px solid #4f46e5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Total box */
    .total-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    .total-box h2 {
        margin: 0;
        font-size: 2rem;
    }
    
    /* Payment info */
    .payment-info {
        background: #f0f9ff;
        border: 2px solid #0ea5e9;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
    }
    
    .payment-info h4 {
        color: #0369a1;
        margin-top: 0;
    }
    
    /* Print button */
    .print-info {
        background: #fef3c7;
        border: 2px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Table styling */
    .invoice-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
        background: white;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .invoice-table th {
        background: #f8fafc;
        padding: 1rem;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid #e5e7eb;
    }
    
    .invoice-table td {
        padding: 1rem;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .invoice-table tr:last-child td {
        border-bottom: none;
    }
    
    @media print {
        .stApp > header, .stApp > footer, button, .print-info {
            display: none !important;
        }
        .invoice-header {
            background: #4f46e5 !important;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
    }
    </style>
""", unsafe_allow_html=True)

DISCOUNT_CODES = {
    "SAY-NO-TO-POLYMATE": 0.15,
    "SKEM-FILAMENT-PRICE": 0.20,
    "PARCEL-DEEZ-NUTS": 0.50
}

FILAMENTS = [
    {
        "id": "pla_white",
        "name": "PLA Filament - White",
        "material": "PLA",
        "price": 25.00,
        "color": "White",
        "stock": "In Stock",
        "rating": 4.8,
        "image": "white.png"
    },
    {
        "id": "pla_black",
        "name": "PLA Filament - Black",
        "material": "PLA",
        "price": 25.00,
        "color": "Black",
        "stock": "In Stock",
        "rating": 4.9,
        "image": "black.png"
    },
    {
        "id": "abs_red",
        "name": "ABS Filament - Red",
        "material": "ABS",
        "price": 28.00,
        "color": "Red",
        "stock": "In Stock",
        "rating": 4.7,
        "image": "red.png"
    },
    {
        "id": "petg_blue",
        "name": "PETG Filament - Blue",
        "material": "PETG",
        "price": 30.00,
        "color": "Blue",
        "stock": "In Stock",
        "rating": 4.6,
        "image": "blue.png"
    },
    {
        "id": "tpu_clear",
        "name": "TPU Flexible - Clear",
        "material": "TPU",
        "price": 35.00,
        "color": "Clear",
        "stock": "Low Stock",
        "rating": 4.5,
        "image": "transparent.png"
    },
    {
        "id": "nylon_natural",
        "name": "Nylon Filament - Natural",
        "material": "Nylon",
        "price": 40.00,
        "color": "Natural",
        "stock": "In Stock",
        "rating": 4.8,
        "image": "tpu.png"
    }
]

# Initialize session state variables
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'filament_cart' not in st.session_state:
    st.session_state.filament_cart = {}
if 'discount_code' not in st.session_state:
    st.session_state.discount_code = ""
if 'discount_amount' not in st.session_state:
    st.session_state.discount_amount = 0
if 'show_invoice' not in st.session_state:
    st.session_state.show_invoice = False
if 'invoice_data' not in st.session_state:
    st.session_state.invoice_data = None

def navigate_to(view):
    """Navigate to different pages in the app"""
    st.session_state.view = view
    st.rerun()

def apply_discount(total, code):
    """Apply discount code to total amount"""
    code = code.upper()
    if code in DISCOUNT_CODES:
        return total * DISCOUNT_CODES[code]
    return 0

def display_metric_card(title, content, description):
    """Display a custom metric card using HTML"""
    st.markdown(f"""
        <div class="metric-card">
            <h3>{title}</h3>
            <div class="metric-value">{content}</div>
            <p>{description}</p>
        </div>
    """, unsafe_allow_html=True)

def display_invoice(invoice_data):
    """Display invoice using Streamlit components with custom styling"""
    
    # Header with gradient
    st.markdown(f"""
        <div class="invoice-header">
            <h1>🖨️ 3D PRINTING HUB</h1>
            <p>Professional 3D Printing Services & Premium Filaments</p>
            <p style="font-size: 1.1rem; font-weight: 600;">Invoice #{invoice_data['invoice_number']} | {invoice_data['date']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Customer and Order Info
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<h3 class="section-header">📋 Bill To</h3>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="info-box">
                <p><strong>Name:</strong> {invoice_data['customer_name']}</p>
                <p><strong>Email:</strong> {invoice_data['customer_email']}</p>
                <p><strong>Phone:</strong> {invoice_data['customer_phone']}</p>
                <p><strong>Address:</strong> {invoice_data['customer_address'].replace('<br>', ', ')}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h3 class="section-header">📦 Order Details</h3>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="info-box">
                <p><strong>Type:</strong> {invoice_data['order_type']}</p>
                <p><strong>Date:</strong> {invoice_data['date']}</p>
                <p><strong>Terms:</strong> Due on Receipt</p>
                <p><strong>Status:</strong> <span style="color: #f59e0b; font-weight: 600;">⏳ Pending Payment</span></p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Items Table using HTML
    st.markdown('<h3 class="section-header">🛒 Items</h3>', unsafe_allow_html=True)
    
    # Build HTML table
    table_html = """
    <table class="invoice-table">
        <thead>
            <tr>
                <th>Description</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for item in invoice_data['items']:
        table_html += f"""
            <tr>
                <td>{item['description']}</td>
                <td>{item['quantity']}</td>
                <td>${item['unit_price']:.2f}</td>
                <td>${item['total']:.2f}</td>
            </tr>
        """
    
    table_html += """
        </tbody>
    </table>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Totals
    col1, col2 = st.columns([1.5, 1], gap="large")
    
    with col1:
        st.markdown("")  # Spacer
    
    with col2:
        st.markdown('<h3 class="section-header">💰 Summary</h3>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style="font-size: 1.1rem; line-height: 2;">
                <p><strong>Subtotal:</strong> <span style="float: right;">${invoice_data['subtotal']:.2f}</span></p>
        """, unsafe_allow_html=True)
        
        if invoice_data.get('shipping', 0) > 0:
            st.markdown(f'<p><strong>Shipping:</strong> <span style="float: right;">${invoice_data["shipping"]:.2f}</span></p>', unsafe_allow_html=True)
        
        if invoice_data.get('tax', 0) > 0:
            st.markdown(f'<p><strong>Tax (9%):</strong> <span style="float: right;">${invoice_data["tax"]:.2f}</span></p>', unsafe_allow_html=True)
        
        if invoice_data.get('discount', 0) > 0:
            st.markdown(f'<p style="color: #10b981;"><strong>Discount ({invoice_data["discount_code"]}):</strong> <span style="float: right;">-${invoice_data["discount"]:.2f}</span></p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="total-box">
                <h2>TOTAL: ${invoice_data['total']:.2f} SGD</h2>
            </div>
        """, unsafe_allow_html=True)
    
    # Payment Information
    st.markdown(f"""
        <div class="payment-info">
            <h4>💳 Payment Information</h4>
            <p><strong>Thank you for your business!</strong></p>
            <p>Payment Instructions: Please transfer to <strong>DBS Singapore</strong></p>
            <p>Account Number: <strong>123-456789-0</strong></p>
            <p>Reference: <strong>Invoice #{invoice_data['invoice_number']}</strong></p>
            <hr style="border-color: #0ea5e9; margin: 1rem 0;">
            <p style="font-size: 0.9rem; color: #0369a1;">
                3D Printing Hub | contact@3dprintinghub.sg | +65 9876 5432
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Print instructions
    st.markdown("""
        <div class="print-info">
            <strong>💡 Press Ctrl+P (or Cmd+P on Mac) to print this invoice</strong>
        </div>
    """, unsafe_allow_html=True)

def show_home():
    """Display home page with service options"""
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0 2rem 0;'>
            <h1 style='font-size: 3.5rem; font-weight: 700; margin-bottom: 1rem; 
                       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       background-clip: text;'>
                🖨️ 3D Printing Hub
            </h1>
            <p style='font-size: 1.25rem; color: #6b7280;'>Professional 3D printing services and premium materials</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics display
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    with col1:
        display_metric_card("Materials", "6+", "Premium filaments")
    with col2:
        display_metric_card("Accuracy", "±0.1mm", "High precision")
    with col3:
        display_metric_card("Delivery", "24-48h", "Fast turnaround")
    with col4:
        display_metric_card("Rating", "4.8/5", "500+ customers")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Service selection
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🤖 3D Printing AI Assistant")
            st.markdown("""
            ✓ Expert Guidance - Best practices & tips  
            ✓ Material Selection - Right filament for your project  
            ✓ Print Optimization - Orientation & strength  
            ✓ Troubleshooting - Help with ABS, ASA & more
            """)
            if st.button("Chat with AI", key="btn_print", use_container_width=True, type="primary"):
                navigate_to('ai_assistant')
    
    with col2:
        with st.container(border=True):
            st.markdown("### 🧵 Filament Store")
            st.markdown("""
            ✓ Wide Selection - 6+ materials and colors  
            ✓ Quality Assured - Tested filaments  
            ✓ Best Prices - Competitive pricing  
            ✓ Fast Shipping - Same-day dispatch
            """)
            if st.button("Browse Products", key="btn_filament", use_container_width=True, type="primary"):
                navigate_to('filament')

def show_ai_assistant():
    """Display AI chatbot for 3D printing guidance"""
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button("← Back"):
            navigate_to('home')
    with col2:
        st.markdown("### 🤖 3D Printing AI Assistant")
    
    st.markdown("---")
    
    # Check if API key exists
    try:
        OpenAI_Key = st.secrets["OpenAI_Key"]
    except:
        st.error("⚠️ OpenAI API Key not found in secrets. Please configure it first.")
        st.info("""
        **How to set up Streamlit secrets:**
        
        1. Create a folder called `.streamlit` in your project directory
        2. Inside that folder, create a file called `secrets.toml`
        3. Add this line to the file:
        ```
        OpenAI_Key = "your-api-key-here"
        ```
        4. Get your API key from https://platform.openai.com/api-keys
        5. Restart your Streamlit app
        """)
        return
    
    # Initialize OpenAI client
    client = OpenAI(api_key=OpenAI_Key)
    
    # System prompt with 3D printing expertise
    SYSTEM_PROMPT = """You are an expert 3D printing consultant with years of experience in additive manufacturing. Your role is to help users with:

1. **Material Selection & Properties:**
   - PLA: Best for beginners, biodegradable, low warping, good detail. Temp: 190-220°C. Use for: prototypes, decorative items, low-stress parts.
   - ABS: Strong, heat resistant, requires heated bed (80-110°C), prone to warping. Temp: 220-250°C. Use for: functional parts, mechanical components. Tips: Use enclosure, keep room temperature stable, consider ABS slurry for bed adhesion.
   - PETG: Chemical resistant, strong, flexible, minimal warping. Temp: 220-250°C. Use for: outdoor parts, mechanical parts, water bottles.
   - TPU/Flexible: Elastic, impact resistant, challenging to print. Temp: 210-230°C. Print slow (20-30mm/s), use direct drive extruder.
   - Nylon: Very strong, abrasion resistant, hygroscopic (absorbs moisture). Temp: 240-260°C. Dry filament before use.
   - ASA: Like ABS but UV resistant, better for outdoor use. Temp: 240-260°C. Similar printing challenges as ABS - needs enclosure and heated bed.

2. **Print Orientation for Maximum Strength:**
   - Layer lines are the weakest point - orient parts so stress is parallel to layers, not perpendicular
   - For mechanical parts: position so functional surfaces align with layer direction
   - Overhangs >45° need supports - minimize them by smart orientation
   - Consider anisotropic properties: parts are weakest in Z-axis (layer separation)

3. **Best Practices for Difficult Materials:**
   - **ABS/ASA:** Use fully enclosed printer, heated bed 80-110°C, avoid drafts, use ABS juice (ABS dissolved in acetone) for bed adhesion, print in well-ventilated area
   - **Nylon:** Dry filament at 70°C for 4-6 hours before printing, use glue stick or garolite bed surface, increase bed temp to 70-80°C
   - **PETG:** Clean bed thoroughly, reduce print speed, avoid bed too hot (can stick too well), use lower retraction than PLA
   - **TPU:** Print slow, reduce retraction distance, use direct drive if possible, increase flow rate slightly

4. **General Tips:**
   - First layer is critical - level bed carefully, adjust Z-offset
   - Print temperature towers to find optimal temp for each filament
   - Use cooling fan for PLA, reduce/disable for ABS/ASA
   - Infill: 10-20% for most parts, 50%+ for mechanical strength
   - Wall thickness: minimum 2-3 perimeters for strength

Always provide specific, actionable advice. Ask clarifying questions when needed. Be friendly and encouraging to beginners while giving detailed technical guidance to advanced users."""

    # Display chat messages in a container
    chat_container = st.container(border=True, height=500)
    
    with chat_container:
        if not st.session_state.chat_messages:
            st.info("👋 Hi! I'm your 3D printing assistant. Ask me anything about materials, print settings, orientation, or troubleshooting!")
        
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.markdown(f"""
                    <div style="background: #4f46e5; color: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; max-width: 80%; margin-left: auto;">
                        <strong>You:</strong><br>{message["content"]}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="background: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; max-width: 80%; border: 1px solid #e5e7eb;">
                        <strong>AI Assistant:</strong><br>{message["content"]}
                    </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Ask me anything about 3D printing...", key="chat_input", label_visibility="collapsed")
    with col2:
        send_button = st.button("Send", use_container_width=True, type="primary")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()
    
    # Handle message sending
    if send_button and user_input:
        # Add user message to chat history
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        # Prepare messages for API
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        api_messages.extend(st.session_state.chat_messages)
        
        # Call OpenAI API
        try:
            with st.spinner("AI is thinking..."):
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",  # Using gpt-4o-mini for cost efficiency
                    messages=api_messages,
                    temperature=0.7,
                    max_tokens=800
                )
                
                ai_response = completion.choices[0].message.content
                
                # Add AI response to chat history
                st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
                
                st.rerun()
        except Exception as e:
            st.error(f"Error communicating with AI: {str(e)}")
            # Remove the user message if API call failed
            st.session_state.chat_messages.pop()

def show_printing_checkout():
    """Redirect to AI assistant (deprecated)"""
    navigate_to('ai_assistant')

def show_filament_store():
    """Display filament store with products and shopping cart"""
    col1, col2, col3 = st.columns([1, 6, 3])
    with col1:
        if st.button("← Back", key="back_fil"):
            navigate_to('home')
    with col2:
        st.markdown("### 🧵 Filament Store")
    with col3:
        cart_count = sum(st.session_state.filament_cart.values())
        if cart_count > 0:
            if st.button(f"🛒 Cart ({cart_count})", use_container_width=True):
                navigate_to('filament_checkout')

    st.markdown("---")
    
    # Display products in grid
    cols_per_row = 3
    for i in range(0, len(FILAMENTS), cols_per_row):
        cols = st.columns(cols_per_row, gap="medium")
        for j, col in enumerate(cols):
            if i + j < len(FILAMENTS):
                product = FILAMENTS[i + j]
                with col, st.container(border=True):
                    # Product Image
                    try:
                        st.image(product['image'], use_container_width=True)
                    except Exception as e:
                        st.warning(f"Image not found: {product['name']}")
                    
                    st.markdown(f"**{product['name']}**")
                    st.caption(f"{product['material']} • {product['color']} • {product['stock']}")
                    st.caption(f"⭐ {product['rating']}/5")
                    
                    st.markdown(f"### ${product['price']:.2f}")

                    current_qty = st.session_state.filament_cart.get(product['id'], 0)
                    
                    if st.button("Add to Cart", key=f"add_{product['id']}", use_container_width=True, type="primary"):
                        if current_qty == 0:
                            st.session_state.filament_cart[product['id']] = 1
                        else:
                            st.session_state.filament_cart[product['id']] += 1
                        st.rerun()
                    
                    if current_qty > 0:
                        st.markdown(f"**In Cart: {current_qty}**")
                        if st.button("🗑️ Remove", key=f"remove_{product['id']}", use_container_width=True):
                            del st.session_state.filament_cart[product['id']]
                            st.rerun()
    
    cart_items = sum(st.session_state.filament_cart.values())
    if cart_items > 0:
        st.markdown("---")
        if st.button("Proceed to Checkout →", use_container_width=True, type="primary"):
            navigate_to('filament_checkout')
            
def show_filament_checkout():
    """Display checkout page for filament orders"""
    if st.session_state.show_invoice and st.session_state.invoice_data:
        # Display invoice
        if st.button("← Back to Checkout", key="back_to_checkout2"):
            st.session_state.show_invoice = False
            st.rerun()
        
        st.markdown("---")
        display_invoice(st.session_state.invoice_data)
        return
    
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button("← Back", key="back_fil_check"):
            navigate_to('filament')
    with col2:
        st.markdown("### 🛒 Filament Checkout")
    
    st.markdown("---")
    
    if not st.session_state.filament_cart:
        st.error("Your cart is empty.")
        if st.button("Browse Filaments", use_container_width=True):
            navigate_to('filament')
        return
    
    col_left, col_right = st.columns([1.5, 1], gap="large")
    
    with col_left:
        st.markdown('<h4 class="section-header">📝 Contact Information</h4>', unsafe_allow_html=True)
        customer_name = st.text_input("Name *", key="fil_name")
        customer_email = st.text_input("Email *", key="fil_email")
        customer_phone = st.text_input("Phone *", key="fil_phone")
        customer_address = st.text_area("Address *", height=100, key="fil_addr")
    
    with col_right:
        st.markdown('<h4 class="section-header">📦 Order Summary</h4>', unsafe_allow_html=True)
        
        with st.container(border=True):
            cart_items_data = []
            subtotal = 0
            
            # Calculate cart totals
            for product_id, qty in st.session_state.filament_cart.items():
                product = next(p for p in FILAMENTS if p['id'] == product_id)
                item_total = product['price'] * qty
                subtotal += item_total
                cart_items_data.append({
                    'product': product,
                    'quantity': qty,
                    'total': item_total
                })
                st.text(f"{product['name']} (x{qty}) - ${item_total:.2f}")

            # Calculate additional charges
            shipping = 0 if subtotal >= 100 else 5.00
            tax = subtotal * 0.09
            
            st.markdown("---")
            discount_code = st.text_input("Discount Code", placeholder="Optional", key="cart_discount")
            discount = apply_discount(subtotal, discount_code)
            st.session_state.discount_amount = discount
            
            total = subtotal + shipping + tax - discount
            
            st.markdown(f"""
            <div style="font-size: 1.05rem; line-height: 1.8;">
                Subtotal: <code>${subtotal:.2f}</code><br>
                Shipping: <code>{'FREE' if shipping == 0 else f'${shipping:.2f}'}</code><br>
                Tax (9%): <code>${tax:.2f}</code>
            </div>
            """, unsafe_allow_html=True)
            
            if discount > 0:
                st.success(f"✅ Discount Applied: -${discount:.2f}")
        
        st.markdown(f"""
        <div class="total-box">
            <h2>${total:.2f} SGD</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 View Invoice", type="primary", use_container_width=True, key="gen_inv"):
            if not all([customer_name, customer_email, customer_phone, customer_address]):
                st.error("⚠️ Please fill in all contact fields")
            else:
                invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
                
                items = []
                for item in cart_items_data:
                    items.append({
                        'description': item['product']['name'],
                        'quantity': item['quantity'],
                        'unit_price': item['product']['price'],
                        'total': item['total']
                    })
                
                invoice_data = {
                    'invoice_number': invoice_number,
                    'date': datetime.now().strftime('%B %d, %Y'),
                    'customer_name': customer_name,
                    'customer_email': customer_email,
                    'customer_phone': customer_phone,
                    'customer_address': customer_address.replace('\n', '<br>'),
                    'order_type': 'Filament Order',
                    'items': items,
                    'subtotal': subtotal,
                    'shipping': shipping,
                    'tax': tax,
                    'discount': discount,
                    'discount_code': discount_code.upper() if discount > 0 else '',
                    'total': total
                }
                
                st.session_state.invoice_data = invoice_data
                st.session_state.show_invoice = True
                st.rerun()

def main():
    """Main function to route between pages"""
    views = {
        'home': show_home,
        'ai_assistant': show_ai_assistant,
        'printing': show_ai_assistant,  # Redirect old route
        'printing_checkout': show_printing_checkout,  # Redirect old route
        'filament': show_filament_store,
        'filament_checkout': show_filament_checkout
    }
    
    view_func = views.get(st.session_state.view, show_home)
    view_func()

if __name__ == "__main__":
    main()
