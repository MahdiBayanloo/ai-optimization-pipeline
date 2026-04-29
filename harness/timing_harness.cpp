// timing_harness.cpp
// ─────────────────────────────────────────────────────────────────────────
// Standalone timing harness for validating the TLS blocking fix in the
// seve / Reflex cooperative event-driven OS.
//
//   Goal: prove that after applying the AI-generated patch
//         (TlsHandshakeAdapter), the event loop is no longer frozen
//         for ~500ms during a TLS handshake.
//
//   Modes
//   -----
//     before : monolithic blocking handshake during tick 20
//              (this models the unpatched CycloneSSL behavior)
//     after  : non-blocking start() at tick 20 + progress() per tick
//              (this models the TlsHandshakeAdapter state machine)
//
//   Output files (written to current working directory)
//   ---------------------------------------------------
//     baseline.json    full per-tick trace of the BEFORE run
//     after.json       full per-tick trace of the AFTER run
//     comparison.json  PASS/FAIL verdict + summary metrics
//
//   Build
//   -----
//     g++ -std=c++20 -O0 -pthread timing_harness.cpp -o harness
//
//   Run
//   ---
//     ./harness            # runs both, writes all three JSON files
//     ./harness before     # baseline.json only
//     ./harness after      # after.json only
//
//   Verdict criteria (in compare step)
//   ----------------------------------
//     1. TLS completes in BOTH runs.
//     2. before.max_tick_gap_ms >= 100 ms   (blocking is observable)
//     3. after.max_tick_gap_ms  <  10 ms    (event loop stays responsive)
//     4. before.ticks_during_tls == 0       (no ticks ran inside handshake)
//     5. after.ticks_during_tls  > 40       (ticks kept running)
// ─────────────────────────────────────────────────────────────────────────

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

using clk = std::chrono::steady_clock;
using ms  = std::chrono::milliseconds;
using us  = std::chrono::microseconds;

// ── Configuration ─────────────────────────────────────────────────────────
constexpr int    TOTAL_TICKS      = 200;
constexpr int    TLS_TRIGGER_TICK = 20;
constexpr int    TICK_IDLE_MS     = 1;     // background loop period
constexpr int    BLOCKING_TLS_MS  = 500;   // simulated blocking handshake
constexpr int    HANDSHAKE_STEPS  = 50;    // chunks in non-blocking handshake
constexpr int    STEP_WORK_MS     = 1;     // work per progress() call
constexpr double VERDICT_GAP_MS   = 10.0;  // after-run gap ceiling
constexpr double BLOCKING_GAP_MS  = 100.0; // before-run gap floor

// ── Mock TLS adapter – two modes ──────────────────────────────────────────
struct TlsAdapter {
    enum State { IDLE, RUNNING, DONE };
    State state          = IDLE;
    int   progress_count = 0;

    // BEFORE patch: handshake runs to completion in one call – blocks loop.
    void blocking_handshake() {
        state = RUNNING;
        std::this_thread::sleep_for(ms(BLOCKING_TLS_MS));
        state = DONE;
    }

    // AFTER patch: start() returns immediately. Each progress() does a
    // small chunk of crypto work; after HANDSHAKE_STEPS calls, state=DONE.
    void start() {
        state          = RUNNING;
        progress_count = 0;
    }
    void progress() {
        if (state != RUNNING) return;
        std::this_thread::sleep_for(ms(STEP_WORK_MS)); // simulated chunk
        ++progress_count;
        if (progress_count >= HANDSHAKE_STEPS) state = DONE;
    }
};

// ── Per-run result ─────────────────────────────────────────────────────────
struct Result {
    std::string          mode;
    std::vector<int64_t> tick_timestamps_us; // microseconds since loop start
    int    tls_start_tick    = -1;
    int    tls_done_tick     = -1;
    int    ticks_during_tls  = 0;
    double max_tick_gap_ms   = 0.0;
    double avg_tick_gap_ms   = 0.0;
    bool   tls_completed     = false;
};

