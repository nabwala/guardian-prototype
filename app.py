import streamlit as st
import pandas as pd
import datetime
from typing import Dict, List, Tuple
import random

# Configure page
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🔒",
    layout="wide"
)

# Initialize session state
if 'transactions' not in st.session_state:
    # Pre-seeded example transactions
    st.session_state.transactions = [
        {
            'timestamp': '2024-09-20 10:30:15',
            'customer_name': 'Amina Ochieng',
            'amount': 75000,
            'device': 'new',
            'location': 'Mombasa',
            'prev_location': 'Nairobi',
            'status': 'Flagged as Fraudulent',
            'reasons': 'High amount (>50,000), New device detected',
            'biometric_verified': False
        },
        {
            'timestamp': '2024-09-20 09:15:42',
            'customer_name': 'John Kamau',
            'amount': 12500,
            'device': 'trusted',
            'location': 'Nairobi',
            'prev_location': 'Nairobi',
            'status': 'Legitimate',
            'reasons': 'All checks passed',
            'biometric_verified': True
        },
        {
            'timestamp': '2024-09-20 08:45:20',
            'customer_name': 'Sarah Wanjiku',
            'amount': 45000,
            'device': 'trusted',
            'location': 'Kisumu',
            'prev_location': 'Eldoret',
            'status': 'Flagged as Fraudulent',
            'reasons': 'Location change >100km (Eldoret to Kisumu)',
            'biometric_verified': False
        }
    ]

def calculate_distance(loc1: str, loc2: str) -> int:
    """Simulate distance calculation between locations"""
    distances = {
        ('Nairobi', 'Mombasa'): 480,
        ('Nairobi', 'Kisumu'): 350,
        ('Nairobi', 'Eldoret'): 310,
        ('Mombasa', 'Kisumu'): 580,
        ('Eldoret', 'Kisumu'): 65,
        ('Eldoret', 'Mombasa'): 620,
        ('Nakuru', 'Nairobi'): 160,
        ('Nakuru', 'Kisumu'): 190,
    }
    
    key1 = (loc1, loc2)
    key2 = (loc2, loc1)
    
    return distances.get(key1, distances.get(key2, random.randint(50, 150)))

def fraud_detection_engine(customer_name: str, amount: float, device: str, location: str, prev_location: str) -> Tuple[str, List[str]]:
    """Simple rule-based fraud detection system"""
    flags = []
    
    # Rule 1: High amount threshold
    if amount > 50000:
        flags.append(f"High amount (>{50000:,})")
    
    # Rule 2: New device
    if device.lower() == 'new':
        flags.append("New device detected")
    
    # Rule 3: Location change > 100km
    if location != prev_location:
        distance = calculate_distance(location, prev_location)
        if distance > 100:
            flags.append(f"Location change >{100}km ({prev_location} to {location})")
    
    # Rule 4: Suspicious transaction patterns (random simulation)
    if amount % 1000 == 0 and amount > 20000:  # Round numbers above 20k
        flags.append("Suspicious round number transaction")
    
    if flags:
        return "Flagged as Fraudulent", flags
    else:
        return "Legitimate", ["All checks passed"]

# Main app
st.title("🔒 Fraud Detection System")
st.markdown("*Real-time transaction monitoring and verification*")

# Sidebar for inputs
st.sidebar.header("🔍 New Transaction")
st.sidebar.markdown("Enter transaction details below:")

