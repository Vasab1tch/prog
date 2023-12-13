import csv
import tkinter as tk
from tkinter import simpledialog, messagebox
import pandas
import matplotlib.pyplot as plt


def decsort(funk):
    def inal(self, name):
        print("sorted by: ", name)
        return funk(self, name)

    return inal


def decsearch(funk):
    def inal(self, key, name):
        print("searched", name, " by: ", key)
        return funk(self, key, name)

    return inal


class Worker:
    def __init__(self, id, name, salary):
        self.__id = id
        self.name = name
        self.salary = salary

    def get_id(self):
        return self.__id

    def set_id(self, new_id):
        self.__id = new_id

    def __str__(self):
        return f"ID: {self.__id}, Name: {self.name}, Salary: {self.salary}"

    def __repr__(self):
        return self.__str__()

    def __getattribute__(self, name):
        try:
            a = super().__getattribute__(name)
        except AttributeError:
            return None
        return super().__getattribute__(name)

    def __eq__(self, other):
        if isinstance(other, Worker):
            return (
                    self.get_id() == other.get_id() and
                    self.name == other.name and
                    self.salary == other.salary
            )
        return False


class DeliveryWorker(Worker):
    def __init__(self, id, name, salary, duty):
        super().__init__(id, name, salary)
        self.duty = duty

    def __str__(self):
        return f"ID: {self.get_id()}, Name: {self.name}, Salary: {self.salary}, Duty: {self.duty}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, DeliveryWorker):
            return (
                    super().__eq__(other) and
                    self.duty == other.duty
            )
        return False


class NonDeliveryWorker(Worker):
    def __init__(self, id, name, salary, responsibility):
        super().__init__(id, name, salary)
        self.responsibility = responsibility

    def __str__(self):
        return f"ID: {self.get_id()}, Name: {self.name}, Salary: {self.salary}, responsibility: {self.responsibility}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, NonDeliveryWorker):
            return (
                    super().__eq__(other) and
                    self.responsibility == other.responsibility
            )
        return False


class WorkerDatabase:
    def __init__(self, file_name):
        self.file_name = file_name
        self.container = self.load_data()
        self.next_id = self.get_next_id()

    def get_next_id(self):
        val = max([worker.get_id() for worker in self.container])
        while True:
            val += 1
            yield val

    def load_data(self):
        container = []
        with open(self.file_name, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = int(row['id'])
                name = row['name']
                salary = float(row['salary'])
                duty = row.get('duty')
                responsibility = row.get('responsibility')

                if duty != '':
                    worker = DeliveryWorker(id, name, salary, duty)
                elif responsibility != '':
                    worker = NonDeliveryWorker(id, name, salary, responsibility)
                else:
                    worker = Worker(id, name, salary)

                container.append(worker)
        return container

    def save_data(self):
        with open(self.file_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'salary', 'duty', 'responsibility'])
            writer.writeheader()
            for worker in self.container:
                if isinstance(worker, DeliveryWorker):
                    writer.writerow(
                        {'id': worker.get_id(), 'name': worker.name, 'salary': worker.salary, 'duty': worker.duty,
                         'responsibility': ''})
                elif isinstance(worker, NonDeliveryWorker):
                    writer.writerow({'id': worker.get_id(), 'name': worker.name, 'salary': worker.salary, 'duty': '',
                                     'responsibility': worker.responsibility})
                else:
                    writer.writerow({'id': worker.get_id(), 'name': worker.name, 'salary': worker.salary, 'duty': '',
                                     'responsibility': ''})

    def add_worker(self, name, salary, duty=None, responsibility=None):
        if duty is not None:
            worker = DeliveryWorker(next(self.next_id), name, salary, duty)
        elif responsibility is not None:
            worker = NonDeliveryWorker(next(self.next_id), name, salary, responsibility)
        else:
            worker = Worker(next(self.next_id), name, salary)

        self.container.append(worker)
        self.save_data()

    def remove_worker(self, worker):
        self.container.remove(worker)
        self.save_data()

    def update_worker(self, old_id, new_name, new_salary, duty=None, responsibility=None):
        for worker in self.container:
            if worker.get_id() == old_id:
                if duty is not None:
                    worker.name = new_name
                    worker.salary = new_salary
                    worker.duty = duty
                elif responsibility is not None:
                    worker.name = new_name
                    worker.salary = new_salary
                    worker.responsibility = responsibility
                else:
                    worker.name = new_name
                    worker.salary = new_salary
                self.save_data()
                return
        print(f"Worker with id {old_id} not found.")

    @decsort
    def sort_by(self, name):
        if all(element.__getattribute__(name) == None for element in self.container):
            print("no name like this")
            return None
        data = []
        for element in self.container:
            if element.__getattribute__(name) != None:
                data.append(element)
        return sorted(data, key=lambda x: x.__getattribute__(name))

    @decsearch
    def search(self, key, name1):
        container = []
        with open(self.file_name, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if str(name1) in row[key]:
                    id = int(row['id'])
                    name = row['name']
                    salary = float(row['salary'])
                    duty = row.get('duty')
                    responsibility = row.get('responsibility')

                    if duty != '':
                        worker = DeliveryWorker(id, name, salary, duty)
                    elif responsibility != '':
                        worker = NonDeliveryWorker(id, name, salary, responsibility)
                    else:
                        worker = Worker(id, name, salary)
                    container.append(worker)
        return container

    def salary_graph(self):
        df = pandas.read_csv(self.file_name)
        salarys = [0, 1000, 2000, 10000, 20000, 100000]
        df["salary_category"] = pandas.cut(df["salary"], salarys)
        salary_cat_count = df["salary_category"].value_counts()
        plt.figure(figsize=(8, 8))
        salary_cat_count.plot.pie(autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.3))
        plt.title('Distribution of Salaries')
        plt.ylabel('')
        plt.show()

class WorkerDatabaseGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Worker Database GUI")

        self.worker_db = WorkerDatabase("file.csv")


        # Worker type selection
        self.worker_type_var = tk.StringVar()
        self.worker_type_var.set("Worker")  # Default to Worker type
        self.worker_type_menu = tk.OptionMenu(master, self.worker_type_var, "Worker", "DeliveryWorker", "NonDeliveryWorker")
        self.worker_type_menu.grid(row=2, column=1, padx=10, pady=5)

        # Labels
        tk.Label(master, text="Worker Type:").grid(row=2, column=0, padx=10, pady=5)

        # Buttons
        tk.Button(master, text="Add Worker", command=self.add_worker).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(master, text="Remove Worker", command=self.remove_worker).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(master, text="Update Worker", command=self.update_worker).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(master, text="Sort Workers", command=self.sort_workers).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(master, text="Search Workers", command=self.search_workers).grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(master, text="Show Salary Distribution", command=self.show_salary_distribution).grid(row=8, column=0, columnspan=2, pady=10)

    def add_worker(self):
        name = simpledialog.askstring("Input", "Enter name:")
        salary = simpledialog.askfloat("Input", "Enter salary:")
        worker_type = self.worker_type_var.get()

        if worker_type == "Worker":
            self.worker_db.add_worker( name, salary)
        elif worker_type == "DeliveryWorker":
            duty = simpledialog.askstring("Input", "Enter duty for Delivery Worker:")
            self.worker_db.add_worker(name, salary, duty)
        elif worker_type == "NonDeliveryWorker":
            responsibility = simpledialog.askstring("Input", "Enter responsibility for Non-Delivery Worker:")
            self.worker_db.add_worker(name, salary, None, responsibility)
        messagebox.showinfo("Success", "Worker added successfully.")

    def remove_worker(self):
        ID = simpledialog.askinteger("Input", "Enter ID:")
        result = self.worker_db.search("id",ID)
        if result:
            self.worker_db.remove_worker(result[0])
            messagebox.showinfo("Success", "Worker removed successfully.")
        else:
            messagebox.showinfo("Error", "No matching workers found for removal.")

    def update_worker(self):
        ID = simpledialog.askinteger("Input", "Enter ID")
        new_name = simpledialog.askstring("Input", "Enter new name:")
        new_salary = simpledialog.askfloat("Input", "Enter new salary:")
        worker_type = self.worker_type_var.get()
        if worker_type == "Worker":
            self.worker_db.update_worker(ID,new_name,new_salary)
        elif worker_type == "DeliveryWorker":
            duty = simpledialog.askstring("Input", "Enter duty for Delivery Worker:")
            self.worker_db.update_worker(ID,new_name,new_salary,duty)
        elif worker_type == "NonDeliveryWorker":
            responsibility = simpledialog.askstring("Input", "Enter responsibility for Non-Delivery Worker:")
            self.worker_db.update_worker(ID,name, salary, None, responsibility)
        messagebox.showinfo("Success", "Worker updated successfully.")

    def sort_workers(self):
        attribute = simpledialog.askstring("Input", "Enter attribute to sort by:")
        sorted_workers = self.worker_db.sort_by(attribute)
        self.show_result(sorted_workers, "Sorted Workers")

    def search_workers(self):
        attribute = simpledialog.askstring("Input", "Enter attribute to search by:")
        value = simpledialog.askstring("Input", f"Enter value for {attribute}:")
        result = self.worker_db.search(attribute, value)
        self.show_result(result, "Search Result")

    def show_result(self, result, title):
        if result:
            result_str = "\n".join(str(worker) for worker in result)
            messagebox.showinfo(title, result_str)
        else:
            messagebox.showinfo(title, "No matching workers found.")
    def show_salary_distribution(self):
        self.worker_db.salary_graph()

root = tk.Tk()
app = WorkerDatabaseGUI(root)
root.mainloop()