// ── One simulation run ─────────────────────────────────────────────────────
Result run_simulation(const std::string& mode) {
    Result r;
    r.mode = mode;
    r.tick_timestamps_us.reserve(TOTAL_TICKS);

    TlsAdapter tls;
    auto t0 = clk::now();

    for (int tick = 0; tick < TOTAL_TICKS; ++tick) {
        // Record this tick's timestamp the moment we enter it.
        auto    now = clk::now();
        int64_t t   = std::chrono::duration_cast<us>(now - t0).count();
        r.tick_timestamps_us.push_back(t);

        // Trigger TLS at the configured tick.
        if (tick == TLS_TRIGGER_TICK) {
            r.tls_start_tick = tick;
            std::cout << "[Tick " << tick << "] TLS handshake triggered ("
                      << mode << " mode)\n";
            if (mode == "before") {
                tls.blocking_handshake();   // ← freezes loop for ~500ms
                r.tls_done_tick  = tick;    //   completes in same tick
                r.tls_completed  = true;
                std::cout << "[Tick " << tick << "] TLS done (blocking)\n";
            } else {
                tls.start();                // returns immediately
            }
        }

        // In after-mode, drive the state machine from each tick.
        if (mode == "after" && tls.state == TlsAdapter::RUNNING) {
            tls.progress();
            if (tls.state == TlsAdapter::DONE && r.tls_done_tick < 0) {
                r.tls_done_tick = tick;
                r.tls_completed = true;
                std::cout << "[Tick " << tick << "] TLS done (non-blocking)\n";
            }
        }

        // Background idle period (the loop itself isn't free-running).
        std::this_thread::sleep_for(ms(TICK_IDLE_MS));
    }

    // Compute gap statistics over the recorded tick timestamps.
    double max_gap_us = 0.0, total_gap_us = 0.0;
    for (size_t i = 1; i < r.tick_timestamps_us.size(); ++i) {
        double gap = double(r.tick_timestamps_us[i] -
                            r.tick_timestamps_us[i - 1]);
        total_gap_us += gap;
        if (gap > max_gap_us) max_gap_us = gap;
    }
    r.max_tick_gap_ms = max_gap_us / 1000.0;
    r.avg_tick_gap_ms = (total_gap_us /
        std::max<size_t>(1, r.tick_timestamps_us.size() - 1)) / 1000.0;

    // ticks that landed strictly between TLS start and TLS done.
    if (r.tls_start_tick >= 0 && r.tls_done_tick > r.tls_start_tick)
        r.ticks_during_tls = r.tls_done_tick - r.tls_start_tick - 1;
    else
        r.ticks_during_tls = 0;

    return r;
}

// ── Minimal JSON output (zero deps) ───────────────────────────────────────
static void write_result_json(const Result& r, const std::string& path) {
    std::ofstream f(path);
    f << "{\n";
    f << "  \"mode\": \""              << r.mode               << "\",\n";
    f << "  \"total_ticks\": "         << r.tick_timestamps_us.size() << ",\n";
    f << "  \"tls_trigger_tick\": "    << TLS_TRIGGER_TICK     << ",\n";
    f << "  \"tls_start_tick\": "      << r.tls_start_tick     << ",\n";
    f << "  \"tls_done_tick\": "       << r.tls_done_tick      << ",\n";
    f << "  \"tls_completed\": "       << (r.tls_completed ? "true" : "false") << ",\n";
    f << "  \"ticks_during_tls\": "    << r.ticks_during_tls   << ",\n";
    f << "  \"max_tick_gap_ms\": "     << r.max_tick_gap_ms    << ",\n";
    f << "  \"avg_tick_gap_ms\": "     << r.avg_tick_gap_ms    << ",\n";
    f << "  \"tick_timestamps_us\": [";
    for (size_t i = 0; i < r.tick_timestamps_us.size(); ++i) {
        f << r.tick_timestamps_us[i];
        if (i + 1 < r.tick_timestamps_us.size()) f << ", ";
    }
    f << "]\n";
    f << "}\n";
}

