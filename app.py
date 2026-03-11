import streamlit as st
import json
from pathlib import Path
import time

json_file = Path("inventory.json")

if json_file.exists():
    with open(json_file, "r") as f:
        inventory = json.load(f)
else:
    # Default data if file doesn't exist
    inventory = [] 

order_id_create = 1
new_order_id = str(1)

#st.set_page_config(page_title="Smart Coffee Kiosk Application")
st.title("Smart Coffee Kiosk Application")

orders = []

tab1, tab2, tab3, tab4 = st.tabs(["Place Order", "View Inventory", "Restock", "Manage Orders"])

with tab1:
    select_item = st.selectbox("Item", ["Espresso", "Latte", "Cold Brew", "Mocha", "Blueberry Muffin"])
    quantity = st.number_input("Input Quantity", min_value= 1, step=1)
    name = st.text_input("Customer Name")
    order_btn = st.button("Place Order", key = "btn_order", type="primary", use_container_width=True)

    if order_btn:
        with st.spinner("Ordering..."):
            time.sleep(3)
            for item in inventory:
                if item['name'] == select_item:
                    if item['stock'] >= quantity:
                        item['stock'] = item['stock'] - quantity
                        with open(json_file, "w") as f:
                            json.dump(inventory, f, indent=4)
                        total_price = item['price'] * quantity
                        order = {
                            "order_id" : new_order_id,
                            "customer" : name,
                            "item" : select_item,
                            "total" : total_price,
                            "status" : "Placed"
                        }
                        order_id_create += 1
                        orders.append(order)
                        st.success("Ordered!")
                        st.dataframe(order)
                        time.sleep(4)
                        st.rerun()
                    else:
                        st.info("Out of Stock")
                        time.sleep(4)
                        st.rerun()