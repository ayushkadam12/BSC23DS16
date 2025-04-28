# Save as app.py and run: streamlit run app.py

import streamlit as st
import hashlib
import time

# --- Blockchain classes with full hashing ---

class Block:
    def __init__(self, parcel_id, location, event, previous_hash=''):
        self.timestamp = time.time()
        self.parcel_id = parcel_id
        self.location = location
        self.event = event
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = f"{self.timestamp}{self.parcel_id}{self.location}{self.event}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class ParcelBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    
    def create_genesis_block(self):
        return Block("GENESIS", "Origin", "Created blockchain", "0")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, parcel_id, location, event):
        new_block = Block(parcel_id, location, event, self.get_latest_block().hash)
        self.chain.append(new_block)
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# --- Streamlit UI ---

st.set_page_config(page_title="Parcel Blockchain Hashing Demo", page_icon="🔗", layout="wide")

st.title("🔗 Parcel Delivery Tracking Ledger with Hashing")

# Initialize blockchain
if "blockchain" not in st.session_state:
    st.session_state.blockchain = ParcelBlockchain()

# Form to add a new event
with st.form("add_event_form"):
    st.subheader("➕ Add New Parcel Event")
    parcel_id = st.text_input("Parcel ID")
    location = st.text_input("Current Location")
    event = st.text_input("Event Description")
    submitted = st.form_submit_button("Add Event to Blockchain")
    
    if submitted:
        if parcel_id and location and event:
            st.session_state.blockchain.add_block(parcel_id, location, event)
            st.success("✅ Event added and block hashed!")
        else:
            st.error("❗ Please fill out all fields!")

st.divider()

# Display the blockchain
st.subheader("📜 Blockchain Ledger (with Hashing Info)")

for idx, block in enumerate(st.session_state.blockchain.chain):
    with st.expander(f"Block {idx} | Parcel: {block.parcel_id}"):
        st.write(f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
        st.write(f"**Parcel ID:** {block.parcel_id}")
        st.write(f"**Location:** {block.location}")
        st.write(f"**Event:** {block.event}")
        st.code(f"Previous Hash: {block.previous_hash}")
        st.code(f"Current Hash: {block.hash}")

# Tampering simulation (optional)
st.divider()
st.subheader("🛠️ Tamper with a Block (Simulation)")

tamper_index = st.number_input("Select block index to tamper:", min_value=1, max_value=len(st.session_state.blockchain.chain)-1, step=1, format="%d")
tamper_data = st.text_input("New Event Data (fake tampering):")
if st.button("Tamper Block"):
    if tamper_data:
        # Tampering by changing the event
        block_to_tamper = st.session_state.blockchain.chain[tamper_index]
        block_to_tamper.event = tamper_data
        block_to_tamper.hash = block_to_tamper.calculate_hash()
        st.error("⚠️ Block tampered! Blockchain may be invalid now!")
    else:
        st.warning("Please enter new tampering data.")

# Blockchain validity check
st.divider()
if st.session_state.blockchain.is_chain_valid():
    st.success("✅ Blockchain is valid! No tampering detected.")
else:
    st.error("❗ Blockchain is INVALID! Tampering detected!")

