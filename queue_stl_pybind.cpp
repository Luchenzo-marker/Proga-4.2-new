#include <deque>
#include <cstdlib>
#include <ctime>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
class Queue {
private:
    std::deque<int> container;
    static bool seeded;
public:
    Queue() = default;
    void create_queue() {
        container.clear();
    }
    bool is_empty() const {
        return container.empty();
    }
    void enqueue(int value) {
        container.push_back(value);
    }
    py::tuple dequeue() {
        if (container.empty()) {
            return py::make_tuple(0, false);
        }
        int val = container.front();
        container.pop_front();
        return py::make_tuple(val, true);
    }
    py::tuple peek() const {
        if (container.empty()) {
            return py::make_tuple(0, false);
        }
        return py::make_tuple(container.front(), true);
    }
    int size() const {
        return static_cast<int>(container.size());
    }
    void clear() {
        container.clear();
    }
    void fill_random(int count, int min_val, int max_val) {
        if (!seeded) {
            std::srand(static_cast<unsigned>(std::time(nullptr)));
            seeded = true;
        }
        for (int i = 0; i < count; ++i) {
            int val = min_val + std::rand() % (max_val - min_val + 1);
            container.push_back(val);
        }
    }
    std::deque<int> get_all() const {
        return container;
    }
};
bool Queue::seeded = false;

PYBIND11_MODULE(queue_stl_pybind, m) {
    m.doc() = "Очередь на C++";

    py::class_<Queue>(m, "Queue")
        .def(py::init<>())
        .def("create_queue", &Queue::create_queue)
        .def("is_empty", &Queue::is_empty)
        .def("enqueue", &Queue::enqueue)
        .def("dequeue", &Queue::dequeue)
        .def("peek", &Queue::peek)
        .def("size", &Queue::size)
        .def("clear", &Queue::clear)
        .def("fill_random", &Queue::fill_random)
        .def("get_all", &Queue::get_all);

}
