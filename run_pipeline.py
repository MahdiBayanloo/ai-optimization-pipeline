#!/usr/bin/env python3
"""
run_pipeline.py — Reflex AI Optimization Pipeline Orchestrator
Usage: python3 run_pipeline.py --task <path-to-task-folder>
"""

import os, sys, json, argparse, datetime
from config import CONFIG

def resolve_paths(task_folder):
    tf = os.path.abspath(task_folder)
    return {
        "task_folder":  tf,
        "knowledge":    os.path.join(tf, "knowledge"),
        "prompts":      os.path.join(tf, "prompts"),
        "tasks":        os.path.join(tf, "tasks"),
        "codebase":     os.path.join(tf, "codebase"),
        "outputs":      os.path.join(tf, "outputs"),
        "tests":        os.path.join(tf, "tests"),
    }

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def read_dir(folder, exts=None):
    result = {}
    if not os.path.isdir(folder):
        return result
    for fname in sorted(os.listdir(folder)):
        if exts and not any(fname.endswith(e) for e in exts):
            continue
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath):
            result[fname] = read_file(fpath)
    return result

class RunLogger:
    def __init__(self, outputs_dir):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(outputs_dir, f"run_log_{ts}.jsonl")
        os.makedirs(outputs_dir, exist_ok=True)

    def log(self, agent, prompt, response, model, input_tokens, output_tokens):
        entry = {
            "agent":         agent,
            "model":         model,
            "input_tokens":  input_tokens,
            "output_tokens": output_tokens,
            "cost_estimate": round((input_tokens * 15 + output_tokens * 75) / 1_000_000, 6),
            "prompt":        prompt,
            "response":      response,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"  [log] {agent}: {input_tokens}in / {output_tokens}out tokens")

def call_agent(agent_name, prompt, logger):
    import anthropic
    model = (CONFIG["agents"][agent_name]["model"] or CONFIG["default_model"])
    client = anthropic.Anthropic(api_key=CONFIG["api_key"])
    msg = client.messages.create(
        model=model,
        max_tokens=CONFIG["max_tokens"],
        messages=[{"role": "user", "content": prompt}]
    )
    response = msg.content[0].text
    logger.log(agent_name, prompt, response, model,
               msg.usage.input_tokens, msg.usage.output_tokens)
    return response

def build_prompt(prompt_template, **sections):
    parts = [prompt_template]
    for title, content in sections.items():
        parts.append(f"\n\n---\n## {title}\n\n{content}")
    return "\n".join(parts)

def knowledge_block(knowledge_files):
    return "\n\n".join(f"### {k}\n{v}" for k, v in knowledge_files.items())

def run_planner(p, knowledge, prompts, logger):
    print("[1/6] Planner...")
    task   = read_file(os.path.join(p["tasks"], sorted(os.listdir(p["tasks"]))[0]))
    code   = read_dir(p["codebase"])
    prompt = build_prompt(prompts["planner.txt"],
                          KNOWLEDGE=knowledge_block(knowledge),
                          TASK=task,
                          CODEBASE="\n\n".join(f"// {k}\n{v}" for k, v in code.items()))
    result = call_agent("planner", prompt, logger)
    write_file(os.path.join(p["outputs"], "plan.md"), result)
    return result

def run_generator(p, knowledge, prompts, plan, logger):
    print("[2/6] Generator...")
    task   = read_file(os.path.join(p["tasks"], sorted(os.listdir(p["tasks"]))[0]))
    code   = read_dir(p["codebase"])
    prompt = build_prompt(prompts["generator.txt"],
                          KNOWLEDGE=knowledge_block(knowledge),
                          TASK=task,
                          CODEBASE="\n\n".join(f"// {k}\n{v}" for k, v in code.items()),
                          PLAN=plan)
    result = call_agent("generator", prompt, logger)
    write_file(os.path.join(p["outputs"], "patch.diff"), result)
    return result

def run_arch_reviewer(p, knowledge, prompts, plan, patch, logger):
    print("[3/6] Architecture Reviewer...")
    task   = read_file(os.path.join(p["tasks"], sorted(os.listdir(p["tasks"]))[0]))
    code   = read_dir(p["codebase"])
    prompt = build_prompt(prompts["architecture_reviewer.txt"],
                          KNOWLEDGE=knowledge_block(knowledge),
                          TASK=task,
                          CODEBASE="\n\n".join(f"// {k}\n{v}" for k, v in code.items()),
                          PLAN=plan,
                          PATCH=patch)
    result = call_agent("architecture_reviewer", prompt, logger)
    write_file(os.path.join(p["outputs"], "architecture_review.md"), result)
    return result

