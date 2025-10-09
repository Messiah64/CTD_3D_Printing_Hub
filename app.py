import streamlit as st
import streamlit_shadcn_ui as ui
from streamlit_stl import stl_from_file
from stl import mesh
import numpy as np
import tempfile
import os
import stripe

# ====================================
# PAGE CONFIG
# ====================================
st.set_page_config(
    page_title="3D Printing Hub",
    page_icon="🖨️",
    layout="wide"
)

# ====================================
# SESSION STATE INITIALIZATION
# ====================================
if 'view' not in st.session_state:
    st.session_state.view = 'home'
if 'print_volume' not in st.session_state:
    st.session_state.print_volume = 0
if 'print_weight' not in st.session_state:
    st.session_state.print_weight = 0
if 'print_cost' not in st.session_state:
    st.session_state.print_cost = 0
if 'print_material' not in st.session_state:
    st.session_state.print_material = "PLA"
if 'stl_file_path' not in st.session_state:
    st.session_state.stl_file_path = None
if 'filament_cart' not in st.session_state:
    st.session_state.filament_cart = {}

# ====================================
# STRIPE CONFIGURATION
# ====================================
STRIPE_SECRET_KEY = st.secrets.get("stripe_secret_key", "")
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

# ====================================
# MATERIAL DATA
# ====================================
MATERIAL_DENSITY = {
    "PLA": 1.24,
    "ABS": 1.04,
    "PETG": 1.27,
    "Resin": 1.10,
    "Nylon": 1.14
}

MATERIAL_COST = {
    "PLA": 0.05,
    "ABS": 0.04,
    "PETG": 0.06,
    "Resin": 0.12,
    "Nylon": 0.08
}

# ====================================
# FILAMENT PRODUCTS DATA
# ====================================
FILAMENT_PRODUCTS = [
    {
        'id': 'pla_white',
        'name': 'PLA Filament - White',
        'material': 'PLA',
        'price': 25.00,
        'color': 'White',
        'weight': '1kg',
        'image': 'https://via.placeholder.com/300x200/FFFFFF/000000?text=PLA+White',
        'use_cases': 'Perfect for prototypes, models, and decorative items.',
        'features': ['Easy to print', 'Low warping', 'Biodegradable']
    },
    {
        'id': 'pla_black',
        'name': 'PLA Filament - Black',
        'material': 'PLA',
        'price': 25.00,
        'color': 'Black',
        'weight': '1kg',
        'image': 'https://via.placeholder.com/300x200/000000/FFFFFF?text=PLA+Black',
        'use_cases': 'Ideal for professional-looking models and parts.',
        'features': ['Sleek finish', 'Easy to print', 'Versatile']
    },
    {
        'id': 'abs_red',
        'name': 'ABS Filament - Red',
        'material': 'ABS',
        'price': 28.00,
        'color': 'Red',
        'weight': '1kg',
        'image': 'https://via.placeholder.com/300x200/FF0000/FFFFFF?text=ABS+Red',
        'use_cases': 'Great for functional parts with heat resistance.',
        'features': ['High strength', 'Heat resistant', 'Impact resistant']
    },
    {
        'id': 'petg_blue',
        'name': 'PETG Filament - Blue',
        'material': 'PETG',
        'price': 30.00,
        'color': 'Blue',
        'weight': '1kg',
        'image': 'https://via.placeholder.com/300x200/0000FF/FFFFFF?text=PETG+Blue',
        'use_cases': 'Perfect for outdoor parts and containers.',
        'features': ['UV resistant', 'Waterproof', 'Strong']
    },
    {
        'id': 'tpu_clear',
        'name': 'TPU Flexible - Clear',
        'material': 'TPU',
        'price': 35.00,
        'color': 'Clear',
        'weight': '1kg',
        'image': 'https://via.placeholder.com/300x200/E0E0E0/000000?text=TPU+Clear',
        'use_cases': 'Ideal for flexible parts and phone cases.',
        'features': ['Flexible', 'Elastic', 'Shock absorbing']
    },
    {
        'id': 'nylon_natural',
        'name': 'Nylon Filament - Natural',
        'material': 'Nylon',
        'price': 40.00,
        'color': 'Natural',
        'weight': '1kg',
        'image': 'https://via.placeholder.com/300x200/F5F5DC/000000?text=Nylon+Natural',
        'use_cases': 'Best for high-strength mechanical parts.',
        'features': ['High strength', 'Low friction', 'Wear resistant']
    }
]

