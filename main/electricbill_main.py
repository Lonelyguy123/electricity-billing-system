import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class ElectricityBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Electricity Billing System v1.1.1")
        self.root.geometry("800x600")
        
        # Database connection
        self.conn = self.create_database_connection()
        
        # Main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Variables for bill calculation
        self.name_var = tk.StringVar()
        self.appliance_count_var = tk.StringVar()
        self.monyear_var = tk.StringVar()
        self.appliances = []
        
        self.create_main_menu()
        
    def create_database_connection(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user="Shastha",
                password="idkbro",
                database="electricbill"
            )
            return conn
        except Error:
            try:
                # First connect without selecting a database
                conn = mysql.connector.connect(
                    host='localhost',
                    user="Shastha",
                    password="idkbro"
                )
                
                if conn.is_connected():
                    cursor = conn.cursor()
                    cursor.execute("CREATE DATABASE IF NOT EXISTS electricbill")
                    cursor.execute("USE electricbill")
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS electricbill (
                            name varchar(30), 
                            monyear varchar(30),
                            pu integer,
                            tamount integer
                        );
                    """)
                    return conn
            except Error as e:
                messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
                return None
    
    def create_main_menu(self):
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Title
        title_label = ttk.Label(self.main_frame, text="Electricity Billing System", font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Menu buttons
        buttons = [
            ("Calculate New Bill", self.show_bill_calculator),
            ("View Previous Bill", self.show_bill_finder),
            ("View All Previous Bills", self.show_all_bills),
            ("Common Appliances", self.show_common_appliances),
            ("Software Information", self.show_software_info)
        ]
        
        for idx, (text, command) in enumerate(buttons, start=1):
            btn = ttk.Button(self.main_frame, text=text, command=command)
            btn.grid(row=idx, column=0, columnspan=2, pady=5, padx=20, sticky="ew")
    
    def show_bill_calculator(self):
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Bill calculator form
        ttk.Label(self.main_frame, text="Calculate Electricity Bill", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Name input
        ttk.Label(self.main_frame, text="Name:").grid(row=1, column=0, pady=5, padx=5)
        name_entry = ttk.Entry(self.main_frame, textvariable=self.name_var)
        name_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Month-Year input
        ttk.Label(self.main_frame, text="Month-Year (MM-YYYY):").grid(row=2, column=0, pady=5, padx=5)
        monyear_entry = ttk.Entry(self.main_frame, textvariable=self.monyear_var)
        monyear_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Number of appliances
        ttk.Label(self.main_frame, text="Number of Appliances:").grid(row=3, column=0, pady=5, padx=5)
        appliance_entry = ttk.Entry(self.main_frame, textvariable=self.appliance_count_var)
        appliance_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Button to proceed with appliance details
        ttk.Button(self.main_frame, text="Enter Appliance Details", 
                  command=self.show_appliance_details).grid(row=4, column=0, columnspan=2, pady=20)
        
        # Back button
        ttk.Button(self.main_frame, text="Back to Main Menu", 
                  command=self.create_main_menu).grid(row=5, column=0, columnspan=2, pady=5)
    
    def show_appliance_details(self):
        try:
            n = int(self.appliance_count_var.get())
            if n <= 0:
                messagebox.showerror("Error", "Please enter a positive number of appliances")
                return
                
            # Create new window for appliance details
            appliance_window = tk.Toplevel(self.root)
            appliance_window.title("Appliance Details")
            appliance_window.geometry("400x600")
            
            # Create a canvas with scrollbar
            canvas = tk.Canvas(appliance_window)
            scrollbar = ttk.Scrollbar(appliance_window, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            self.appliances = []
            
            # Create entry fields for each appliance
            for i in range(n):
                ttk.Label(scrollable_frame, text=f"Appliance {i+1}").grid(row=i*2, column=0, pady=5)
                
                power_frame = ttk.Frame(scrollable_frame)
                power_frame.grid(row=i*2+1, column=0, pady=5)
                
                power_var = tk.StringVar()
                time_var = tk.StringVar()
                
                ttk.Label(power_frame, text="Power Rating (W):").pack(side=tk.LEFT)
                ttk.Entry(power_frame, textvariable=power_var).pack(side=tk.LEFT, padx=5)
                
                ttk.Label(power_frame, text="Usage (hours):").pack(side=tk.LEFT)
                ttk.Entry(power_frame, textvariable=time_var).pack(side=tk.LEFT, padx=5)
                
                self.appliances.append((power_var, time_var))
            
            # Calculate button
            ttk.Button(scrollable_frame, text="Calculate Bill", 
                      command=lambda: self.calculate_bill(appliance_window)).grid(row=n*2, column=0, pady=20)
            
            # Pack the canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of appliances")
    
    def calculate_bill(self, appliance_window):
        try:
            pu = 0.0
            
            # Calculate total power usage
            for power_var, time_var in self.appliances:
                power = float(power_var.get())
                time = float(time_var.get())
                pu += (power * time / 1000)
            
            # Calculate amount based on usage
            if pu <= 100:
                amount = pu * 4.22
            elif pu <= 200:
                amount = (100 * 4.22) + (pu - 100) * 5.02
            else:
                amount = (100 * 4.22) + (100 * 5.02) + (pu - 200) * 5.87
            
            # Add fixed charge and energy duty
            tamount = amount + 40 + (pu * 0.15)
            
            # Save to database
            cursor = self.conn.cursor()
            sql = """INSERT INTO electricbill (name, monyear, pu, tamount) 
                    VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (self.name_var.get(), self.monyear_var.get(), pu, tamount))
            self.conn.commit()
            
            # Show result
            appliance_window.destroy()
            messagebox.showinfo("Bill Calculation", 
                              f"Total Power Usage: {pu:.2f} KWh\n"
                              f"Base Amount: ₹{amount:.2f}\n"
                              f"Fixed Charge: ₹40.00\n"
                              f"Energy Duty: ₹{pu*0.15:.2f}\n"
                              f"Total Amount: ₹{tamount:.2f}")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error saving bill: {e}")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for power rating and usage time")
    
    def show_bill_finder(self):
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        ttk.Label(self.main_frame, text="Find Previous Bill", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Name input
        ttk.Label(self.main_frame, text="Name:").grid(row=1, column=0, pady=5, padx=5)
        name_entry = ttk.Entry(self.main_frame)
        name_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Month-Year input
        ttk.Label(self.main_frame, text="Month-Year (MM-YYYY):").grid(row=2, column=0, pady=5, padx=5)
        monyear_entry = ttk.Entry(self.main_frame)
        monyear_entry.grid(row=2, column=1, pady=5, padx=5)
        
        def find_bill():
            try:
                cursor = self.conn.cursor()
                sql = """SELECT * FROM electricbill 
                        WHERE name = %s AND monyear = %s"""
                cursor.execute(sql, (name_entry.get(), monyear_entry.get()))
                result = cursor.fetchone()
                
                if result:
                    messagebox.showinfo("Bill Details",
                                      f"Name: {result[0]}\n"
                                      f"Month-Year: {result[1]}\n"
                                      f"Power Usage: {result[2]} KWh\n"
                                      f"Total Amount: ₹{result[3]}")
                else:
                    messagebox.showinfo("Not Found", "No bill found for the specified details")
                    
            except Error as e:
                messagebox.showerror("Database Error", f"Error finding bill: {e}")
        
        ttk.Button(self.main_frame, text="Find Bill", 
                  command=find_bill).grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(self.main_frame, text="Back to Main Menu", 
                  command=self.create_main_menu).grid(row=4, column=0, columnspan=2, pady=5)
    
    def show_all_bills(self):
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        ttk.Label(self.main_frame, text="View All Bills", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Name input
        ttk.Label(self.main_frame, text="Name:").grid(row=1, column=0, pady=5, padx=5)
        name_entry = ttk.Entry(self.main_frame)
        name_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Treeview for bills
        tree = ttk.Treeview(self.main_frame, columns=('Month-Year', 'Usage', 'Amount'), show='headings')
        tree.heading('Month-Year', text='Month-Year')
        tree.heading('Usage', text='Usage (KWh)')
        tree.heading('Amount', text='Amount (₹)')
        tree.grid(row=2, column=0, columnspan=2, pady=10, padx=5)
        
        def find_all_bills():
            for item in tree.get_children():
                tree.delete(item)
                
            try:
                cursor = self.conn.cursor()
                sql = "SELECT * FROM electricbill WHERE name = %s"
                cursor.execute(sql, (name_entry.get(),))
                results = cursor.fetchall()
                
                if results:
                    for row in results:
                        tree.insert('', 'end', values=(row[1], row[2], row[3]))
                else:
                    messagebox.showinfo("Not Found", "No bills found for the specified name")
                    
            except Error as e:
                messagebox.showerror("Database Error", f"Error finding bills: {e}")
        
        ttk.Button(self.main_frame, text="Find Bills", 
                  command=find_all_bills).grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.main_frame, text="Back to Main Menu", 
                  command=self.create_main_menu).grid(row=4, column=0, columnspan=2, pady=5)
    
    def show_common_appliances(self):
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        ttk.Label(self.main_frame, text="Common Appliances", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, pady=20)
        
        # Create Treeview
        tree = ttk.Treeview(self.main_frame, columns=('Appliance', 'Min', 'Max', 'Standby'), show='headings')
        tree.heading('Appliance', text='Appliance')
        tree.heading('Min', text='Min (W)')
        tree.heading('Max', text='Max (W)')
        tree.heading('Standby', text='Standby (W)')
        
        # Add data
        appliances = [
            ('32 Inch LED TV', '20', '60', '1'),
            ('Refrigerator', '100', '200', 'N/A'),
            ('Washing Machine', '500', '500', '1'),
            ('100W light bulb (Incandescent)', '100', '100', '0'),
            ('Electric Pressure Cooker', '1000', '1000', 'N/A'),
            ('Inverter Air conditioner', '1300', '1800', 'N/A'),
            ('Iron', '1000', '1000', 'N/A'),
            ('Laptop Computer', '50', '100', 'N/A'),
            ('LED Light Bulb', '7', '10', '0'),
            ('Pedestal Fan', '50', '60', 'N/A')
        ]
        
        for appliance in appliances:
            tree.insert('', 'end', values=appliance)
            
        tree.grid(row=1, column=0, pady=10, padx=10, sticky='nsew')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Back button
        ttk.Button(self.main_frame, text="Back to Main Menu", 
                  command=self.create_main_menu).grid(row=2, column=0, pady=20)
    
    def show_software_info(self):
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Title
        ttk.Label(self.main_frame, text="Software Information", 
                 font=('Helvetica', 14, 'bold')).grid(row=0, column=0, pady=20)
        
        # Info text
        info_text = """
Version: 1.1.1
Latest Patch: 17/2/2022
Python version: 3.9
MySQL Version: 8.0.28

v1.1.1 Patch Notes:
- Converted to GUI application
- Added monthly billing instead of billing by date
- Added automatic database creation
- Improved user interface and experience
- Added scrollable views for multiple appliances
- Enhanced error handling and validation
        """
        
        info_label = ttk.Label(self.main_frame, text=info_text, justify=tk.LEFT)
        info_label.grid(row=1, column=0, pady=10, padx=20)
        
        # Back button
        ttk.Button(self.main_frame, text="Back to Main Menu", 
                  command=self.create_main_menu).grid(row=2, column=0, pady=20)

def main():
    root = tk.Tk()
    app = ElectricityBillingSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()