def run_behav_reviewer(p, knowledge, prompts, plan, patch, logger):
    print("[4/6] Behavior Reviewer...")
    task   = read_file(os.path.join(p["tasks"], sorted(os.listdir(p["tasks"]))[0]))
    code   = read_dir(p["codebase"])
    prompt = build_prompt(prompts["behavior_reviewer.txt"],
                          KNOWLEDGE=knowledge_block(knowledge),
                          TASK=task,
                          CODEBASE="\n\n".join(f"// {k}\n{v}" for k, v in code.items()),
                          PLAN=plan,
                          PATCH=patch)
    result = call_agent("behavior_reviewer", prompt, logger)
    write_file(os.path.join(p["outputs"], "behavior_review.md"), result)
    return result

def run_repair(p, knowledge, prompts, plan, patch, arch_review, behav_review, logger):
    print("[R] Repair Agent...")
    task   = read_file(os.path.join(p["tasks"], sorted(os.listdir(p["tasks"]))[0]))
    code   = read_dir(p["codebase"])
    prompt = build_prompt(prompts["repair_agent.txt"],
                          KNOWLEDGE=knowledge_block(knowledge),
                          TASK=task,
                          CODEBASE="\n\n".join(f"// {k}\n{v}" for k, v in code.items()),
                          PLAN=plan,
                          PATCH=patch,
                          ARCHITECTURE_REVIEW=arch_review,
                          BEHAVIOR_REVIEW=behav_review)
    result = call_agent("repair", prompt, logger)
    write_file(os.path.join(p["outputs"], "repair.diff"), result)
    return result

def run_test_designer(p, knowledge, prompts, plan, patch, logger):
    print("[6/6] Test Designer...")
    task   = read_file(os.path.join(p["tasks"], sorted(os.listdir(p["tasks"]))[0]))
    code   = read_dir(p["codebase"])
    prompt = build_prompt(prompts["test_designer.txt"],
                          KNOWLEDGE=knowledge_block(knowledge),
                          TASK=task,
                          CODEBASE="\n\n".join(f"// {k}\n{v}" for k, v in code.items()),
                          PLAN=plan,
                          PATCH=patch)
    result = call_agent("test_designer", prompt, logger)
    write_file(os.path.join(p["outputs"], "test_plan.md"), result)
    return result

def is_fail(review_text):
    return "FAIL" in review_text.upper()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, help="Path to task folder")
    args = parser.parse_args()

    p         = resolve_paths(args.task)
    logger    = RunLogger(p["outputs"])
    knowledge = read_dir(p["knowledge"], exts=[".md"])
    prompts   = read_dir(p["prompts"],   exts=[".txt"])

    print(f"\n=== Pipeline start: {args.task} ===\n")

    plan         = run_planner(p, knowledge, prompts, logger)
    patch        = run_generator(p, knowledge, prompts, plan, logger)
    arch_review  = run_arch_reviewer(p, knowledge, prompts, plan, patch, logger)
    behav_review = run_behav_reviewer(p, knowledge, prompts, plan, patch, logger)

    repair_iter = 0
    max_repairs = CONFIG["max_repair_iterations"]
    while (is_fail(arch_review) or is_fail(behav_review)) and repair_iter < max_repairs:
        repair_iter += 1
        print(f"  [repair loop {repair_iter}/{max_repairs}]")
        patch        = run_repair(p, knowledge, prompts, plan, patch,
                                  arch_review, behav_review, logger)
        arch_review  = run_arch_reviewer(p, knowledge, prompts, plan, patch, logger)
        behav_review = run_behav_reviewer(p, knowledge, prompts, plan, patch, logger)

    if repair_iter == max_repairs and (is_fail(arch_review) or is_fail(behav_review)):
        print("\n  [!] Max repair iterations reached — manual review needed.")

    run_test_designer(p, knowledge, prompts, plan, patch, logger)

    # TODO Phase 10.5: git apply patch -> make build -> run tests -> feed errors to Repair

    print(f"\n=== Pipeline complete. Outputs in: {p['outputs']} ===\n")

if __name__ == "__main__":
    main()
