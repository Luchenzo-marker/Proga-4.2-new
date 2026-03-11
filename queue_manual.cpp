#include <cstdlib>
#include <ctime>

#ifdef _WIN32
    #define DLL_EXPORT __declspec(dllexport)
#else
    #define DLL_EXPORT
#endif

extern "C" {

struct Node {
    int data;
    Node* next;
};

static Node* front = nullptr;
static Node* rear = nullptr;
static int count = 0;

DLL_EXPORT void create_queue() {
    while (front != nullptr) {
        Node* temp = front;
        front = front->next;
        delete temp;
    }
    rear = nullptr;
    count = 0;
}

DLL_EXPORT int is_empty() {
    return (front == nullptr) ? 1 : 0;
}

DLL_EXPORT void enqueue(int value) {
    Node* node = new Node;
    node->data = value;
    node->next = nullptr;

    if (rear == nullptr) {
        front = rear = node;
    } else {
        rear->next = node;
        rear = node;
    }
    count++;
}

DLL_EXPORT int dequeue(int* success) {
    if (front == nullptr) {
        *success = 0;
        return 0;
    }
    Node* temp = front;
    int value = temp->data;
    front = temp->next;
    if (front == nullptr) {
        rear = nullptr;
    }
    delete temp;
    count--;
    *success = 1;
    return value;
}

DLL_EXPORT int peek(int* value) {
    if (front == nullptr) return 0;
    *value = front->data;
    return 1;
}

DLL_EXPORT int size() {
    return count;
}

DLL_EXPORT void clear_queue() {
    while (front != nullptr) {
        Node* temp = front;
        front = front->next;
        delete temp;
    }
    rear = nullptr;
    count = 0;
}

DLL_EXPORT void fill_random(int cnt, int min_val, int max_val) {
    static bool seeded = false;
    if (!seeded) {
        std::srand(static_cast<unsigned>(std::time(nullptr)));
        seeded = true;
    }
    for (int i = 0; i < cnt; ++i) {
        int val = min_val + std::rand() % (max_val - min_val + 1);
        enqueue(val);
    }
}

}