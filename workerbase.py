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
class DeliveryWorker(Worker):
    def __init__(self, id, name, salary, duty):
        super().__init__(id, name, salary)
        self.duty = duty
    def __str__(self):
        return f"ID: {self.get_id()}, Name: {self.name}, Salary: {self.salary}, Duty: {self.duty}"
    def __repr__(self):
        return self.__str__()
class NonDeliveryWorker(Worker):
    def __init__(self, id, name, salary, responsibility):
        super().__init__(id, name, salary)
        self.responsibility = responsibility
    def __str__(self):
        return f"ID: {self.get_id()}, Name: {self.name}, Salary: {self.salary}, responsibility: {self.responsibility}"
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
                    writer.writerow({'id': worker.get_id(), 'name': worker.name, 'salary': worker.salary, 'duty': worker.duty, 'responsibility': ''})
                elif isinstance(worker, NonDeliveryWorker):
                    writer.writerow({'id': worker.get_id(), 'name': worker.name, 'salary': worker.salary, 'duty': '', 'responsibility': worker.responsibility})
                else:
                    writer.writerow({'id': worker.get_id(), 'name': worker.name, 'salary': worker.salary, 'duty': '', 'responsibility': ''})
    def add_worker(self, name, salary, duty=None, responsibility=None):
        if duty is not None:
            worker = DeliveryWorker(self.next_id, name, salary, duty)
        elif responsibility is not None:
            worker = NonDeliveryWorker(self.next_id, name, salary, responsibility)
        else:
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