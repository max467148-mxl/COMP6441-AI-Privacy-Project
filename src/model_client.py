import json
import os


def dry_run_response(profile_id, condition_name, question):
    confidence = {
        "no_memory": 0.15,
        "limited_memory": 0.45,
        "full_aggregated_memory": 0.75,
        "compartmentalised_memory": 0.35,
    }.get(condition_name, 0.2)
    return json.dumps(
        {
            "answer": (
                f"Dry-run placeholder for {profile_id}. This is not final evidence. "
                f"The response simulates a {question['category']} inference under {condition_name}."
            ),
            "evidence": ["Dry-run output; run a real model for report evidence."],
            "confidence": confidence,
            "refusal_or_uncertainty": condition_name == "no_memory",
        }
    )


def openai_response(prompt, model):
    from openai import OpenAI

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=0,
    )
    return response.output_text

