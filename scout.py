#!/usr/bin/env python3
"""
scout.py — periCORE-SDK Blocking Call Discovery
Usage: python3 scout.py --sdk <path-to-sdk-root> --out <output-file>
"""

import os, sys, argparse, datetime, subprocess
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
from config import CONFIG

SCAN_DIRS     = ["seve", "libperiCORE", "applications"]
SCAN_EXTS     = {".c", ".cpp", ".h", ".hpp"}
MAX_FILE_SIZE  = 200_000   # bytes
MAX_TOTAL_CHARS = 140_000  # chars sent to API

# Keywords that indicate a file is relevant to blocking/TLS/network
PRIORITY_KEYWORDS = [
    "tls", "ssl", "mbedtls", "wolfssl", "cyclone", "handshake",
    "x509", "certificate", "crypto", "mqtt", "http", "socket",
    "connect", "sleep", "delay", "poll", "blocking", "wait",
    "security", "encrypt", "decrypt", "firmware", "update",
]

SCOUT_PROMPT = """You are a static analysis agent for an embedded C/C++ codebase.

The system is a single-threaded, non-preemptive, event-driven OS called Reflex
running on ARM microcontrollers. A purchased third-party TLS/networking stack
called CycloneTCP has been integrated. The event loop must never block.

Your job: find every location in the code below where the event loop could block.

Focus on:
1. TLS handshake calls (tls_*, ssl_*, tlsConnect, tlsClientHandshake, etc.)
2. Crypto key generation or certificate parsing (x509*, rsa*, ecdsa*, etc.)
3. Any sleep(), wait(), delay(), osDelay(), or poll() inside event handlers
4. Any synchronous socket or network call that waits for completion
5. Any function that loops without yielding to the event loop
6. CycloneTCP API calls that are synchronous/blocking by nature

For each finding report:
- FILE: relative path
- FUNCTION: name of the containing function or class method
- LINE HINT: 1-2 lines of surrounding code (copy exactly)
- BLOCKING TYPE: TLS handshake / crypto / sleep / sync socket / unbounded loop / other
- SEVERITY: HIGH (definitely blocks) / MEDIUM (likely blocks) / LOW (possible concern)
- NOTE: one sentence explaining why it blocks

End with a SUMMARY section:
- Total HIGH / MEDIUM / LOW findings
- Recommended first target (most isolated HIGH finding, best candidate to transform first)
- Recommended transformation pattern (State Machine / Adapter Layer / Callback Wrapper)

Be precise. Only report what you actually see. If no blocking found, say so.
"""

def collect_all_files(sdk_root):
    files = []
    for d in SCAN_DIRS:
        abs_dir = os.path.join(sdk_root, d)
        if not os.path.isdir(abs_dir):
            print(f"  [scout] Warning: not found: {abs_dir}")
            continue
        for root, _, filenames in os.walk(abs_dir):
            for fname in sorted(filenames):
                if os.path.splitext(fname)[1] in SCAN_EXTS:
                    abs_path = os.path.join(root, fname)
                    rel_path = os.path.relpath(abs_path, sdk_root)
                    size = os.path.getsize(abs_path)
                    files.append((rel_path, abs_path, size))
    return files

def score_file(rel_path, abs_path):
    """Score a file by how many priority keywords appear in its path or content preview."""
    score = 0
    path_lower = rel_path.lower()
    for kw in PRIORITY_KEYWORDS:
        if kw in path_lower:
            score += 10  # path match is strong signal

    # Quick grep of first 4KB for keywords
    try:
        preview = open(abs_path, "r", encoding="utf-8", errors="replace").read(4096).lower()
        for kw in PRIORITY_KEYWORDS:
            if kw in preview:
                score += 1
    except Exception:
        pass
    return score

