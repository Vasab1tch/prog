import csv

class Worker:
    def __init__(self, id, name, salary):
        self.__id = id  
        self.name = name
        self.salary = salary
    def get_id(self):
        return self.__id
    def set_id(self, new_id):
        self.__id = new_id
    def search_by_name(self, name):
        return self.name == name
    def search_by_salary(self, salary):
        return self.salary == salary
    def __str__(self):
        return f"ID: {self.__id}, Name: {self.name}, Salary: {self.salary}"
    def __repr__(self):
        return self.__str__()

class WorkerDatabase:
    def __init__(self, file_name):
        self.file_name = file_name
        self.container = self.load_data()
        self.next_id = max([worker.get_id() for worker in self.container]) + 1 if self.container else 1        
    def load_data(self):
        container = []
        with open(self.file_name, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = int(row['id'])
                name = row['name']
                salary = float(row['salary'])
                worker = Worker(id, name, salary)
                container.append(worker)
        return container
    def save_data(self):
        with open(self.file_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'salary'])
            writer.writeheader()
            for worker in self.container:
                writer.writerow({'id': worker.get_id(), 'name': worker.name, 'salary': worker.salary})
    def add_worker(self, name, salary):
        worker = Worker(self.next_id, name, salary)
        self.container.append(worker)
        self.save_data()
        self.next_id += 1
    def remove_worker(self, worker):
        self.container.remove(worker)
        self.save_data()
    def update_worker(self, old_id, new_name, new_salary):
        for worker in self.container:
            if worker.get_id() == old_id:
                worker.name = new_name
                worker.salary = new_salary
                self.save_data()
                return
        print(f"Worker with id {old_id} not found.")
a=WorkerDatabase("file.csv")
print(a.container)

a.add_worker("boba",1000)
print(a.container)