with st.sidebar.form("transaction_form"):
    customer_name = st.text_input("Customer Name", placeholder="e.g., Jane Doe")
    amount = st.number_input("Amount (KES)", min_value=0.0, value=25000.0, step=1000.0)
    device = st.selectbox("Device Status", ["trusted", "new", "suspicious"])
    location = st.selectbox("Transaction Location", 
                           ["Nairobi", "Mombasa", "Kisumu", "Eldoret", "Nakuru", "Thika"])
    prev_location = st.selectbox("Previous Location", 
                                ["Nairobi", "Mombasa", "Kisumu", "Eldoret", "Nakuru", "Thika"])
    
    submit_transaction = st.form_submit_button("🔍 Analyze Transaction", use_container_width=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    if submit_transaction and customer_name:
        # Run fraud detection
        status, reasons = fraud_detection_engine(customer_name, amount, device, location, prev_location)
        
        # Display result
        st.subheader("🎯 Analysis Result")
        
        if status == "Flagged as Fraudulent":
            st.error(f"🚨 **{status}**")
            st.write("**Reasons:**")
            for reason in reasons:
                st.write(f"• {reason}")
            
            # Biometric verification section
            st.subheader("🔐 Biometric Verification Required")
            col_bio1, col_bio2 = st.columns(2)
            
            with col_bio1:
                if st.button("👆 Verify Fingerprint", use_container_width=True):
                    if random.random() > 0.3:  # 70% success rate
                        st.success("✅ Fingerprint Verified!")
                        biometric_verified = True
                    else:
                        st.error("❌ Fingerprint Verification Failed!")
                        biometric_verified = False
            
            with col_bio2:
                if st.button("🎤 Verify Voice", use_container_width=True):
                    if random.random() > 0.2:  # 80% success rate
                        st.success("✅ Voice Verified!")
                        biometric_verified = True
                    else:
                        st.error("❌ Voice Verification Failed!")
                        biometric_verified = False
            
            biometric_verified = st.session_state.get('bio_verified', False)
            
        else:
            st.success(f"✅ **{status}**")
            st.write("**Analysis:**")
            for reason in reasons:
                st.write(f"• {reason}")
            biometric_verified = True
        
        # Log transaction
        new_transaction = {
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'customer_name': customer_name,
            'amount': amount,
            'device': device,
            'location': location,
            'prev_location': prev_location,
            'status': status,
            'reasons': ', '.join(reasons),
            'biometric_verified': biometric_verified
        }
        
        st.session_state.transactions.insert(0, new_transaction)
        st.success("📝 Transaction logged successfully!")

with col2:
    st.subheader("📊 Quick Stats")
    
    # Calculate stats
    total_transactions = len(st.session_state.transactions)
    fraudulent_count = sum(1 for t in st.session_state.transactions if t['status'] == 'Flagged as Fraudulent')
    fraud_rate = (fraudulent_count / total_transactions * 100) if total_transactions > 0 else 0
    
    st.metric("Total Transactions", total_transactions)
    st.metric("Fraudulent Transactions", fraudulent_count)
    st.metric("Fraud Rate", f"{fraud_rate:.1f}%")
    
    # Risk indicator
    if fraud_rate > 30:
        st.error("🚨 High Risk Period")
    elif fraud_rate > 15:
        st.warning("⚠️ Elevated Risk")
    else:
        st.success("✅ Normal Risk Level")

# Audit Log / Dashboard
st.markdown("---")
st.subheader("📋 Transaction Audit Log")

if st.session_state.transactions:
    # Convert to DataFrame for better display
    df = pd.DataFrame(st.session_state.transactions)
    
    # Style the dataframe
    def color_status(val):
        if val == 'Flagged as Fraudulent':
            return 'background-color: #ffebee'
        else:
            return 'background-color: #e8f5e8'
    
    # Display table
    styled_df = df.style.applymap(color_status, subset=['status'])
    
    st.dataframe(
        styled_df,
        column_config={
            "timestamp": "Timestamp",
            "customer_name": "Customer",
            "amount": st.column_config.NumberColumn("Amount (KES)", format="%.0f"),
            "device": "Device",
            "location": "Location",
            "prev_location": "Previous Location",
            "status": "Status",
            "reasons": "Reasons",
            "biometric_verified": "Bio Verified"
        },
        hide_index=True,
        use_container_width=True
    )
    
    # Clear log button
    if st.button("🗑️ Clear Audit Log"):
        st.session_state.transactions = []
        st.rerun()
        
else:
    st.info("No transactions recorded yet. Submit a transaction to see it appear here.")

# Footer
st.markdown("---")
st.markdown("*This is a proof-of-concept fraud detection system for demonstration purposes.*")