def build_codebase_block(files, sdk_root):
    parts = []
    total = 0
    included = []
    skipped = []

    for rel_path, abs_path, size in files:
        if size > MAX_FILE_SIZE:
            skipped.append((rel_path, "file too large"))
            continue
        try:
            content = open(abs_path, "r", encoding="utf-8", errors="replace").read()
        except Exception as e:
            skipped.append((rel_path, str(e)))
            continue

        block = f"// === FILE: {rel_path} ===\n{content}\n"
        if total + len(block) > MAX_TOTAL_CHARS:
            skipped.append((rel_path, "context limit reached"))
            continue

        parts.append(block)
        total += len(block)
        included.append(rel_path)

    return "\n".join(parts), included, skipped

def run_scout_agent(codebase_block):
    import anthropic
    model  = CONFIG["default_model"]
    client = anthropic.Anthropic(api_key=CONFIG["api_key"])
    prompt = SCOUT_PROMPT + "\n\n---\n## CODEBASE\n\n" + codebase_block
    print(f"  [scout] Sending {len(prompt):,} chars to {model}...")
    msg = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    response = msg.content[0].text
    in_tok  = msg.usage.input_tokens
    out_tok = msg.usage.output_tokens
    cost    = round((in_tok * 15 + out_tok * 75) / 1_000_000, 4)
    print(f"  [scout] {in_tok}in / {out_tok}out tokens — estimated cost: ${cost}")
    return response, in_tok, out_tok

def write_report(out_path, sdk_root, included, skipped, response, in_tok, out_tok):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# Scout Report — periCORE-SDK Blocking Call Discovery",
        "",
        f"**Generated:** {ts}  ",
        f"**SDK root:** {sdk_root}  ",
        f"**Files scanned:** {len(included)}  ",
        f"**Files skipped:** {len(skipped)}  ",
        f"**Tokens:** {in_tok} in / {out_tok} out  ",
        "",
        "---",
        "",
        "## Files Included in Scan",
        "",
    ]
    for f in included:
        lines.append(f"- `{f}`")

    if skipped:
        lines += ["", "## Files Skipped", ""]
        for f, reason in skipped:
            lines.append(f"- `{f}` — {reason}")

    lines += [
        "",
        "---",
        "",
        "## Analysis",
        "",
        response,
        "",
        "---",
        "",
        "## Next Step",
        "",
        "Review the HIGH findings above. For each target:",
        "1. `cp -r task_template/ task_<name>/`",
        "2. Update `knowledge/system_summary.md` for periCORE-SDK",
        "3. Write `tasks/task.md` naming the specific file and function",
        "4. Copy the target source file into `codebase/`",
        "5. `python3 run_pipeline.py --task task_<name>/`",
    ]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [scout] Report written: {out_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sdk", required=True)
    parser.add_argument("--out", default="scout_report.md")
    args = parser.parse_args()

    sdk_root = os.path.expanduser(args.sdk)
    if not os.path.isdir(sdk_root):
        print(f"Error: not found: {sdk_root}")
        sys.exit(1)

    print(f"\n=== Scout: scanning {sdk_root} ===\n")

    all_files = collect_all_files(sdk_root)
    print(f"  [scout] Found {len(all_files)} source files total")

    # Score and sort — highest relevance first
    scored = sorted(all_files, key=lambda x: -score_file(x[0], x[1]))

    print(f"  [scout] Top 10 by relevance score:")
    for rel, abs_p, size in scored[:10]:
        sc = score_file(rel, abs_p)
        print(f"    score={sc:3d}  {rel}")

    codebase_block, included, skipped = build_codebase_block(scored, sdk_root)
    print(f"\n  [scout] Sending {len(included)} files ({len(codebase_block):,} chars)")
    print(f"  [scout] Skipped {len(skipped)} lower-priority files")

    response, in_tok, out_tok = run_scout_agent(codebase_block)

    out_path = os.path.expanduser(args.out)
    write_report(out_path, sdk_root, included, skipped, response, in_tok, out_tok)

    print(f"\n=== Scout complete. Review: {out_path} ===\n")

if __name__ == "__main__":
    main()
