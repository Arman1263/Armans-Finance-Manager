import sqlite3 as sq
import streamlit as st
import pandas as pd

# --- Database setup ---
conn = sq.connect('finance_tracker.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS finance (
        id INTEGER PRIMARY KEY,
        item TEXT NOT NULL,
        price INTEGER NOT NULL 
    )
''')
conn.commit()

# --- Functions ---
def see_expense():
    cursor.execute("SELECT * FROM finance")
    rows = cursor.fetchall()
    return rows

def add_expense(item, price):
    cursor.execute("INSERT INTO finance (item, price) VALUES (?, ?)", (item, price))
    conn.commit()

def update_expense(id, new_item, new_price):
    cursor.execute("UPDATE finance SET item = ?, price = ? WHERE id = ?", (new_item, new_price, id))
    conn.commit()

def delete_expense(id):
    cursor.execute("DELETE FROM finance WHERE id = ?", (id,))
    conn.commit()

# --- Streamlit UI ---
st.set_page_config(page_title="Finance Tracker", layout="centered")
st.title("💰 Arman’s Personal Finance Manager")

menu = ["See Expenses", "Add Expense", "Update Expense", "Delete Expense"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "See Expenses":
    st.subheader("📋 Your Expenses")
    rows = see_expense()
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Item", "Price"])
        st.table(df)

        total = df["Price"].sum()
        st.metric(label="💵 Total Expenses", value=f"{total} ₹")
    else:
        st.warning("No expenses found. Add some!")


elif choice == "Add Expense":
    st.subheader("➕ Add a New Expense")
    with st.form("add_form"):
        item = st.text_input("Item Name")
        price = st.number_input("Price", min_value=1, step=1)
        submit = st.form_submit_button("Add")
        if submit:
            add_expense(item, int(price))
            st.success(f"Added: {item} ({price} ₹)")

elif choice == "Update Expense":
    st.subheader("✏️ Update an Expense")
    rows = see_expense()
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Item", "Price"])
        st.dataframe(df)

        with st.form("update_form"):
            id = st.number_input("Enter ID to Update", min_value=1, step=1)
            new_item = st.text_input("New Item Name")
            new_price = st.number_input("New Price", min_value=1, step=1)
            submit = st.form_submit_button("Update")
            if submit:
                update_expense(id, new_item, int(new_price))
                st.success(f"Updated ID {id} → {new_item} ({new_price} ₹)")
    else:
        st.warning("No expenses to update.")

elif choice == "Delete Expense":
    st.subheader("🗑️ Delete an Expense")
    rows = see_expense()
    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Item", "Price"])
        st.dataframe(df)

        with st.form("delete_form"):
            id = st.number_input("Enter ID to Delete", min_value=1, step=1)
            submit = st.form_submit_button("Delete")
            if submit:
                delete_expense(id)
                st.error(f"Deleted expense with ID {id}")
    else:
        st.warning("No expenses to delete.")
