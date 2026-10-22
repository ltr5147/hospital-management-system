class Patient:
    def __init__(self, name, urgency):
        if type(urgency) is not int or not 1 <= urgency <= 10:
            raise ValueError(
                "Urgency must be an integer from 1 to 10."
            )

        self.name = name
        self.urgency = urgency


class MinHeap:
    def __init__(self):
        self.data = []

    def heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if self.data[index].urgency >= self.data[parent].urgency:
                break

            self.data[index], self.data[parent] = (
                self.data[parent],
                self.data[index]
            )

            index = parent

    def heapify_down(self, index):
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if (
                left < len(self.data)
                and self.data[left].urgency
                < self.data[smallest].urgency
            ):
                smallest = left

            if (
                right < len(self.data)
                and self.data[right].urgency
                < self.data[smallest].urgency
            ):
                smallest = right

            if smallest == index:
                break

            self.data[index], self.data[smallest] = (
                self.data[smallest],
                self.data[index]
            )

            index = smallest

    def insert(self, patient):
        if not isinstance(patient, Patient):
            raise TypeError("Insert a Patient object.")

        self.data.append(patient)
        self.heapify_up(len(self.data) - 1)

    def peek(self):
        if not self.data:
            return None

        return self.data[0]

    def remove_min(self):
        if not self.data:
            return None

        patient = self.data[0]
        last = self.data.pop()

        if self.data:
            self.data[0] = last
            self.heapify_down(0)

        return patient

    def print_heap(self):
        print("Current Queue:")

        if not self.data:
            print("The queue is empty.")

        for patient in self.data:
            print(f"- {patient.name} ({patient.urgency})")


def run_tests():
    heap = MinHeap()

    # Empty queue
    assert heap.peek() is None
    assert heap.remove_min() is None

    # Assignment example and non-removing peek
    heap.insert(Patient("Jordan", 3))
    heap.insert(Patient("Taylor", 1))
    heap.insert(Patient("Avery", 5))

    assert heap.peek().name == "Taylor"
    assert len(heap.data) == 3
    heap.print_heap()

    assert heap.remove_min().name == "Taylor"
    assert heap.remove_min().name == "Jordan"
    assert heap.remove_min().name == "Avery"
    assert heap.remove_min() is None

    # Reuse an emptied heap, equal priorities, and urgency boundaries
    patients = [
        ("A", 10),
        ("B", 2),
        ("C", 2),
        ("D", 1),
        ("E", 7)
    ]

    for name, urgency in patients:
        heap.insert(Patient(name, urgency))

        for index in range(1, len(heap.data)):
            parent = (index - 1) // 2
            assert (
                heap.data[parent].urgency
                <= heap.data[index].urgency
            )

    served = []

    while heap.data:
        served.append(heap.remove_min())

        for index in range(1, len(heap.data)):
            parent = (index - 1) // 2
            assert (
                heap.data[parent].urgency
                <= heap.data[index].urgency
            )

    assert [
        patient.urgency for patient in served
    ] == [1, 2, 2, 7, 10]

    assert {
        patient.name for patient in served
    } == {"A", "B", "C", "D", "E"}

    # Invalid urgency values
    for invalid in (0, 11, 2.5, "2", True):
        try:
            Patient("Invalid", invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(
                "Invalid urgency should raise ValueError."
            )

    # Invalid object passed to insert
    try:
        heap.insert("Not a patient")
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Invalid patient should raise TypeError."
        )

    print("All emergency queue tests passed.")


if __name__ == "__main__":
    run_tests()
