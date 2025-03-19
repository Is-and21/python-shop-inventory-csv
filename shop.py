import csv
from tabulate import tabulate

class Shop:
    def __init__(self):
        self.inv = {}  
        self.inv_file = "inventory.csv" 
        self.sales_file = "sales.csv"  
        try:
            with open(self.inv_file, newline='') as f:
                for row in csv.reader(f):
                    if row:
                        self.inv[row[0]] = [row[1], float(row[2]), int(row[3])]
        except FileNotFoundError:
            open(self.inv_file, 'w').close()

    def save(self):
        with open(self.inv_file, 'w', newline='') as f:
            csv.writer(f).writerows([[k, *v] for k, v in self.inv.items()])

    def menu(self):
        while (c := input("\n1. View Inventory\n2. Add Product\n3. Process Sale\n4. View Sales\n5. Exit\nChoice: ")) != "5":
            {"1": self.view, "2": self.add, "3": self.sale, "4": self.report}.get(c, lambda: print("Invalid"))()
    
    def view(self):
        print(tabulate([[k, *v] for k, v in self.inv.items()], headers=["ID", "Name", "Price", "Stock"], tablefmt="grid"))
    
    def add(self):
        self.inv[input("ID: ")] = [input("Name: "), float(input("Price: ")), int(input("Stock: "))]
        self.save()
    
    def sale(self):
        sid, items = input("Sale ID: "), []
        while (pid := input("Product ID (or 'done'): ")) != "done":
            if pid in self.inv and (qty := int(input(f"Quantity for {self.inv[pid][0]}: "))) <= self.inv[pid][2]:
                self.inv[pid][2] -= qty; items.append([pid, self.inv[pid][0], qty, self.inv[pid][1]])
            else: print("Invalid/Insufficient stock!")
        with open(self.sales_file, 'a', newline='') as f:
            csv.writer(f).writerows([[sid, *i, i[1] * i[2]] for i in items])
        self.save()
    
    def report(self):
        try:
            with open(self.sales_file, newline='') as f:
                print(tabulate([row for row in csv.reader(f)], headers=["Sale ID", "Product ID", "Name", "Quantity", "Total"], tablefmt="grid"))
        except FileNotFoundError:
            print("No sales recorded.")

if __name__ == "__main__":
    Shop().menu()

INVENTORY.CSV
101,Soap,20.5,50
102,Shampoo,100.0,30
103,Toothpaste,50.0,25

pip install tabulate 

SALES.CSV
1001,101,Soap,3,61.5
1001,102,Shampoo,1,100.0
1002,103,Toothpaste,2,100.0