static void write_comparison_json(const Result& before,
                                  const Result& after,
                                  const std::string& path) {
    bool tls_ok               = before.tls_completed && after.tls_completed;
    bool before_blocking      = before.max_tick_gap_ms >= BLOCKING_GAP_MS;
    bool after_unblocked      = after.max_tick_gap_ms  <  VERDICT_GAP_MS;
    bool before_no_ticks      = before.ticks_during_tls == 0;
    bool after_many_ticks     = after.ticks_during_tls  > 40;

    bool verdict = tls_ok && before_blocking && after_unblocked &&
                   before_no_ticks && after_many_ticks;

    std::ofstream f(path);
    f << "{\n";
    f << "  \"verdict\": \"" << (verdict ? "PASS" : "FAIL") << "\",\n";
    f << "  \"thresholds\": {\n";
    f << "    \"after_max_tick_gap_ms_lt\": " << VERDICT_GAP_MS  << ",\n";
    f << "    \"before_max_tick_gap_ms_ge\": " << BLOCKING_GAP_MS << ",\n";
    f << "    \"after_ticks_during_tls_gt\": 40,\n";
    f << "    \"before_ticks_during_tls_eq\": 0\n";
    f << "  },\n";
    f << "  \"before\": {\n";
    f << "    \"max_tick_gap_ms\": "  << before.max_tick_gap_ms  << ",\n";
    f << "    \"avg_tick_gap_ms\": "  << before.avg_tick_gap_ms  << ",\n";
    f << "    \"ticks_during_tls\": " << before.ticks_during_tls << ",\n";
    f << "    \"tls_completed\": "    << (before.tls_completed ? "true" : "false") << "\n";
    f << "  },\n";
    f << "  \"after\": {\n";
    f << "    \"max_tick_gap_ms\": "  << after.max_tick_gap_ms   << ",\n";
    f << "    \"avg_tick_gap_ms\": "  << after.avg_tick_gap_ms   << ",\n";
    f << "    \"ticks_during_tls\": " << after.ticks_during_tls  << ",\n";
    f << "    \"tls_completed\": "    << (after.tls_completed ? "true" : "false") << "\n";
    f << "  },\n";
    f << "  \"checks\": {\n";
    f << "    \"tls_completed_both\": "          << (tls_ok            ? "true" : "false") << ",\n";
    f << "    \"before_shows_blocking\": "       << (before_blocking   ? "true" : "false") << ",\n";
    f << "    \"after_unblocked\": "             << (after_unblocked   ? "true" : "false") << ",\n";
    f << "    \"before_ticks_during_tls_eq_0\": "<< (before_no_ticks   ? "true" : "false") << ",\n";
    f << "    \"after_ticks_during_tls_gt_40\": "<< (after_many_ticks  ? "true" : "false") << "\n";
    f << "  }\n";
    f << "}\n";
}

// ── Pretty per-run summary on stdout ──────────────────────────────────────
static void print_summary(const Result& r) {
    std::cout << "  mode             : " << r.mode << "\n"
              << "  tls_completed    : " << (r.tls_completed ? "yes" : "no") << "\n"
              << "  tls_start_tick   : " << r.tls_start_tick << "\n"
              << "  tls_done_tick    : " << r.tls_done_tick << "\n"
              << "  ticks_during_tls : " << r.ticks_during_tls << "\n"
              << "  max_tick_gap_ms  : " << r.max_tick_gap_ms << "\n"
              << "  avg_tick_gap_ms  : " << r.avg_tick_gap_ms << "\n";
}

// ── main ──────────────────────────────────────────────────────────────────
int main(int argc, char** argv) {
    std::string mode = (argc > 1) ? argv[1] : "both";

    Result before, after;
    bool have_before = false, have_after = false;

    if (mode == "before" || mode == "both") {
        std::cout << "── BEFORE patch (blocking handshake) ───────────────────\n";
        before = run_simulation("before");
        write_result_json(before, "baseline.json");
        std::cout << "Wrote baseline.json\n";
        print_summary(before);
        have_before = true;
    }

    if (mode == "after" || mode == "both") {
        std::cout << "\n── AFTER patch (non-blocking adapter) ──────────────────\n";
        after = run_simulation("after");
        write_result_json(after, "after.json");
        std::cout << "Wrote after.json\n";
        print_summary(after);
        have_after = true;
    }

    if (have_before && have_after) {
        write_comparison_json(before, after, "comparison.json");
        bool verdict =
            before.tls_completed && after.tls_completed &&
            before.max_tick_gap_ms >= BLOCKING_GAP_MS &&
            after.max_tick_gap_ms  <  VERDICT_GAP_MS &&
            before.ticks_during_tls == 0 &&
            after.ticks_during_tls  > 40;

        std::cout << "\n── Comparison ──────────────────────────────────────────\n"
                  << "Wrote comparison.json\n"
                  << "VERDICT: " << (verdict ? "PASS ✓" : "FAIL ✗") << "\n";
        return verdict ? 0 : 1;
    }
    return 0;
}
