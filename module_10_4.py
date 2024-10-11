import queue
from threading import Thread
from random import randint
import time


class Table:
    def __init__(self, number, guest=None):
        self.number = number
        self.guest = guest


class Guest(Thread):
    def __init__(self, name):
        super(Guest, self).__init__()
        self.name = name

    def run(self):
        randon_number = randint(3, 10)
        time.sleep(randon_number)


class Cafe:
    def __init__(self, *tables):
        self.tables = tables
        self.queue = queue.Queue()
        self.guest_dict = {}

    def guest_arrival(self, *guests):
        for i in range(len(guests)):
            if not all([table.guest for table in tables]):
                for j in range(len(tables)):
                    if tables[j].guest is None:
                        tables[j].guest = guests[i].name
                        guests[i].start()
                        self.guest_dict[guests[i].name] = guests[i]
                        print(f"{guests[i].name} сел(-а) за стол номер {tables[j].number}")
                        break
            else:
                self.queue.put(guests[i])
                print(f"{guests[i].name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any([table.guest for table in tables]):
            for j in range(len(tables)):
                if tables[j].guest is not None:
                    self.guest_dict[tables[j].guest].join()
            for j in range(len(tables)):
                if tables[j].guest is not None and not self.guest_dict[tables[j].guest].is_alive():
                    print(f"{tables[j].guest} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {tables[j].number} свободен")
                    tables[j].guest = None
                    if not self.queue.empty() and not all([table.guest for table in tables]):
                        new_guest = self.queue.get()
                        self.guest_dict[new_guest.name] = new_guest
                        print(f"{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {tables[j].number}")
                        tables[j].guest = new_guest.name
                        new_guest.start()


tables = [Table(number) for number in range(1, 6)]
guests_names = ['Maria', 'Oleg', 'Vakhtang', 'Sergey',
                'Darya', 'Arman', 'Vitoria', 'Nikita',
                'Galina', 'Pavel', 'Ilya', 'Alexandra'
                ]
guests = [Guest(name) for name in guests_names]

cafe = Cafe(*tables)
cafe.guest_arrival(*guests)
cafe.discuss_guests()