# ====================================
# HELPER FUNCTIONS
# ====================================
def navigate_to(view):
    st.session_state.view = view
    st.rerun()

# ====================================
# HOME VIEW
# ====================================
def show_home():
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🖨️ 3D Printing Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;'>Your one-stop solution for 3D printing services and materials</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with ui.element("div", className="p-6 border rounded-lg shadow-sm", key="card_printing"):
            st.markdown("### 🖨️ 3D Printing Service")
            st.markdown("---")
            st.markdown("""
            **Upload your 3D model and get it printed!**
            
            ✓ Fast turnaround time
            
            ✓ Multiple material options
            
            ✓ Instant price calculation
            
            ✓ High-quality prints
            """)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Start Printing →", key="btn_to_printing", use_container_width=True, type="primary"):
                navigate_to('printing')
    
    with col2:
        with ui.element("div", className="p-6 border rounded-lg shadow-sm", key="card_filament"):
            st.markdown("### 🧵 Get Filament")
            st.markdown("---")
            st.markdown("""
            **Browse our premium filament collection**
            
            ✓ PLA, ABS, PETG & more
            
            ✓ Various colors available
            
            ✓ Competitive pricing
            
            ✓ Fast shipping
            """)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Browse Filaments →", key="btn_to_filament", use_container_width=True, type="primary"):
                navigate_to('filament')

# ====================================
# 3D PRINTING SERVICE VIEW
# ====================================
def show_printing_service():
    # Navigation
    col_nav1, col_nav2 = st.columns([1, 5])
    with col_nav1:
        if st.button("← Home", key="back_from_printing"):
            navigate_to('home')
    
    st.title("🖨️ 3D Printing Service")
    ui.badges(badge_list=[("STL Upload", "default"), ("Price Calculator", "secondary")], class_name="flex gap-2", key="printing_badges")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main content
    col_left, col_right = st.columns([1.2, 1], gap="large")
    
    with col_left:
        st.subheader("📁 Upload Your Model")
        
        uploaded_file = st.file_uploader(
            "Choose an STL file",
            type="stl",
            help="Upload your 3D model in STL format"
        )
        
        material = st.selectbox(
            "Select Material",
            list(MATERIAL_COST.keys()),
            help="Choose the material for your print"
        )
        
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
                st.session_state.stl_file_path = tmp_file_path
            
            try:
                # Load and calculate volume
                your_mesh = mesh.Mesh.from_file(tmp_file_path)
                vectors = your_mesh.vectors
                
                volume_mm3 = np.abs(np.sum(np.einsum('...i,...i->...', vectors[:, 0], np.cross(vectors[:, 1], vectors[:, 2])))) / 6
                volume_cm3 = volume_mm3 / 1000.0
                
                density_g_per_cm3 = MATERIAL_DENSITY[material]
                cost_per_gram = MATERIAL_COST[material]
                weight_g = volume_cm3 * density_g_per_cm3
                cost_sgd = weight_g * cost_per_gram
                
                st.session_state.print_volume = volume_cm3
                st.session_state.print_weight = weight_g
                st.session_state.print_cost = cost_sgd
                st.session_state.print_material = material
                
                st.success("✅ Model uploaded successfully!")
                
                st.markdown("---")
                st.subheader("🧊 3D Model Preview")
                stl_from_file(
                    file_path=tmp_file_path,
                    color='#FF6B6B',
                    material='material',
                    auto_rotate=True,
                    height=400,
                    key="stl_viewer"
                )
                
            except Exception as e:
                st.error(f"Error processing STL file: {e}")
    
    with col_right:
        st.subheader("💰 Price Estimation")
        
        if uploaded_file:
            # Metrics using shadcn-ui cards
            cols_metrics = st.columns(2)
            with cols_metrics[0]:
                ui.card(
                    title="Volume",
                    content=f"{st.session_state.print_volume:.2f} cm³",
                    key="volume_card"
                ).render()
            with cols_metrics[1]:
                ui.card(
                    title="Weight",
                    content=f"{st.session_state.print_weight:.2f} g",
                    key="weight_card"
                ).render()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Material info
            st.markdown(f"**Material:** {st.session_state.print_material}")
            st.markdown(f"**Unit Cost:** ${MATERIAL_COST[st.session_state.print_material]:.3f}/g")
            
            st.markdown("---")
            
            # Total cost
            st.markdown("### Total Cost")
            st.markdown(f"<h2 style='color: #FF6B6B;'>${st.session_state.print_cost:.2f} SGD</h2>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Continue to Checkout →", key="btn_to_printing_checkout", type="primary", use_container_width=True):
                navigate_to('printing_checkout')
        else:
            st.info("📤 Upload an STL file to see pricing")
            st.markdown("""
            **Pricing is based on:**
            - Model volume (cm³)
            - Material density
            - Material cost per gram
            
            Upload your file to get an instant quote!
            """)

