import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from datetime import datetime
import random
from PyPDF2 import PdfFileReader
from tkinter import filedialog
from tkinter import PhotoImage

# Create a MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nagag0410?",
    database="amc"
)



cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS amc_rec (
    amc_id INT NOT NULL PRIMARY KEY,
    amc_name VARCHAR(255),
    address VARCHAR(255),
    amc_type VARCHAR(255));"""
)
cursor.execute("""CREATE TABLE IF NOT EXISTS asset (
    asset_id INT NOT NULL PRIMARY KEY,
    asset_type VARCHAR(255),
    asset_name VARCHAR(255),
    no_of_shares INT,
    promoter_holding VARCHAR(255),
    valuation VARCHAR(255));"""
)
cursor.execute("""CREATE TABLE IF NOT EXISTS bank (
    ifsc_code VARCHAR(20),
    bank_name VARCHAR(255),
    account_no INT NOT NULL PRIMARY KEY,
    balance_amount DECIMAL(10,2),
    amc_id INT,
    FOREIGN KEY (amc_id) REFERENCES amc_rec(amc_id)
);"""
)
cursor.execute("""CREATE TABLE IF NOT EXISTS certificate (
    cert_id INT NOT NULL PRIMARY KEY,
    cert_name VARCHAR(255),
    issue_date DATE,
    expiry_date DATE
);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS cus (
    cus_id INT NOT NULL PRIMARY KEY,
    cus_dob DATE,
    cus_type VARCHAR(255),
    cus_name VARCHAR(255),
    cus_addr VARCHAR(255),
    cus_g VARCHAR(1),
    cus_ph CHAR(10),
    cus_age INT,
    amc_id INT,
    FOREIGN KEY (amc_id) REFERENCES amc_rec(amc_id)
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS fund_manager (
    fm_id INT NOT NULL PRIMARY KEY,
    amc_id INT,
    FOREIGN KEY (amc_id) REFERENCES amc_rec(amc_id)
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS fund (
    fund_id INT NOT NULL PRIMARY KEY,
    asset_class VARCHAR(255),
    fund_size INT,
    return_pa INT,
    fund_balance INT,
    manages_id INT,
    FOREIGN KEY (manages_id) REFERENCES fund_manager(fm_id)
);""")

cursor.execute("""CREATE TABLE IF NOT EXISTS investment (
    inv_id INT NOT NULL PRIMARY KEY,
    invest_amt INT,
    fund_id INT,
    cus_id INT,
    invest_date DATE,
    FOREIGN KEY (fund_id) REFERENCES fund(fund_id),
    FOREIGN KEY (cus_id) REFERENCES cus(cus_id)
);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS transaction (
    transaction_id INT NOT NULL PRIMARY KEY,
    timestamp DATETIME,
    transaction_amount INT,
    transaction_type VARCHAR(255),
    asset_id INT,
    FOREIGN KEY (asset_id) REFERENCES asset(asset_id)
);""")
# Function to check if an AMC record exists
def check_amc():
    amc_name = amc_name_entry.get()
    cursor.execute("SELECT * FROM amc_rec WHERE amc_name = %s", (amc_name,))
    record = cursor.fetchone()
    global current_amc_id
    if record:
        # AMC record exists, navigate to the next page
        messagebox.showinfo("Success", "AMC record exists!")
        #global current_amc_id
        current_amc_id = record[0]  # Get the AMC ID from the database
        window.withdraw()  # Hide the login window
        activities()
        
        # Add code to navigate to the next page here
    else:
        # AMC record doesn't exist, add it and navigate to the next page
        
        insert_amc()
        cursor.execute("SELECT * FROM amc_rec WHERE amc_name = %s", (amc_name,))
        record = cursor.fetchone()
        current_amc_id = record[0]  # Get the AMC ID from the database
        window.withdraw()
        activities()
        # Add code to navigate to the next page here

# Function to insert a new AMC record
def insert_amc():
    amc_id=int(amc_id_entry.get())
    address = address_entry.get("1.0", tk.END).strip()
    type = type_entry.get()
    amc_name = amc_name_entry.get()
    
    cursor.execute("INSERT INTO amc_rec (amc_id,address, amc_type, amc_name) VALUES (%s,%s, %s, %s)",
                   (amc_id,address, type, amc_name))
    
    db.commit()
    messagebox.showinfo("Success", "AMC record added!")

def activities():
    options_window = tk.Toplevel()
    options_window.title("WealthWise - Main Menu")

    icon_path = "images/icon.ico"  # Replace with the path to your icon file
    options_window.iconbitmap(icon_path)
    
    screen_width = options_window.winfo_screenwidth()
    screen_height = options_window.winfo_screenheight()

    # Set window size and position for fullscreen and centered
    window_width = int(screen_width)
    window_height = int(screen_height)
    options_window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")

    options_window.configure(bg="#518db5")
    background_image1 = PhotoImage(file ="images/4.png")
    background_label = tk.Label(options_window, image=background_image1)
    background_label.place(relwidth=1, relheight=1)

    options_frame = tk.Frame(options_window, pady=20, padx=30)
    options_frame.pack(expand=True)
    options_frame.configure(bg="#83aeca", highlightbackground="#00013b", highlightthickness=2)


    label = tk.Label(options_frame, text="CHOOSE AN OPTION", font=("Helvetica", 16), bg="#83aeca")
    label.pack(pady=20)

    buttons_font = ("Helvetica", 14)
    search_button = tk.Button(options_frame, text="Manage Bank Account", command=show_options_window, font= buttons_font, width=25, bg='blue', fg='white')
    search_button.pack(pady=10)

    view_button = tk.Button(options_frame, text="Manage Customers", command=cust_options, font=buttons_font, width=25, bg='blue', fg='white')
    view_button.pack(pady=10)

    add_button = tk.Button(options_frame, text="Fund Manager", command=fm, font=buttons_font, width=25, bg='blue', fg='white')
    add_button.pack(pady=10)

    asin_button = tk.Button(options_frame, text="Asset Investment", command=ass_inves, font=buttons_font, width=25, bg='blue', fg='white')
    asin_button.pack(pady=10)

    exit_button = tk.Button(options_frame, text="EXIT", command=exit_application, font=labels_font, width =15, bg='red', fg='white')
    exit_button.pack(pady=20)


    options_window.mainloop()

def ass_inves():
    options_window = tk.Toplevel()
    options_window.title("WealthWise - Asset Management")

    icon_path = "images/icon.ico"  # Replace with the path to your icon file
    options_window.iconbitmap(icon_path)

    options_window.configure(bg="#518db5")
    background_image = PhotoImage(file="images/7.png")
    background_label = tk.Label(options_window, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Get the screen width and height
    screen_width = options_window.winfo_screenwidth()
    screen_height = options_window.winfo_screenheight()

    # Set window size and position for fullscreen and centered
    window_width = int(screen_width )
    window_height = int(screen_height)
    options_window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")

    # Create a frame to contain all widgets
    o_frame = tk.Frame(options_window, pady=20, padx=20)
    o_frame.pack(expand=True)
    o_frame.configure(bg="#83aeca", highlightbackground="#00013b", highlightthickness=2)
    
    def buy():
        #transaction_id = random.randint(1000, 9999)
        transaction_id = tid_entry.get()
        # Get the current timestamp
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Capture user inputs for transaction amount, transaction type, and asset ID
        transaction_amount = tamt_entry.get()
        transaction_type = ttype_entry.get()
        asset_id = asid_entry.get()
        cursor.execute("CREATE TABLE IF NOT EXISTS transaction (transaction_id INT, timestamp DATETIME, transaction_amount DECIMAL(10, 2), transaction_type VARCHAR(255), asset_id INT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS bill (bill_id INT AUTO_INCREMENT PRIMARY KEY, transaction_id INT, timestamp DATETIME, transaction_amount DECIMAL(10, 2), transaction_type VARCHAR(255), asset_id INT, FOREIGN KEY (asset_id) REFERENCES asset(asset_id))")
        cursor.execute("""
        CREATE TRIGGER bill_trigger
        AFTER INSERT ON transaction
        FOR EACH ROW
        BEGIN
            INSERT INTO bill (transaction_id, timestamp, transaction_amount, transaction_type, asset_id)
            VALUES (NEW.transaction_id, NEW.timestamp, NEW.transaction_amount, NEW.transaction_type, NEW.asset_id);
        END;
        """)
        # Insert data into the transaction table
        cursor.execute("INSERT INTO transaction (transaction_id, timestamp, transaction_amount, transaction_type, asset_id) VALUES (%s, %s, %s, %s, %s)",
                    (transaction_id, current_timestamp, transaction_amount, transaction_type, asset_id))
        db.commit()
        display_generated_bill(transaction_id, current_timestamp, transaction_amount, transaction_type, asset_id)
    def display_generated_bill(transaction_id, timestamp, transaction_amount, transaction_type, asset_id):
    # Retrieve the bill details from the 'bill' table
        cursor.execute("SELECT * FROM bill WHERE transaction_id = %s", (transaction_id,))
        bill_record = cursor.fetchone()

        bill_window = tk.Toplevel()
        bill_window.title("Transaction Bill/Acknowledgment")

        bill_text = f"Transaction ID: {transaction_id}\n"
        bill_text += f"Timestamp: {timestamp}\n"
        bill_text += f"Transaction Amount: {transaction_amount}\n"
        bill_text += f"Transaction Type: {transaction_type}\n"
        bill_text += f"Asset ID: {asset_id}\n"
        bill_text += f"Bill ID: {bill_record[0]}\n"  # Display the bill ID from the 'bill' table

        bill_label = tk.Label(bill_window, text=bill_text, font=("Helvetica", 12))
        bill_label.pack(pady=10)
    def show_asset():
        # seeass_window = tk.Tk()
        # seeass_window.title("BUY ASSET")
        query = """
        SELECT asset_id,asset_name,asset_type,no_of_shares,promoter_holding,valuation from asset;
        """
        cursor.execute(query)
        records = cursor.fetchall()
        print(records)
        search_res_window = tk.Tk()
        search_res_window.title("Search")
        search_result = tk.Text(search_res_window, height=20, width=120, state="disabled", font=("Helvetica", 12), bg="#83aeca", highlightbackground="#00013b", highlightthickness=2)
        search_result.pack(pady=10)
        if records:
            # Display the search results
            search_result.config(state="normal")
            search_result.delete(1.0, "end")
            for record in records:
                search_result.insert("end", f"Asset_id: {record[0]}, Asset_name: {record[1]}, Asset_Type: {record[2]},No._of_shares: {record[3]},Promoter_holding: {record[4]}\n")
            search_result.config(state="disabled")
        else:
            messagebox.showinfo("Search", "NO assets")
        search_res_window.mainloop()

    log_button = tk.Button(o_frame, text="See Assets ", command=show_asset, font=("Helvetica", 15), width=25, bg='blue', fg='white')
    log_button.pack(pady=10)

    asid_label = tk.Label(o_frame, text="Asset ID", font=("Helvetica", 15), bg="#83aeca")
    asid_label.pack(pady=5)
    asid_entry = tk.Entry(o_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    asid_entry.pack(pady=5)

    tid_label = tk.Label(o_frame, text="Transaction ID", font=("Helvetica", 15), bg="#83aeca")
    tid_label.pack(pady=5)
    tid_entry = tk.Entry(o_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    #tid_entry=random.randint(1000, 9999)
    tid_entry.pack(pady=5)

    tamt_label = tk.Label(o_frame, text="Transaction Amount ", font=("Helvetica", 15), bg="#83aeca")
    tamt_label.pack(pady=5)
    tamt_entry = tk.Entry(o_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    tamt_entry.pack(pady=5)

    ttype_label = tk.Label(o_frame, text="Transaction Tyoe", font=("Helvetica", 15), bg="#83aeca")
    ttype_label.pack(pady=5)
    ttype_entry = tk.Entry(o_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    ttype_entry.pack(pady=5)
    
    buy_button = tk.Button(o_frame, text="Buy Assets ", command=buy, font=("Helvetica", 15), width=25, bg='blue', fg='white')
    buy_button.pack(pady=10)

    exit_button = tk.Button(o_frame, text="EXIT", command=options_window.destroy, font=labels_font, width =15, bg='red', fg='white')
    exit_button.pack(pady=20)
    options_window.mainloop()

def cust_options():
    options_window = tk.Toplevel()
    options_window.title("WealthWise - Customer Management")

    icon_path = "images/icon.ico"  # Replace with the path to your icon file
    options_window.iconbitmap(icon_path)

    options_window.configure(bg="#518db5")
    background_image = PhotoImage(file="images/6.png")
    background_label = tk.Label(options_window, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Get the screen width and height
    screen_width = options_window.winfo_screenwidth()
    screen_height = options_window.winfo_screenheight()

    # Set window size and position for fullscreen and centered
    window_width = int(screen_width )
    window_height = int(screen_height)
    options_window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")

    # Create a frame to contain all widgets
    o_frame = tk.Frame(options_window, pady=20, padx=20)
    o_frame.pack(expand=True)
    o_frame.configure(bg="#83aeca", highlightbackground="#00013b", highlightthickness=2)

    label = tk.Label(o_frame, text="CHOOSE AN OPTION", font=("Helvetica", 16), bg="#83aeca")
    label.pack(pady=20)
    log_button = tk.Button(o_frame, text="Customer Login ", command=show_cust_options, font=("Helvetica", 14), width=25, bg='blue', fg='white')
    log_button.pack(pady=10)
    invest_button = tk.Button(o_frame, text="Customer Investment", command=show_cust_invest, font=("Helvetica", 14), width=25, bg='blue', fg='white')
    invest_button.pack(pady=10)
    invest_button = tk.Button(o_frame, text="Update Customer Info", command=update_cus_add, font=("Helvetica", 14), width=25, bg='blue', fg='white')
    invest_button.pack(pady=10)
    invest_button = tk.Button(o_frame, text="Deactivate Customer", command=del_cus_id, font=("Helvetica", 14), width=25, bg='blue', fg='white')
    invest_button.pack(pady=10)
    exit_button = tk.Button(o_frame, text="EXIT", command=options_window.destroy, font=labels_font, width =15, bg='red', fg='white')
    exit_button.pack(pady=10)

    options_window.mainloop()

def update_cus_add():
    def update_address():
        cus_id=int(cus_id_entry.get())
        add = add_entry.get()
        try:
        # SQL query to update the address in the cus table
            update_query = "UPDATE cus SET cus_addr = %s WHERE cus_id = %s"
            cursor.execute(update_query, (add, cus_id))
            db.commit()
            messagebox.showinfo("Success", "Address updated successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error updating address: {err}")
    w=tk.Tk()
    w.title('UPDATE CUSTOMER INFO')
    
    cus_id_label = tk.Label(w, text="Enter Cus ID", font=("Helvetica", 12))
    cus_id_label.pack(pady=5)
    cus_id_entry = tk.Entry(w, font=("Helvetica", 12))
    cus_id_entry.pack(pady=5)

    add_label = tk.Label(w, text="Enter new address", font=("Helvetica", 12))
    add_label.pack(pady=5)
    add_entry = tk.Entry(w, font=("Helvetica", 12))
    add_entry.pack(pady=5)
    update_address_button = tk.Button(w, text="Update Address", command=update_address, font=("Helvetica", 12))
    update_address_button.pack(pady=10)
    w.mainloop()
    

def del_cus_id():
    def del_acc():
        cid=cus_id_entry.get()
        try:
            # SQL query to update the address in the cus table
            delete_query = "DELETE FROM cus WHERE cus_id = %s"
            cursor.execute(delete_query, (cid,))
            db.commit()
            messagebox.showinfo("Success", "Account Deleted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error deleting account: {err}")
    w=tk.Tk()
    w.title('DELETE CUSTOMER INFO')
    
    cus_id_label = tk.Label(w, text="Enter Cus ID", font=("Helvetica", 12))
    cus_id_label.pack(pady=5)
    cus_id_entry = tk.Entry(w, font=("Helvetica", 12))
    cus_id_entry.pack(pady=5)

    del_button = tk.Button(w, text="Deactivate Acc.", command=del_acc, font=("Helvetica", 12))
    del_button.pack(pady=10)
    w.mainloop()

def fm():
    def cmi():
        try:
        # Nested query to calculate the sum of investment amounts for each customer
            query = """
                SELECT cus_id, cus_name, (
                    SELECT MAX(invest_amt) FROM investment WHERE investment.cus_id = cus.cus_id
                ) AS total_investment
                FROM cus
            """
            cursor.execute(query)
            result = cursor.fetchall()

            # Display the result
            for row in result:
                messagebox.showinfo("Max Investment", f"Customer ID: {row[0]}\nCustomer Name: {row[1]}\nMax Investment by Customer: {row[2]}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching data: {err}")

    fm_options_window = tk.Toplevel()
    fm_options_window.title("WealthWise - Fund Manager Window")

    
    icon_path = "images/icon.ico"  # Replace with the path to your icon file
    fm_options_window.iconbitmap(icon_path)

    
    background_image = PhotoImage(file="images/4.png")
    background_label = tk.Label(fm_options_window, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Get the screen width and height
    screen_width = fm_options_window.winfo_screenwidth()
    screen_height = fm_options_window.winfo_screenheight()

    # Set window size and position for fullscreen and centered
    window_width = int(screen_width )
    window_height = int(screen_height)
    fm_options_window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")

    # Create a frame to contain all widgets
    fm_frame = tk.Frame(fm_options_window, pady=20, padx=20)
    fm_frame.pack(expand=True)
    fm_frame.configure(bg="#83aeca", highlightbackground="#00013b", highlightthickness=2)
    
    label = tk.Label(fm_frame, text="CHOOSE AN OPTION", font=("Helvetica", 16), bg="#83aeca")
    label.pack(pady=10)
    log_button = tk.Button(fm_frame, text="Fund Manager Login ", command=fm_login, font=("Helvetica", 14), width=35, bg='blue', fg='white')
    log_button.pack(pady=10)
    uc_button= tk.Button(fm_frame, text="Certificate Upload ", command=upload, font=("Helvetica", 14), width=35, bg='blue', fg='white')
    uc_button.pack(pady=10)
    cm_button= tk.Button(fm_frame, text="View Customer with Maximum Investmert", command=cmi, font=("Helvetica", 14), width=35, bg='blue', fg='white')
    cm_button.pack(pady=10)

    exit_button = tk.Button(fm_frame, text="EXIT", command=fm_options_window.destroy, font=labels_font, width =20, bg='red', fg='white')
    exit_button.pack(pady=20)
    fm_options_window.mainloop()

def upload():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    if file_path:
        cert_id = extract_certificate_info(file_path)
        show_certificate_input_window(cert_id)
def extract_certificate_info(file_path):
    # Extract certificate information from the PDF file (you may need to customize this part)
    pdf = PdfFileReader(open(file_path, 'rb'))
    cert_id = None

    for page_number in range(1):
        page = pdf.getPage(page_number)
        page_text = page.extractText()
        print(page_text)
        if 'Certificate ID:' in page_text:
            cert_id = int(page_text.split("Certificate ID:")[1].strip().split()[0])
            break

    print("Extracted Certificate ID:", cert_id)
    return cert_id
def add_certificate(cert_id, cert_name, issue_date, expiry_date):
    stored_procedure_code = """
    CREATE PROCEDURE cert_insert(IN cert_id INT, IN cert_name VARCHAR(255), IN issue_date DATE, IN expiry_date DATE)
    BEGIN
        INSERT INTO certificate (cert_id, cert_name, issue_date, expiry_date) VALUES(%s,%s,%s,%s) ,(cert_id , cert_name,issue_date,expiry_date);
    END
    """
    
    # Execute the stored procedure code
    cursor = db.cursor()
    cursor.execute(stored_procedure_code)
    db.commit()
    
    
    # cursor.execute("INSERT INTO certificate (cert_id, cert_name, issue_date, expiry_date) VALUES (%s, %s, %s, %s)",
    #                (cert_id, cert_name, issue_date, expiry_date))
    # db.commit()
    messagebox.showinfo("Success", "Certificate information added!")

def show_certificate_input_window(cert_id):
    cert_input_window = tk.Tk()
    cert_input_window.title("Add Certificate Information")

    cert_id_label = tk.Label(cert_input_window, text="Certificate ID:", font=("Helvetica", 12))
    cert_id_label.pack(pady=5)

    cert_id_entry = tk.Entry(cert_input_window, font=("Helvetica", 12))
    cert_id_entry.insert(0, cert_id)
    cert_id_entry.pack(pady=5)

    cert_name_label = tk.Label(cert_input_window, text="Certificate Name:", font=("Helvetica", 12))
    cert_name_label.pack(pady=5)

    cert_name_entry = tk.Entry(cert_input_window, font=("Helvetica", 12))
    cert_name_entry.pack(pady=5)
    issue_date_label = tk.Label(cert_input_window, text="Issue Date:", font=("Helvetica", 12))
    issue_date_label.pack(pady=5)

    issue_date_entry = tk.Entry(cert_input_window, font=("Helvetica", 12))
    issue_date_entry.pack(pady=5)

    expiry_date_label = tk.Label(cert_input_window, text="Expiry Date:", font=("Helvetica", 12))
    expiry_date_label.pack(pady=5)

    expiry_date_entry = tk.Entry(cert_input_window, font=("Helvetica", 12))
    expiry_date_entry.pack(pady=5)

    add_cert_button = tk.Button(cert_input_window, text="Add Certificate", command=lambda: add_certificate(
        cert_id_entry.get(), cert_name_entry.get(), issue_date_entry.get(), expiry_date_entry.get()), font=("Helvetica", 14))
    add_cert_button.pack(pady=10)

    cert_input_window.mainloop()

def fm_login():
    def create_fmuser():
        def create_user():
            username = username_entry.get()
            password = password_entry.get()
            privileges = privileges_var.get()

            try:
                # Create the user
                cursor.execute(f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'")

                # Grant privileges to the user
                cursor.execute(f"GRANT {privileges} ON your_database.* TO '{username}'@'localhost'")

                # Flush privileges to apply changes
                cursor.execute("FLUSH PRIVILEGES")

                messagebox.showinfo("Success", f"User '{username}' created with privileges: {privileges}")
                ins_fund()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error creating user: {err}")
        window = tk.Tk()
        window.title("Create User")
        username_label = tk.Label(window, text="Username:", font=("Helvetica", 12))
        username_label.pack(pady=5)
        username_entry = tk.Entry(window, font=("Helvetica", 12))
        username_entry.pack(pady=5)

        password_label = tk.Label(window, text="Password:", font=("Helvetica", 12))
        password_label.pack(pady=5)
        password_entry = tk.Entry(window, show="*", font=("Helvetica", 12))
        password_entry.pack(pady=5)

        privileges_label = tk.Label(window, text="Privileges:", font=("Helvetica", 12))
        privileges_label.pack(pady=5)

        privileges_var = tk.StringVar()
        privileges_var.set("SELECT, INSERT, UPDATE, DELETE")  # Default privileges

        # Create a dropdown menu for privileges
        privileges_menu = tk.OptionMenu(window, privileges_var, "SELECT, INSERT, UPDATE, DELETE", "SELECT, INSERT", "SELECT")
        privileges_menu.pack(pady=10)
        # Create a button to create the user
        create_user_button = tk.Button(window, text="Create User", command=create_user, font=("Helvetica", 12))
        create_user_button.pack(pady=10)
        window.mainloop()
        
        
    def ins_fund():
        def fund_create():
            fm_id=int(fmid_entry.get())
            f_id = fid_entry.get()
            acl = acl_entry.get()
            fsz = fsz_entry.get()
            rpa = rpa_entry.get()
            fb = fb_entry.get()
            try:
                cursor.execute("INSERT INTO fund_manager (fm_id, amc_id) VALUES (%s, %s)",
                    (fm_id, current_amc_id))
                db.commit()
            #messagebox.showinfo("Success", "Fund Manager record added!")
            except mysql.connector.IntegrityError as e:
                if e.errno == 1062:  # MySQL error code for duplicate entry
                    messagebox.showerror("Error", "Fund ID already exists. The record was not added to the Fund Manager table.")
                
                    cursor.execute("INSERT INTO fund (fund_id, asset_class,fund_size,return_pa,fund_balance,manages_id) VALUES (%s, %s,%s, %s,%s, %s)",
                    (f_id,acl,fsz,rpa,fb, fm_id))
                    db.commit()
                    messagebox.showinfo("Success", "Fund record added!")
            else:
                cursor.execute("INSERT INTO fund (fund_id, asset_class,fund_size,return_pa,fund_balance,manages_id) VALUES (%s, %s,%s, %s,%s, %s)",
                    (f_id,acl,fsz,rpa,fb, fm_id))
                db.commit()
                messagebox.showinfo("Success", "Fund record added!")
        fm_window = tk.Tk()
        fm_window.title("Add Customer Account")
        fmid_label = tk.Label(fm_window, text="FM Id", font=("Helvetica", 12))
        fmid_label.pack(pady=5)
        fmid_entry = tk.Entry(fm_window, font=("Helvetica", 12))
        fmid_entry.pack(pady=5)

        fid_label = tk.Label(fm_window, text="Fund Id", font=("Helvetica", 12))
        fid_label.pack(pady=5)
        fid_entry = tk.Entry(fm_window, font=("Helvetica", 12))
        fid_entry.pack(pady=5)

        acl_label = tk.Label(fm_window, text="Asset Class", font=("Helvetica", 12))
        acl_label.pack(pady=5)
        acl_entry = tk.Entry(fm_window, font=("Helvetica", 12))
        acl_entry.pack(pady=5)

        fsz_label = tk.Label(fm_window, text="Fund Size", font=("Helvetica", 12))
        fsz_label.pack(pady=5)
        fsz_entry = tk.Entry(fm_window, font=("Helvetica", 12))
        fsz_entry.pack(pady=5)

        rpa_label = tk.Label(fm_window, text="Return PA", font=("Helvetica", 12))
        rpa_label.pack(pady=5)
        rpa_entry = tk.Entry(fm_window, font=("Helvetica", 12))
        rpa_entry.pack(pady=5)

        fb_label = tk.Label(fm_window, text="Fund Balance", font=("Helvetica", 12))
        fb_label.pack(pady=5)
        fb_entry = tk.Entry(fm_window, font=("Helvetica", 12))
        fb_entry.pack(pady=5)
        cf_button = tk.Button(fm_window, text="Create Fund ", command=fund_create, font=("Helvetica", 14))
        cf_button.pack(pady=10)
        fm_window.mainloop()
    create_fmuser()
    

def show_cust_invest():
    def make_invest():
        def insert_investment():
            invest_amt = invest_amt_entry.get()
            fund_id = fund_id_entry.get()
            cus_id = cus_id_entry.get()
            inv_id=inv_id_entry.get()
            # Generate the current date in 'yyyy-mm-dd' format
            current_date = datetime.now().strftime("%Y-%m-%d")

            # Insert data into the investment table
            cursor.execute("INSERT INTO investment (inv_id,invest_date, invest_amt, fund_id, cus_id) VALUES (%s, %s, %s, %s,%s)",
                        (inv_id,current_date, invest_amt, fund_id, cus_id))
            db.commit()
            sum_query = "SELECT SUM(invest_amt) FROM investment WHERE cus_id = %s"
            cursor.execute(sum_query, (cus_id,))
            total_investment = cursor.fetchone()[0]
            messagebox.showinfo("Success", f"Investment record added!\nTotal Investment Amount Till Now: {total_investment}")

        window = tk.Tk()
        window.title("Add Customer Investment")
        inv_id_label = tk.Label(window, text="Investment Id", font=("Helvetica", 12))
        inv_id_label.pack(pady=5)
        inv_id_entry = tk.Entry(window, font=("Helvetica", 12))
        inv_id_entry.pack(pady=5)
        invest_amt_label = tk.Label(window, text="Investment Amount", font=("Helvetica", 12))
        invest_amt_label.pack(pady=5)
        invest_amt_entry = tk.Entry(window, font=("Helvetica", 12))
        invest_amt_entry.pack(pady=5)

        fund_id_label = tk.Label(window, text="Fund ID ", font=("Helvetica", 12))
        fund_id_label.pack(pady=5)
        fund_id_entry = tk.Entry(window, font=("Helvetica", 12))
        fund_id_entry.pack(pady=5)

        cus_id_label = tk.Label(window, text="Customer ID ", font=("Helvetica", 12))
        cus_id_label.pack(pady=5)
        cus_id_entry = tk.Entry(window, font=("Helvetica", 12))
        cus_id_entry.pack(pady=5)

        insert = tk.Button(window, text="Make Investment", command=insert_investment, font=("Helvetica", 14))
        insert.pack()
        window.mainloop()
    def see():
        query = """
        SELECT f.fund_id, f.asset_class, f.fund_size, f.return_pa, f.fund_balance
        FROM fund AS f
        JOIN fund_manager AS fm ON f.manages_id = fm.fm_id
        WHERE fm.amc_id = %s
        """
        cursor.execute(query, (current_amc_id,))
        records = cursor.fetchall()
        search_res_window = tk.Tk()
        search_res_window.title("Search")
        search_result = tk.Text(search_res_window, height=10, width=50, state="disabled", font=("Helvetica", 12))
        search_result.pack(pady=10)
        if records:
            # Display the search results
            search_result.config(state="normal")
            search_result.delete(1.0, "end")
            for record in records:
                search_result.insert("end", f"Fund_id: {record[0]}, Asset_class: {record[1]}, Fund_Size: {record[2]}, Return_PA: {record[3]},Fund_Balance: {record[4]}\n")
            search_result.config(state="disabled")
        else:
            messagebox.showinfo("Search", "Bank account not found!")
        see_window.mainloop()

    see_window = tk.Tk()
    see_window.title("Search")
    see_label = tk.Label(see_window, text="View all funds of particular amc", font=("Helvetica", 12))
    see_label.pack(pady=5)
    see_button = tk.Button(see_window, text="See Funds", command=see, font=("Helvetica", 14))
    see_button.pack(pady=10)
    insert_investment_button = tk.Button(see_window, text="Insert Investment Record", command=make_invest, font=("Helvetica", 14))
    insert_investment_button.pack()
    see_window.mainloop()

def show_cust_options():
    def insert_cus_account():
        def insert_cus():
            cus_id = cid_entry.get()
            cus_name = cname_entry.get()
            cus_dob = dob_entry.get()
            cus_addr = addr_entry.get()
            cus_g = g_entry.get()
            cus_type = ctype_entry.get()
            cus_ph = ph_entry.get()

            def is_valid_date(cus_dob):
                try:
                    datetime.strptime(cus_dob, '%Y-%m-%d')
                    return True
                except ValueError:
                    return False

            def is_valid_phone(cus_ph):
                return len(cus_ph) == 10 and cus_ph.isdigit()

            if not is_valid_date(cus_dob):
                messagebox.showerror("Error", "Invalid Date of Birth format (yyyy-mm-dd)")
            elif not is_valid_phone(cus_ph):
                messagebox.showerror("Error", "Invalid Phone number (must have 10 digits)")
            else:
                dob_datetime = datetime.strptime(cus_dob, '%Y-%m-%d')
                today = datetime.now()
                age = today.year - dob_datetime.year - ((today.month, today.day) < (dob_datetime.month, dob_datetime.day))
                cursor.execute("INSERT INTO cus (cus_id,cus_dob, cus_type, cus_name,cus_addr,cus_g,cus_ph,cus_age,amc_id) VALUES (%s,%s, %s, %s,%s, %s, %s, %s,%s)",
                        (cus_id,cus_dob, cus_type, cus_name,cus_addr,cus_g,cus_ph,age,current_amc_id))
            
                db.commit()
                messagebox.showinfo("Success", "Cus record added!")
        def check_cus():
            cus_id = cid_entry.get()
            cursor.execute("SELECT * FROM cus WHERE cus_id= %s", (cus_id,))
            record = cursor.fetchone()
            #global current_amc_id
            if record:
                # cus record exists, navigate to the next page
                messagebox.showinfo("Success", "Cus record exists!")
                #global current_amc_id
                #current_cus_id = record[0]  # Get the AMC ID from the database
                #window.withdraw()  # Hide the login window
            else:
                insert_cus()
                cursor.execute("SELECT * FROM cus WHERE cus_id = %s", (cus_id,))
                record = cursor.fetchone()
                #current_amc_id = record[0]  # Get the AMC ID from the database
                #window.withdraw()
                
        check_cus()

    custadd_window = tk.Toplevel()
    custadd_window.title("Add Customer Account")

    icon_path = "images/icon.ico"  # Replace with the path to your icon file
    window.iconbitmap(icon_path)

    background_image_ca = PhotoImage(file="images/10.png")
    background_label_ca = tk.Label(custadd_window, image=background_image_ca)
    background_label_ca.place(relwidth=1, relheight=1)
    screen_width = custadd_window.winfo_screenwidth()
    screen_height = custadd_window.winfo_screenheight()
    window_width = int(screen_width)
    window_height = int(screen_height)
    custadd_window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")

    ca_frame = tk.Frame(custadd_window, pady=20, padx=20)
    ca_frame.pack(expand=True)
    ca_frame.configure(bg="#83aeca", highlightbackground="#00013b", highlightthickness=2)

    # Design the add account window
    cid_label = tk.Label(ca_frame, text="Customer Id", font=("Helvetica", 15), bg="#83aeca")
    cid_label.pack(pady=5)
    cid_entry = tk.Entry(ca_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2 )
    cid_entry.pack(pady=5)

    cname_label = tk.Label(ca_frame, text="Customer Name", font=("Helvetica", 15), bg="#83aeca")
    cname_label.pack(pady=5)
    cname_entry = tk.Entry(ca_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    cname_entry.pack(pady=5)

    dob_label = tk.Label(ca_frame, text="DOB(yyyy-mm-dd)", font=("Helvetica", 15), bg="#83aeca")
    dob_label.pack(pady=5)
    dob_entry = tk.Entry(ca_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    dob_entry.pack(pady=5)

    addr_label = tk.Label(ca_frame, text="Address", font=("Helvetica", 15), bg="#83aeca")
    addr_label.pack(pady=5)
    addr_entry = tk.Entry(ca_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    addr_entry.pack(pady=5)

    g_label = tk.Label(ca_frame, text="Gender", font=("Helvetica", 15), bg="#83aeca")
    g_label.pack(pady=5)
    g_entry = tk.Entry(ca_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    g_entry.pack(pady=5)

    ph_label = tk.Label(ca_frame, text="Phone", font=("Helvetica", 15), bg="#83aeca")
    ph_label.pack(pady=5)
    ph_entry = tk.Entry(ca_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    ph_entry.pack(pady=5)

    ctype_label = tk.Label(ca_frame, text="Customer Type", font=("Helvetica", 15), bg="#83aeca")
    ctype_label.pack(pady=5)
    ctype_entry = tk.Entry(ca_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    ctype_entry.pack(pady=5)

    add_button = tk.Button(ca_frame, text="Login", command=insert_cus_account, font=("Helvetica", 15), width=25, bg='blue', fg='white')
    add_button.pack(pady=10)

    exit_button = tk.Button(ca_frame, text="EXIT", command=custadd_window.destroy, font=labels_font, width =15, bg='red', fg='white')
    exit_button.pack(pady=10)

    custadd_window.mainloop()


def show_options_window():
    #window.withdraw()
    options_window = tk.Toplevel()
    options_window.title("Bank Account Options")

    icon_path = "images/icon.ico"  # Replace with the path to your icon file
    options_window.iconbitmap(icon_path)

    window.configure(bg="#518db5")
    background_image = PhotoImage(file="images/5.png")
    background_label = tk.Label(options_window, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Get the screen width and height
    screen_width = options_window.winfo_screenwidth()
    screen_height = options_window.winfo_screenheight()

    # Set window size and position for fullscreen and centered
    window_width = int(screen_width)
    window_height = int(screen_height)
    options_window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")

    # Create a frame to contain all widgets
    o_frame = tk.Frame(options_window, pady=20, padx=20)
    o_frame.pack(expand=True)
    o_frame.configure(bg="#83aeca", highlightbackground="#00013b", highlightthickness=2)

    # Design the options window
    label = tk.Label(o_frame, text="CHOOSE AN OPTION", font=("Helvetica", 16), bg="#83aeca")
    label.pack(pady=20)

    search_button = tk.Button(o_frame, text="Search Bank Account", command=search_bank_account, font=("Helvetica", 14), width =25, bg='blue', fg='white')
    search_button.pack(pady=10)

    view_button = tk.Button(o_frame, text="View Bank Accounts", command=view_bank_accounts, font=("Helvetica", 14), width =25, bg='blue', fg='white')
    view_button.pack(pady=10)

    add_button = tk.Button(o_frame, text="Add Bank Account", command=add_bank_account, font=("Helvetica", 14), width =25, bg='blue', fg='white')
    add_button.pack(pady=10)

    exit_button = tk.Button(o_frame, text="EXIT", command=options_window.destroy, font=labels_font, width =15, bg='red', fg='white')
    exit_button.pack(pady=10)

    options_window.mainloop()

def search_bank_account():
    def search():
        account_no_to_search = search_entry.get()
        cursor.execute("SELECT * FROM bank WHERE account_no = %s", (account_no_to_search,))
        records = cursor.fetchall()
        search_res_window = tk.Tk()
        search_res_window.title("Search")
        search_result = tk.Text(search_res_window, height=20, width=100, state="disabled", font=("Helvetica", 15))
        search_result.pack(pady=10)
        if records:
            # Display the search results
            search_result.config(state="normal")
            search_result.delete(1.0, "end")
            for record in records:
                search_result.insert("end", f"IFSC: {record[0]}, Bank: {record[1]}, Account No: {record[2]}, Balance: {record[3]}\n")
            search_result.config(state="disabled")
        else:
            messagebox.showinfo("Search", "Bank account not found!")
        search_window.mainloop()

    search_window = tk.Toplevel()
    search_window.title("Search Bank Account")

    icon_path = "images/icon.ico"  # Replace with the path to your icon file
    search_window.iconbitmap(icon_path)

    background_image_sw = PhotoImage(file="images/5.png")
    background_label_sw = tk.Label(search_window, image=background_image_sw)
    background_label_sw.place(relwidth=1, relheight=1)
    screen_width = search_window.winfo_screenwidth()
    screen_height = search_window.winfo_screenheight()
    window_width = int(screen_width)
    window_height = int(screen_height)
    search_window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")

    s_frame = tk.Frame(search_window, pady=20, padx=20)
    s_frame.pack(expand=True)
    s_frame.configure(bg="#83aeca", highlightbackground="#00013b", highlightthickness=2)


    search_label = tk.Label(s_frame, text="Search By Account Number", font=("Helvetica", 15), bg="#83aeca")
    search_label.pack(pady=5)
    search_entry = tk.Entry(s_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    search_entry.pack(pady=5)
    search_button = tk.Button(s_frame, text="SEARCH", command=search, font=("Helvetica", 15), width=25, bg='blue', fg='white')
    search_button.pack(pady=10)
    exit_button = tk.Button(s_frame, text="EXIT", command=search_window.destroy, font=labels_font, width =15, bg='red', fg='white')
    exit_button.pack(pady=10)


def view_bank_accounts():
    cursor.execute("SELECT * FROM bank WHERE amc_id = %s", (current_amc_id,))
    records = cursor.fetchall()
    view_res_window = tk.Tk()
    view_res_window.title("View Bank Accounts")

    icon_path = "images/icon.ico"  # Replace with the path to your icon file
    window.iconbitmap(icon_path)

    view_result = tk.Text(view_res_window, height=10, width=90, state="disabled", font=("Helvetica", 15), bg="#83aeca")
    view_result.pack(pady=10)

    if records:
        # Display the bank accounts
        view_result.config(state="normal")
        view_result.delete(1.0, "end")
        for record in records:
            view_result.insert("end", f"IFSC: {record[0]}, Bank: {record[1]}, Account No: {record[2]}, Balance: {record[3]}\n")
        view_result.config(state="disabled")
    else:
        messagebox.showinfo("View Bank Accounts", "No bank accounts found for this AMC!")


def add_bank_account():
    def insert_bank_account():
        ifsc_code = ifsc_entry.get()
        bank_name = bank_name_entry.get()
        acc_no = acc_no_entry.get()
        balance_amount = int(balance_entry.get())
        
        cursor.execute("INSERT INTO bank (ifsc_code, bank_name, account_no, balance_amount, amc_id) VALUES (%s, %s, %s, %s, %s)",
                    (ifsc_code, bank_name, acc_no, balance_amount, current_amc_id))
        
        db.commit()
        messagebox.showinfo("Success", "Bank account added!")

    add_account_window = tk.Toplevel()
    add_account_window.title("Add Bank Account")

    background_image = PhotoImage(file="images/7.png")
    background_label = tk.Label(add_account_window, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    screen_width = add_account_window.winfo_screenwidth()
    screen_height = add_account_window.winfo_screenheight()
    window_width = int(screen_width)
    window_height = int(screen_height)
    add_account_window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")

    aa_frame = tk.Frame(add_account_window, pady=20, padx=20)
    aa_frame.pack(expand=True)
    aa_frame.configure(bg="#83aeca", highlightbackground="#00013b", highlightthickness=2)

    # Design the add account window
    acc_no_label = tk.Label(aa_frame, text="Account Number", font=("Helvetica", 15), bg="#83aeca")
    acc_no_label.pack(pady=5)
    acc_no_entry = tk.Entry(aa_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    acc_no_entry.pack(pady=5)

    ifsc_label = tk.Label(aa_frame, text="IFSC Code", font=("Helvetica", 15), bg="#83aeca")
    ifsc_label.pack(pady=5)
    ifsc_entry = tk.Entry(aa_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    ifsc_entry.pack(pady=5)

    bank_name_label = tk.Label(aa_frame, text="Bank Name", font=("Helvetica", 15), bg="#83aeca")
    bank_name_label.pack(pady=5)
    bank_name_entry = tk.Entry(aa_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    bank_name_entry.pack(pady=5)

    balance_label = tk.Label(aa_frame, text="Balance Amount", font=("Helvetica", 15), bg="#83aeca")
    balance_label.pack(pady=5)
    balance_entry = tk.Entry(aa_frame, font=("Helvetica", 15), width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
    balance_entry.pack(pady=5)

    add_button = tk.Button(aa_frame, text="ADD ACCOUNT", command=insert_bank_account, font=("Helvetica", 15), width=25, bg='blue', fg='white')
    add_button.pack(pady=10)

    exit_button = tk.Button(aa_frame, text="EXIT", command=add_account_window.destroy, font=labels_font, width =15, bg='red', fg='white')
    exit_button.pack(pady=10)

    add_account_window.mainloop()
    

def exit_application():
    window.destroy()  # Close the window and terminate the application


# Create the Tkinter window
splash_window = tk.Tk()
splash_window.title("WealthWise Database Management System")

icon_path = "images/icon.ico"  # Replace with the path to your icon file
splash_window.iconbitmap(icon_path)

background_image = PhotoImage(file="images/wealth2.png")
background_label = tk.Label(splash_window, image=background_image)
background_label.place(relwidth=1, relheight=1)

screen_width = splash_window.winfo_screenwidth()
screen_height = splash_window.winfo_screenheight()


# Set window size and position for fullscreen and centered
window_width = int(screen_width )
window_height = int(screen_height)
splash_window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")

# Schedule the window to close after 10 seconds
def destroy_splash():
    splash_window.destroy()

splash_window.after(100, destroy_splash)
splash_window.mainloop()

# Create the main window
window = tk.Tk()
window.title("WealthWise - AMC Authentication Window")
#window.attributes("-alpha", 0.80)

icon_path = "images/icon.ico"  # Replace with the path to your icon file
window.iconbitmap(icon_path)

window.configure(bg="#518db5")
background_image = PhotoImage(file="images/wealth4.png")
background_label = tk.Label(window, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

print(screen_width, screen_height)

# Set window size and position for fullscreen and centered
window_width = int(screen_width )
window_height = int(screen_height)
window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width)/2)}+{int((screen_height - window_height)/2)}")

# Create labels and entry fields for ID, Address, Type, and AMC Name
labels_font = ("Helvetica", 15)
entry_font = ("Helvetica", 15)
label_bg_color = "#83aeca"  
border_color = "#054a77"

# Create a frame to contain all widgets
frame = tk.Frame(window, pady=20, padx=20)
frame.pack(expand=True)
frame.configure(bg="#83aeca", highlightbackground="#00013b", highlightthickness=2)

amc_id_label = tk.Label(frame, text="AMC ID", font=labels_font, bg=label_bg_color)
amc_id_label.grid(row=0, column=0, padx=10, pady=10)

amc_id_entry = tk.Entry(frame, font=entry_font, width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
amc_id_entry.grid(row=0, column=1, padx=10, pady=10)

address_label = tk.Label(frame, text="Company Address", font=labels_font, bg=label_bg_color)
address_label.grid(row=1, column=0, padx=10, pady=10)

address_entry = tk.Text(frame, font=entry_font, wrap=tk.WORD, height=4, width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
address_entry.grid(row=1, column=1, padx=10, pady=10)

type_label = tk.Label(frame, text="AMC Type", font=labels_font, bg=label_bg_color)
type_label.grid(row=2, column=0, padx=5, pady=5)

type_entry = tk.Entry(frame, font=entry_font, width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
type_entry.grid(row=2, column=1, padx=5, pady=5)

amc_name_label = tk.Label(frame, text="AMC Name", font=labels_font, bg=label_bg_color)
amc_name_label.grid(row=3, column=0, padx=10, pady=10)

amc_name_entry = tk.Entry(frame, font=entry_font, width=30, **{'border': 3, 'relief': 'flat'}, highlightbackground="#054a77", highlightthickness=2)
amc_name_entry.grid(row=3, column=1, padx=10, pady=10)


space_frame = tk.Frame(frame, height=30, bg="#83aeca")
space_frame.grid(row=4, column=0, columnspan=2 )

# Create a login button
login_button = tk.Button(frame, text="LOGIN / REGISTER", command=check_amc, font=labels_font, width=25, bg='blue', fg='white')
login_button.grid(row=5, column=0, columnspan=2, pady=10)


#Exit Button for application termination
exit_button = tk.Button(frame, text="EXIT", command=exit_application, font=labels_font, width =15, bg='red', fg='white')
exit_button.grid(row=6, column=0, columnspan=2, pady=10)


# Start the Tkinter main loop
window.mainloop()