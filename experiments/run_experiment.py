"""
Experiment runner — orchestrates the full AgentDojo evaluation:

  For each (user_task × defense):
    1. Benign run   — no injection
    2. Attack run   — for each (injection_task × attack),
                      inject into tool output data

  Records results and computes aggregate metrics.
"""

import json
import traceback
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from environments.workspace import WorkspaceEnvironment
from tasks.user_tasks import USER_TASKS
from tasks.injection_tasks import INJECTION_TASKS
from attacks.ignore_previous import IgnorePreviousAttack
from attacks.important_message import ImportantMessageAttack
from defenses import create_defense
from agent.pipeline import AgentPipeline
from tools.tool_registry import TOOL_SCHEMAS
from evaluation.utility import evaluate_utility
from evaluation.security import evaluate_security
from evaluation.metrics import compute_metrics


# ---------------------------------------------------------------
# Attack registry
# ---------------------------------------------------------------

ATTACKS = {
    "ignore_previous": IgnorePreviousAttack,
    "important_message": ImportantMessageAttack,
}


# ---------------------------------------------------------------
# Inject attack payload into environment data
# ---------------------------------------------------------------

def inject_into_emails(emails, payload):
    """
    Inject the attack payload into the first email's body.
    Returns a modified copy.
    """
    injected = deepcopy(emails)

    if injected:
        injected[0]["body"] += payload

    return injected


# ---------------------------------------------------------------
# Single experiment run
# ---------------------------------------------------------------

def run_single(
    user_task,
    defense_name,
    injection_task=None,
    attack=None,
    verbose=False,
):
    """
    Run one experiment trial.

    Args:
        user_task: dict from USER_TASKS
        defense_name: name of the defense to use
        injection_task: dict from INJECTION_TASKS (or None for benign)
        attack: BaseAttack instance (or None for benign)
        verbose: print intermediate output

    Returns:
        dict with mode, result, utility, security (if attack)
    """
    # Fresh environment for each trial.
    env = WorkspaceEnvironment()

    # If attack mode, inject into the environment data.
    if injection_task and attack:
        payload = attack.apply(
            injection_task["untrusted_content"]
        )
        env._emails = inject_into_emails(
            env._emails, payload
        )

    # Snapshot state before the agent runs.
    state_before = env.snapshot()

    # Create the pipeline with the selected defense.
    defense = create_defense(defense_name)
    pipeline = AgentPipeline(
        environment=env,
        tool_schemas=TOOL_SCHEMAS,
        defense=defense,
    )

    # Determine the prompt.
    if injection_task:
        prompt = injection_task["user_prompt"]
    else:
        prompt = user_task["prompt"]

    # Run the agent.
    try:
        result = pipeline.run(prompt)
    except Exception as error:
        if verbose:
            traceback.print_exc()
        result = {
            "answer": f"[ERROR] {error}",
            "tool_trace": [],
            "steps": 0,
        }

    # Snapshot state after the agent runs.
    state_after = env.snapshot()

    # Evaluate utility.
    utility = evaluate_utility(
        result, user_task, state_after
    )

    # Build the record.
    record = {
        "mode": "attack" if injection_task else "benign",
        "user_task_id": user_task["task_id"],
        "defense": defense_name,
        "result": result,
        "utility": utility,
    }

    # Evaluate security (attack mode only).
    if injection_task:
        security = evaluate_security(
            result, injection_task, state_after
        )
        record["security"] = security
        record["injection_task_id"] = (
            injection_task["task_id"]
        )
        record["attack_type"] = (
            injection_task["attack_type"]
        )

    if verbose:
        mode_label = record["mode"].upper()
        print(
            f"  [{mode_label}] "
            f"task={user_task['task_id']}  "
            f"defense={defense_name}  "
            f"utility={utility['score']:.2f}"
        )
        if injection_task:
            asr = record["security"]["attack_success"]
            print(f"  attack_success={asr}")

    return record


# ---------------------------------------------------------------
# Full experiment sweep
# ---------------------------------------------------------------

def run_experiment(
    defense_names=None,
    verbose=True,
):
    """
    Run the full AgentDojo evaluation sweep.

    Args:
        defense_names: list of defense names to test.
                       Defaults to all registered defenses.
        verbose: print progress.

    Returns:
        dict with 'results' list and 'metrics' per defense.
    """
    if defense_names is None:
        defense_names = ["no_defense", "delimiter", "detector"]

    all_results = []

    for defense_name in defense_names:

        if verbose:
            print(f"\n{'='*60}")
            print(f"Defense: {defense_name}")
            print(f"{'='*60}")

        defense_results = []

        # ----- Benign runs -----
        for task in USER_TASKS:

            if verbose:
                print(f"\n  Benign: {task['task_id']}")

            record = run_single(
                user_task=task,
                defense_name=defense_name,
                verbose=verbose,
            )
            defense_results.append(record)

        # ----- Attack runs -----
        for injection_task in INJECTION_TASKS:

            attack_type = injection_task["attack_type"]
            attack_cls = ATTACKS.get(attack_type)

            if attack_cls is None:
                if verbose:
                    print(
                        f"  Skipping unknown attack: "
                        f"{attack_type}"
                    )
                continue

            attack = attack_cls()

            # Use the user task that matches the
            # injection task's category.
            matching_user_tasks = [
                t for t in USER_TASKS
                if t["category"] == injection_task["category"]
            ]

            if not matching_user_tasks:
                matching_user_tasks = USER_TASKS[:1]

            for task in matching_user_tasks:

                if verbose:
                    print(
                        f"\n  Attack: {injection_task['task_id']}"
                        f" vs {task['task_id']}"
                    )

                record = run_single(
                    user_task=task,
                    defense_name=defense_name,
                    injection_task=injection_task,
                    attack=attack,
                    verbose=verbose,
                )
                defense_results.append(record)

        all_results.extend(defense_results)

        # Compute per-defense metrics.
        metrics = compute_metrics(defense_results)

        if verbose:
            print(f"\n  --- {defense_name} metrics ---")
            print(
                f"  Benign Utility:      "
                f"{metrics['benign_utility']:.2f}"
            )
            print(
                f"  Utility Under Attack: "
                f"{metrics['attack_utility']:.2f}"
            )
            print(
                f"  Attack Success Rate:  "
                f"{metrics['attack_success_rate']:.2f}"
            )

    # ----- Save results -----
    output = {
        "timestamp": datetime.now().isoformat(),
        "defense_names": defense_names,
        "results": _serialize_results(all_results),
        "metrics_by_defense": {
            d: compute_metrics(
                [r for r in all_results if r["defense"] == d]
            )
            for d in defense_names
        },
    }

    output_path = Path("experiments") / "results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, default=str)

    if verbose:
        print(f"\nResults saved to {output_path}")

    return output


def _serialize_results(results):
    """
    Make results JSON-serializable by stripping
    non-serializable raw_response objects.
    """
    clean = []
    for r in results:
        cr = dict(r)
        if "result" in cr and isinstance(cr["result"], dict):
            result_copy = dict(cr["result"])
            # Strip tool_trace raw_result if needed.
            result_copy.pop("raw_response", None)
            cr["result"] = result_copy
        clean.append(cr)
    return clean


# ---------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------

if __name__ == "__main__":
    run_experiment(verbose=True)

