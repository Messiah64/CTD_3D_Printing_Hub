import streamlit as st
import streamlit_shadcn_ui as ui
from streamlit_stl import stl_from_file
from stl import mesh
import numpy as np
import tempfile
from datetime import datetime
import random
import os
import pandas as pd

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
    
    /* Quantity controls */
    .qty-controls {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    
    .qty-btn {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 2px solid #4f46e5;
        background: white;
        color: #4f46e5;
        font-size: 1.5rem;
        font-weight: bold;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }
    
    .qty-btn:hover {
        background: #4f46e5;
        color: white;
    }
    
    .qty-display {
        font-size: 1.3rem;
        font-weight: 600;
        min-width: 50px;
        text-align: center;
        color: #4f46e5;
    }
    
    /* Container styling */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        border-radius: 10px;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
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
    .dataframe {
        font-size: 0.95rem;
    }
    
    /* Metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
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

MATERIALS = {
    "PLA": {"density": 1.24, "cost": 0.05, "desc": "General purpose printing"},
    "ABS": {"density": 1.04, "cost": 0.04, "desc": "Functional parts"},
    "PETG": {"density": 1.27, "cost": 0.06, "desc": "Durable applications"},
    "Resin": {"density": 1.10, "cost": 0.12, "desc": "High detail models"},
    "Nylon": {"density": 1.14, "cost": 0.08, "desc": "Strong mechanical parts"}
}

# ADD YOUR IMAGE PATHS HERE
FILAMENTS = [
    {
        "id": "pla_white",
        "name": "PLA Filament - White",
        "material": "PLA",
        "price": 25.00,
        "color": "White",
        "stock": "In Stock",
        "rating": 4.8,
        "image": "https://via.placeholder.com/300x200/FFFFFF/000000?text=PLA+White"  # Replace with your image path
    },
    {
        "id": "pla_black",
        "name": "PLA Filament - Black",
        "material": "PLA",
        "price": 25.00,
        "color": "Black",
        "stock": "In Stock",
        "rating": 4.9,
        "image": "https://via.placeholder.com/300x200/000000/FFFFFF?text=PLA+Black"  # Replace with your image path
    },
    {
        "id": "abs_red",
        "name": "ABS Filament - Red",
        "material": "ABS",
        "price": 28.00,
        "color": "Red",
        "stock": "In Stock",
        "rating": 4.7,
        "image": "https://via.placeholder.com/300x200/FF0000/FFFFFF?text=ABS+Red"  # Replace with your image path
    },
    {
        "id": "petg_blue",
        "name": "PETG Filament - Blue",
        "material": "PETG",
        "price": 30.00,
        "color": "Blue",
        "stock": "In Stock",
        "rating": 4.6,
        "image": "https://via.placeholder.com/300x200/0000FF/FFFFFF?text=PETG+Blue"  # Replace with your image path
    },
    {
        "id": "tpu_clear",
        "name": "TPU Flexible - Clear",
        "material": "TPU",
        "price": 35.00,
        "color": "Clear",
        "stock": "Low Stock",
        "rating": 4.5,
        "image": "https://via.placeholder.com/300x200/CCCCCC/000000?text=TPU+Clear"  # Replace with your image path
    },
    {
        "id": "nylon_natural",
        "name": "Nylon Filament - Natural",
        "material": "Nylon",
        "price": 40.00,
        "color": "Natural",
        "stock": "In Stock",
        "rating": 4.8,
        "image": "https://via.placeholder.com/300x200/F5F5DC/000000?text=Nylon+Natural"  # Replace with your image path
    }
]

# Initialize session state variables
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
    
    # Items Table
    st.markdown('<h3 class="section-header">🛒 Items</h3>', unsafe_allow_html=True)
    
    # Create dataframe for items
    items_data = []
    for item in invoice_data['items']:
        items_data.append({
            'Description': item['description'],
            'Quantity': item['quantity'],
            'Unit Price': f"${item['unit_price']:.2f}",
            'Total': f"${item['total']:.2f}"
        })
    
    df = pd.DataFrame(items_data)
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Description": st.column_config.TextColumn("Description", width="large"),
            "Quantity": st.column_config.NumberColumn("Qty", width="small"),
            "Unit Price": st.column_config.TextColumn("Unit Price", width="medium"),
            "Total": st.column_config.TextColumn("Total", width="medium"),
        }
    )
    
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
        ui.metric_card(title="Materials", content="6+", description="Premium filaments", key="m1")
    with col2:
        ui.metric_card(title="Accuracy", content="±0.1mm", description="High precision", key="m2")
    with col3:
        ui.metric_card(title="Delivery", content="24-48h", description="Fast turnaround", key="m3")
    with col4:
        ui.metric_card(title="Rating", content="4.8/5", description="500+ customers", key="m4")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Service selection
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        with st.container(border=True):
            st.markdown("### 🖨️ 3D Printing Service")
            st.markdown("""
            ✓ Multiple Materials - 5 options available  
            ✓ Instant Pricing - Upload for immediate quote  
            ✓ High Quality - Industrial-grade printers  
            ✓ Fast Delivery - 24-48 hour turnaround
            """)
            if st.button("Start Your Print", key="btn_print", use_container_width=True, type="primary"):
                navigate_to('printing')
    
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

def show_printing_service():
    """Display 3D printing service page with STL upload and pricing"""
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button("← Back"):
            navigate_to('home')
    with col2:
        st.markdown("### 🖨️ 3D Printing Service")
    
    st.markdown("---")
    
    col_left, col_right = st.columns([1.3, 1], gap="large")
    
    with col_left:
        st.markdown("#### Upload Your STL File")
        
        uploaded_file = st.file_uploader("Choose STL file", type="stl", label_visibility="collapsed")
        
        material = st.selectbox("Select Material", list(MATERIALS.keys()))
        
        st.info(f"""
        **{material} Properties:**  
        Density: {MATERIALS[material]['density']} g/cm³  
        Cost: ${MATERIALS[material]['cost']:.3f}/gram  
        Use: {MATERIALS[material]['desc']}
        """)
        
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".stl") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
                st.session_state.stl_file_path = tmp_file_path
            
            try:
                # Calculate volume and weight from STL file
                your_mesh = mesh.Mesh.from_file(tmp_file_path)
                vectors = your_mesh.vectors
                volume_mm3 = np.abs(np.sum(np.einsum('...i,...i->...', vectors[:, 0], np.cross(vectors[:, 1], vectors[:, 2])))) / 6
                volume_cm3 = volume_mm3 / 1000.0
                
                weight_g = volume_cm3 * MATERIALS[material]['density']
                cost = weight_g * MATERIALS[material]['cost']
                
                # Store in session state
                st.session_state.print_volume = volume_cm3
                st.session_state.print_weight = weight_g
                st.session_state.print_cost = cost
                st.session_state.print_material = material
                
                st.success("✅ Model analyzed successfully!")
                
                # Display 3D preview
                st.markdown("#### 3D Preview")
                stl_from_file(
                    file_path=tmp_file_path,
                    color='#3b82f6',
                    material='material',
                    auto_rotate=True,
                    height=400,
                    key="stl_viewer"
                )
                
            except Exception as e:
                st.error(f"Error processing STL: {str(e)}")
            finally:
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
    
    with col_right:
        st.markdown("#### 💰 Price Estimation")
        
        if uploaded_file:
            # Display metrics
            col1, col2 = st.columns(2)
            with col1:
                ui.metric_card(
                    title="Volume",
                    content=f"{st.session_state.print_volume:.2f}",
                    description="cm³",
                    key="vol_metric"
                )
            with col2:
                ui.metric_card(
                    title="Weight",
                    content=f"{st.session_state.print_weight:.2f}",
                    description="grams",
                    key="weight_metric"
                )
            
            st.markdown("---")
            
            # Discount code input
            discount_code = st.text_input("Discount Code", placeholder="Optional")
            
            base_cost = st.session_state.print_cost
            discount = apply_discount(base_cost, discount_code)
            final_cost = base_cost - discount
            
            st.session_state.discount_code = discount_code
            st.session_state.discount_amount = discount
            
            # Display pricing
            if discount > 0:
                st.success(f"✅ Discount applied: {DISCOUNT_CODES[discount_code.upper()]*100:.0f}% off!")
                st.markdown(f"<p style='font-size: 1.2rem;'>~~${base_cost:.2f}~~ <strong style='color: #10b981; font-size: 1.5rem;'>${final_cost:.2f} SGD</strong></p>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="total-box">
                    <h2>${final_cost:.2f} SGD</h2>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("Proceed to Checkout", key="checkout_print", type="primary", use_container_width=True):
                navigate_to('printing_checkout')
        else:
            st.info("📤 Upload a file to get instant pricing")

def show_printing_checkout():
    """Display checkout page for 3D printing service"""
    if st.session_state.show_invoice and st.session_state.invoice_data:
        # Display invoice
        if st.button("← Back to Checkout", key="back_to_checkout"):
            st.session_state.show_invoice = False
            st.rerun()
        
        st.markdown("---")
        display_invoice(st.session_state.invoice_data)
        return
    
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button("← Back", key="back_checkout"):
            navigate_to('printing')
    with col2:
        st.markdown("### 🛒 Checkout")
    
    st.markdown("---")
    
    if st.session_state.print_cost == 0:
        st.error("No order found. Please upload a model first.")
        return
    
    col_left, col_right = st.columns([1.5, 1], gap="large")
    
    with col_left:
        st.markdown('<h4 class="section-header">📝 Contact Information</h4>', unsafe_allow_html=True)
        customer_name = st.text_input("Name *")
        customer_email = st.text_input("Email *")
        customer_phone = st.text_input("Phone *")
        customer_address = st.text_area("Address *", height=100)
    
    with col_right:
        st.markdown('<h4 class="section-header">📦 Order Summary</h4>', unsafe_allow_html=True)
        
        base_cost = st.session_state.print_cost
        discount = st.session_state.discount_amount
        final_cost = base_cost - discount
        
        st.info(f"""
        **3D Print Service**  
        Material: {st.session_state.print_material}  
        Volume: {st.session_state.print_volume:.2f} cm³  
        Weight: {st.session_state.print_weight:.2f} g  
        
        Subtotal: ${base_cost:.2f}
        """)
        
        if discount > 0:
            st.success(f"✅ Discount: -${discount:.2f}")
        
        st.markdown(f"""
        <div class="total-box">
            <h2>${final_cost:.2f} SGD</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 View Invoice", type="primary", use_container_width=True):
            if not all([customer_name, customer_email, customer_phone, customer_address]):
                st.error("⚠️ Please fill in all required fields")
            else:
                invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
                
                invoice_data = {
                    'invoice_number': invoice_number,
                    'date': datetime.now().strftime('%B %d, %Y'),
                    'customer_name': customer_name,
                    'customer_email': customer_email,
                    'customer_phone': customer_phone,
                    'customer_address': customer_address.replace('\n', '<br>'),
                    'order_type': '3D Printing Service',
                    'items': [{
                        'description': f'3D Printing - {st.session_state.print_material}',
                        'quantity': 1,
                        'unit_price': base_cost,
                        'total': base_cost
                    }],
                    'subtotal': base_cost,
                    'discount': discount,
                    'discount_code': st.session_state.discount_code.upper() if discount > 0 else '',
                    'total': final_cost
                }
                
                st.session_state.invoice_data = invoice_data
                st.session_state.show_invoice = True
                st.rerun()

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
                    # Product Image - FIXED: use_column_width instead of use_container_width
                    try:
                        st.image(product['image'], use_column_width=True)
                    except Exception as e:
                        st.warning(f"Image not found: {product['name']}")
                    
                    st.markdown(f"**{product['name']}**")
                    st.caption(f"{product['material']} • {product['color']} • {product['stock']}")
                    st.caption(f"⭐ {product['rating']}/5")
                    
                    st.markdown(f"### ${product['price']:.2f}")

                    current_qty = st.session_state.filament_cart.get(product['id'], 0)
                    
                    # Always show Add to Cart button
                    if st.button("Add to Cart", key=f"add_{product['id']}", use_container_width=True, type="primary"):
                        if current_qty == 0:
                            st.session_state.filament_cart[product['id']] = 1
                        else:
                            st.session_state.filament_cart[product['id']] += 1
                        st.rerun()
                    
                    # Show quantity controls if item is in cart
                    if current_qty > 0:
                        st.markdown(f"""
                            <div class="qty-controls">
                                <span class="qty-display">In Cart: {current_qty}</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Remove button
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
        'printing': show_printing_service,
        'printing_checkout': show_printing_checkout,
        'filament': show_filament_store,
        'filament_checkout': show_filament_checkout
    }
    
    view_func = views.get(st.session_state.view, show_home)
    view_func()

if __name__ == "__main__":
    main()
