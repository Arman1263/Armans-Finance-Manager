import sqlite3 as sq

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

def see_expense():
    cursor.execute("SELECT * FROM finance")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No expenses found")


def add_expense(item, price):
    cursor.execute("INSERT INTO finance  (item, price) VALUES (?, ?)",(item, price))
    conn.commit()

def update_expense(id, new_item, new_price):
    cursor.execute("UPDATE finance SET item = ?, price = ? WHERE id = ?",
        (new_item, new_price, id))
    conn.commit()

def delete_expense(id):
    cursor.execute("DELETE FROM finance  WHERE id = ?", (id, )) ## , is necessary becoz it will accept as tuple 
    conn.commit()

def main():
    while True:
        print("\n=== Arman`s Personal Finance Manager using DB ===")
        print("1. See Expences")
        print("2. Add Expences")
        print("3. Update Expences")
        print("4. Delete Expences")
        print("5. Exit")
        choice = input("Enter the Choice : ")

        if choice == '1':
            see_expense()

        elif choice == '2':
            item = input("Enter item name to Add : ")
            price = int(input("Enter item price : "))
            add_expense(item, price)

        elif choice == '3':
            id = input("Enter ID of item to Update : ")
            item = input("Enter item name : ")
            price = int(input("Enter item price : "))
            update_expense(id, item, price)

        elif choice == '4':
            id = input("Enter ID of item of Delete : ")
            delete_expense(id)

        elif choice == '5':
            print("Goodbye...")
            break

        else:
            print("Enter a valid choice...")

    conn.close()

if __name__ == "__main__":
    main()