class PriorityQueue:
    def __init__(self):
        self.heap = []

    def add_request(self, request):
        self.heap.append(request)
        self._heapify_up()

    def _heapify_up(self):
        index = len(self.heap) - 1

        while index > 0:
            parent = (index - 1) // 2

            if self.heap[index]["priority"] <= self.heap[parent]["priority"]:
                break

            self.heap[index], self.heap[parent] = (
                self.heap[parent],
                self.heap[index]
            )

            index = parent

    def serve_next(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        highest_priority = self.heap[0]

        self.heap[0] = self.heap.pop()

        self._heapify_down()

        return highest_priority

    def _heapify_down(self):
        index = 0

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            if (
                left < len(self.heap)
                and self.heap[left]["priority"] > self.heap[largest]["priority"]
            ):
                largest = left

            if (
                right < len(self.heap)
                and self.heap[right]["priority"] > self.heap[largest]["priority"]
            ):
                largest = right

            if largest == index:
                break

            self.heap[index], self.heap[largest] = (
                self.heap[largest],
                self.heap[index]
            )

            index = largest

    def get_queue(self):
        return self.heap