# ====================================
# PRINTING CHECKOUT VIEW
# ====================================
def show_printing_checkout():
    # Navigation
    col_nav1, col_nav2 = st.columns([1, 5])
    with col_nav1:
        if st.button("← Back", key="back_from_printing_checkout"):
            navigate_to('printing')
    
    st.title("💳 Checkout - 3D Printing")
    ui.badges(badge_list=[("Secure Payment", "default")], class_name="flex gap-2", key="checkout_badges")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.print_cost == 0:
        st.error("⚠️ No order found. Please upload a model first.")
        return
    
    # Order Summary
    st.subheader("📋 Order Summary")
    
    cols_summary = st.columns(2)
    with cols_summary[0]:
        st.markdown("**3D Print Service**")
        st.markdown(f"Material: {st.session_state.print_material}")
        st.markdown(f"Volume: {st.session_state.print_volume:.2f} cm³")
        st.markdown(f"Weight: {st.session_state.print_weight:.2f} g")
    with cols_summary[1]:
        st.markdown(f"<h3 style='color: #FF6B6B;'>${st.session_state.print_cost:.2f}</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Customer Information
    st.subheader("📧 Contact Information")
    col1, col2 = st.columns(2)
    with col1:
        customer_email = st.text_input("Email Address", placeholder="your@email.com", key="print_email")
    with col2:
        customer_name = st.text_input("Full Name", placeholder="John Doe", key="print_name")
    
    st.markdown("---")
    
    # Payment Section
    st.subheader("💰 Payment")
    st.markdown(f"### Total: ${st.session_state.print_cost:.2f} SGD")
    
    if st.button("🔒 Proceed to Secure Payment", type="primary", use_container_width=True, key="btn_pay_printing"):
        if not customer_email or not customer_name:
            st.error("Please fill in all contact information")
        elif not STRIPE_SECRET_KEY:
            st.error("Stripe is not configured. Please add your API key to .streamlit/secrets.toml")
        else:
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'sgd',
                            'product_data': {
                                'name': '3D Printing Service',
                                'description': f'{st.session_state.print_material} - {st.session_state.print_volume:.2f} cm³',
                            },
                            'unit_amount': int(st.session_state.print_cost * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    customer_email=customer_email,
                    success_url=st.secrets.get("success_url", "http://localhost:8501"),
                    cancel_url=st.secrets.get("cancel_url", "http://localhost:8501"),
                    metadata={
                        'customer_name': customer_name,
                        'material': st.session_state.print_material,
                        'volume': str(st.session_state.print_volume),
                    }
                )
                
                st.success("✅ Payment session created!")
                st.markdown(f"**[Click here to complete payment]({session.url})**")
                
            except stripe.error.StripeError as e:
                st.error(f"Payment error: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# ====================================
# FILAMENT STORE VIEW
# ====================================
def show_filament_store():
    # Navigation
    col_nav1, col_nav2 = st.columns([1, 5])
    with col_nav1:
        if st.button("← Home", key="back_from_filament"):
            navigate_to('home')
    
    st.title("🧵 Filament Store")
    ui.badges(badge_list=[("Premium Quality", "default"), (f"Cart: {sum(st.session_state.filament_cart.values())} items", "secondary")], class_name="flex gap-2", key="filament_badges")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filters
    col_filter1, col_filter2 = st.columns([2, 2])
    with col_filter1:
        material_filter = st.selectbox(
            "Filter by Material",
            ["All"] + list(set([p['material'] for p in FILAMENT_PRODUCTS]))
        )
    with col_filter2:
        sort_by = st.selectbox(
            "Sort by",
            ["Price: Low to High", "Price: High to Low", "Material", "Name"]
        )
    
    # Apply filters
    filtered_products = FILAMENT_PRODUCTS.copy()
    if material_filter != "All":
        filtered_products = [p for p in filtered_products if p['material'] == material_filter]
    
    # Apply sorting
    if sort_by == "Price: Low to High":
        filtered_products.sort(key=lambda x: x['price'])
    elif sort_by == "Price: High to Low":
        filtered_products.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == "Material":
        filtered_products.sort(key=lambda x: x['material'])
    elif sort_by == "Name":
        filtered_products.sort(key=lambda x: x['name'])
    
    st.markdown("---")
    st.subheader(f"Available Products ({len(filtered_products)})")
    
    # Display products in grid
    cols_per_row = 3
    for i in range(0, len(filtered_products), cols_per_row):
        cols = st.columns(cols_per_row, gap="large")
        
        for j, col in enumerate(cols):
            if i + j < len(filtered_products):
                product = filtered_products[i + j]
                
                with col:
                    # Product card
                    st.image(product['image'], use_container_width=True)
                    st.markdown(f"### {product['name']}")
                    
                    ui.badges(
                        badge_list=[(product['material'], "default"), (product['color'], "secondary")],
                        class_name="flex gap-2",
                        key=f"badge_{product['id']}"
                    )
                    
                    st.markdown(f"**Weight:** {product['weight']}")
                    st.markdown(f"**Use Cases:** {product['use_cases']}")
                    
                    with st.expander("Features"):
                        for feature in product['features']:
                            st.markdown(f"✓ {feature}")
                    
                    st.markdown("---")
                    
                    col_price, col_qty = st.columns([2, 1])
                    with col_price:
                        st.markdown(f"<h3 style='color: #FF6B6B;'>${product['price']:.2f}</h3>", unsafe_allow_html=True)
                    with col_qty:
                        qty = st.number_input(
                            "Qty",
                            min_value=0,
                            max_value=10,
                            value=st.session_state.filament_cart.get(product['id'], 0),
                            key=f"qty_{product['id']}"
                        )
                    
                    if qty > 0:
                        st.session_state.filament_cart[product['id']] = qty
                    elif product['id'] in st.session_state.filament_cart:
                        del st.session_state.filament_cart[product['id']]
    
    # Cart Summary
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.filament_cart:
        st.subheader("🛒 Your Cart")
        
        total_items = sum(st.session_state.filament_cart.values())
        total_cost = sum(
            st.session_state.filament_cart[pid] * next(p['price'] for p in FILAMENT_PRODUCTS if p['id'] == pid)
            for pid in st.session_state.filament_cart
        )
        
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        with col1:
            st.markdown(f"**Total Items:** {total_items}")
        with col2:
            st.markdown(f"**Total Cost:** ${total_cost:.2f} SGD")
        with col3:
            if st.button("Checkout →", type="primary", use_container_width=True, key="btn_to_filament_checkout"):
                navigate_to('filament_checkout')
        with col4:
            if st.button("Clear", use_container_width=True, key="btn_clear_cart"):
                st.session_state.filament_cart = {}
                st.rerun()
        
        with st.expander("View Cart Details"):
            for product_id, qty in st.session_state.filament_cart.items():
                product = next(p for p in FILAMENT_PRODUCTS if p['id'] == product_id)
                st.markdown(f"- **{product['name']}** x{qty} = ${product['price'] * qty:.2f}")
    else:
        st.info("🛒 Your cart is empty. Add some filaments to get started!")

# ====================================
# FILAMENT CHECKOUT VIEW
# ====================================
def show_filament_checkout():
    # Navigation
    col_nav1, col_nav2 = st.columns([1, 5])
    with col_nav1:
        if st.button("← Back", key="back_from_filament_checkout"):
            navigate_to('filament')
    
    st.title("💳 Checkout - Filament Order")
    ui.badges(badge_list=[("Secure Payment", "default")], class_name="flex gap-2", key="filament_checkout_badges")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not st.session_state.filament_cart:
        st.error("⚠️ Your cart is empty.")
        return
    
    # Calculate totals
    cart_items = []
    subtotal = 0
    
    for product_id, qty in st.session_state.filament_cart.items():
        product = next((p for p in FILAMENT_PRODUCTS if p['id'] == product_id), None)
        if product:
            item_total = product['price'] * qty
            subtotal += item_total
            cart_items.append({'product': product, 'quantity': qty, 'total': item_total})
    
    SHIPPING_RATE = 5.00 if subtotal < 100 else 0
    tax = subtotal * 0.09
    total = subtotal + SHIPPING_RATE + tax
    
    # Order Summary
    st.subheader("📋 Order Summary")
    
    for item in cart_items:
        cols = st.columns([3, 1, 1])
        with cols[0]:
            st.markdown(f"**{item['product']['name']}**")
            st.caption(f"{item['product']['material']} • {item['product']['color']}")
        with cols[1]:
            st.markdown(f"x{item['quantity']}")
        with cols[2]:
            st.markdown(f"${item['total']:.2f}")
    
    st.markdown("---")
    
    cols_total = st.columns([3, 1])
    with cols_total[0]:
        st.markdown("**Subtotal**")
    with cols_total[1]:
        st.markdown(f"${subtotal:.2f}")
    
    cols_shipping = st.columns([3, 1])
    with cols_shipping[0]:
        st.markdown("**Shipping**")
        if SHIPPING_RATE == 0:
            st.caption("🎉 Free!")
    with cols_shipping[1]:
        st.markdown(f"${SHIPPING_RATE:.2f}")
    
    cols_tax = st.columns([3, 1])
    with cols_tax[0]:
        st.markdown("**Tax (GST 9%)**")
    with cols_tax[1]:
        st.markdown(f"${tax:.2f}")
    
    st.markdown("---")
    
    cols_grand = st.columns([3, 1])
    with cols_grand[0]:
        st.markdown("### **Total**")
    with cols_grand[1]:
        st.markdown(f"<h3 style='color: #FF6B6B;'>${total:.2f}</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Shipping Info
    st.subheader("📦 Shipping Information")
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Full Name *", key="fil_name")
        customer_email = st.text_input("Email *", key="fil_email")
        customer_phone = st.text_input("Phone *", key="fil_phone")
    with col2:
        customer_address = st.text_area("Delivery Address *", height=132, key="fil_address")
    
    st.markdown("---")
    
    # Payment
    st.subheader("💰 Payment")
    st.markdown(f"### Total: ${total:.2f} SGD")
    
    if st.button("🔒 Proceed to Secure Payment", type="primary", use_container_width=True, key="btn_pay_filament"):
        if not all([customer_name, customer_email, customer_phone, customer_address]):
            st.error("Please fill in all required fields")
        elif not STRIPE_SECRET_KEY:
            st.error("Stripe is not configured. Please add your API key to .streamlit/secrets.toml")
        else:
            try:
                stripe_line_items = []
                
                for item in cart_items:
                    stripe_line_items.append({
                        'price_data': {
                            'currency': 'sgd',
                            'product_data': {
                                'name': item['product']['name'],
                                'description': f"{item['product']['material']} - {item['product']['color']}",
                            },
                            'unit_amount': int(item['product']['price'] * 100),
                        },
                        'quantity': item['quantity'],
                    })
                
                if SHIPPING_RATE > 0:
                    stripe_line_items.append({
                        'price_data': {
                            'currency': 'sgd',
                            'product_data': {'name': 'Shipping'},
                            'unit_amount': int(SHIPPING_RATE * 100),
                        },
                        'quantity': 1,
                    })
                
                stripe_line_items.append({
                    'price_data': {
                        'currency': 'sgd',
                        'product_data': {'name': 'Tax (GST 9%)'},
                        'unit_amount': int(tax * 100),
                    },
                    'quantity': 1,
                })
                
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=stripe_line_items,
                    mode='payment',
                    customer_email=customer_email,
                    success_url=st.secrets.get("success_url", "http://localhost:8501"),
                    cancel_url=st.secrets.get("cancel_url", "http://localhost:8501"),
                    metadata={
                        'customer_name': customer_name,
                        'order_type': 'filament',
                    }
                )
                
                st.success("✅ Payment session created!")
                st.markdown(f"**[Click here to complete payment]({session.url})**")
                
            except stripe.error.StripeError as e:
                st.error(f"Payment error: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# ====================================
# MAIN APP ROUTER
# ====================================
def main():
    # Custom CSS
    st.markdown("""
        <style>
        .main > div {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Route to appropriate view
    if st.session_state.view == 'home':
        show_home()
    elif st.session_state.view == 'printing':
        show_printing_service()
    elif st.session_state.view == 'printing_checkout':
        show_printing_checkout()
    elif st.session_state.view == 'filament':
        show_filament_store()
    elif st.session_state.view == 'filament_checkout':
        show_filament_checkout()

if __name__ == "__main__":
    main()