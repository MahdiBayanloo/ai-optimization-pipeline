# Forbidden Patterns — Never Generate These

- osDelay() / vTaskDelay() / sleep() / usleep() — all forbidden
- while(status == IN_PROGRESS) { ... } — busy-wait loop, forbidden
- Any function that waits for a network response synchronously
- Calling CycloneTCP TLS functions directly from an Activity handler
- Storing state on the C++ call stack between ticks (use member variables)
- Creating RTOS threads or using any threading primitives
- Recursive calls that could overflow the single shared stack
- Any use of std::mutex, std::thread, std::condition_variable
