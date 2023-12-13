import unittest
from workerbase import WorkerDatabase,Worker
class Dotest(unittest.TestCase):
    def test_search(self):
        a = WorkerDatabase("file.csv")
        b = Worker(4, "adada", 2000.0)
        rez=a.search("salary", "2000.0")
        self.assertEqual(b.get_id(),4)
        self.assertEqual(b.name, "adada")
        self.assertEqual(b.salary, 2000.0)



if __name__ == '__main__':
    unittest.main()
