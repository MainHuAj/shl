"""
Evaluates the agent against all 10 sample conversations.
Usage: python eval2.py
"""

import requests
import time

BASE_URL = "https://shl-production-a1a8.up.railway.app/chat"

CONVERSATIONS = [
    {
        "name": "C1 - Senior Leadership OPQ",
        "turns": [
            "We need a solution for senior leadership.",
            "The pool consists of CXOs, director-level positions; people with more than 15 years of experience.",
            "Selection — comparing candidates against a leadership benchmark.",
            "Perfect, that's what we need.",
        ],
        "expected_urls": [
            "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
            "https://www.shl.com/products/product-catalog/view/opq-universal-competency-report-2-0/",
            "https://www.shl.com/products/product-catalog/view/opq-leadership-report/",
        ],
    },
    {
        "name": "C2 - Senior Rust Engineer",
        "turns": [
            "I'm hiring a senior Rust engineer for high-performance networking infrastructure. What assessments should I use?",
            "Yes, go ahead. Should I also add a cognitive test for this level?",
            "That works. Thanks.",
        ],
        "expected_urls": [
            "https://www.shl.com/products/product-catalog/view/smart-interview-live-coding/",
            "https://www.shl.com/products/product-catalog/view/linux-programming-general/",
            "https://www.shl.com/products/product-catalog/view/networking-and-implementation-new/",
            "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-g/",
            "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
        ],
    },
    {
        "name": "C3 - Contact Centre Agents",
        "turns": [
            "We're screening 500 entry-level contact centre agents. Inbound calls, customer service focus. What should we use?",
            "English.",
            "US.",
            "Is the Contact Center Call Simulation different from the Customer Service Phone Simulation?",
            "Perfect — new simulation for volume, old solution for finalists. Confirmed.",
        ],
        "expected_urls": [
            "https://www.shl.com/products/product-catalog/view/svar-spoken-english-us-new/",
            "https://www.shl.com/products/product-catalog/view/contact-center-call-simulation-new/",
            "https://www.shl.com/products/product-catalog/view/entry-level-customer-serv-retail-and-contact-center/",
            "https://www.shl.com/products/product-catalog/view/customer-service-phone-simulation/",
        ],
    },
    {
        "name": "C4 - Graduate Financial Analysts",
        "turns": [
            "Hiring graduate financial analysts — final-year students, no work experience. We need numerical reasoning and a finance knowledge test.",
            "Good. Can you also add a situational judgement element — work-context decision making for graduates?",
            "That covers it. Numerical + Graduate Scenarios as first filter, domain tests for shortlisted candidates.",
        ],
        "expected_urls": [
            "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-numerical-reasoning/",
            "https://www.shl.com/products/product-catalog/view/financial-accounting-new/",
            "https://www.shl.com/products/product-catalog/view/basic-statistics-new/",
            "https://www.shl.com/products/product-catalog/view/graduate-scenarios/",
            "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
        ],
    },
    {
        "name": "C5 - Sales Reskilling",
        "turns": [
            "As part of our restructuring and annual talent audit, we need to re-skill our Sales organization. What solutions do you recommend?",
            "What's the difference between OPQ and OPQ MQ Sales Report?",
            "Clear. We'll use OPQ for everyone and add MQ only where we want motivators in the Sales Report; keeping the five solutions as our audit stack.",
        ],
        "expected_urls": [
            "https://www.shl.com/products/product-catalog/view/global-skills-assessment/",
            "https://www.shl.com/products/product-catalog/view/global-skills-development-report/",
            "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
            "https://www.shl.com/products/product-catalog/view/opq-mq-sales-report/",
            "https://www.shl.com/products/product-catalog/view/salestransformationreport2-0-individualcontributor/",
        ],
    },
    {
        "name": "C6 - Plant Operators Safety",
        "turns": [
            "We're hiring plant operators for a chemical facility. Safety is absolute top priority — reliability, procedure compliance, never cutting corners. What do you recommend?",
            "What's the difference between the DSI and the Safety and Dependability 8.0?",
            "We're industrial. The 8.0 bundle is the right fit. Confirmed.",
        ],
        "expected_urls": [
            "https://www.shl.com/products/product-catalog/view/safety-and-dependability-focus-8-0/",
            "https://www.shl.com/products/product-catalog/view/workplace-health-and-safety-new/",
        ],
    },
    {
        "name": "C7 - Bilingual Healthcare Admin",
        "turns": [
            "We're hiring bilingual healthcare admin staff in South Texas — they handle patient records and need to be assessed in Spanish. HIPAA compliance is critical. What assessments work?",
            "They're functionally bilingual — English fluent for written work. Go with the hybrid.",
            "Are we legally required under HIPAA to test all staff who touch patient records? And does this SHL test satisfy that requirement?",
            "Understood. Keep the shortlist as-is.",
        ],
        "expected_urls": [
            "https://www.shl.com/products/product-catalog/view/hipaa-security/",
            "https://www.shl.com/products/product-catalog/view/medical-terminology-new/",
            "https://www.shl.com/products/product-catalog/view/microsoft-word-365-essentials-new/",
            "https://www.shl.com/products/product-catalog/view/dependability-and-safety-instrument-dsi/",
            "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
        ],
    },
    {
        "name": "C8 - Admin Assistants Excel Word",
        "turns": [
            "I need to quickly screen admin assistants for Excel and Word daily.",
            "In that case, I am OK with adding a simulation - we want to capture the capabilities.",
            "That's good.",
        ],
        "expected_urls": [
            "https://www.shl.com/products/product-catalog/view/microsoft-excel-365-new/",
            "https://www.shl.com/products/product-catalog/view/microsoft-word-365-new/",
            "https://www.shl.com/products/product-catalog/view/ms-excel-new/",
            "https://www.shl.com/products/product-catalog/view/ms-word-new/",
            "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
        ],
    },
    {
        "name": "C9 - Senior Full Stack Engineer",
        "turns": [
            "Here's the JD: Senior Full-Stack Engineer — 5+ years across Core Java, Spring, REST API design, Angular, SQL/relational databases, AWS deployment, and Docker.",
            "Backend-leaning. Day-one priorities are Core Java and Spring; SQL is constant. Angular is occasional.",
            "Senior IC. They lead design on their own services but don't manage other engineers directly.",
            "Add AWS and Docker. Drop REST.",
            "Keep Verify G+. Locking it in.",
        ],
        "expected_urls": [
            "https://www.shl.com/products/product-catalog/view/core-java-advanced-level-new/",
            "https://www.shl.com/products/product-catalog/view/spring-new/",
            "https://www.shl.com/products/product-catalog/view/sql-new/",
            "https://www.shl.com/products/product-catalog/view/amazon-web-services-aws-development-new/",
            "https://www.shl.com/products/product-catalog/view/docker-new/",
            "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-g/",
            "https://www.shl.com/products/product-catalog/view/occupational-personality-questionnaire-opq32r/",
        ],
    },
    {
        "name": "C10 - Graduate Management Trainee",
        "turns": [
            "We run a graduate management trainee scheme. We need a full battery — cognitive, personality, and situational judgement. All recent graduates.",
            "But can you remove the OPQ32r and replace it with something shorter? Candidates complain it takes too long.",
            "Drop the OPQ. Final list: Verify G+ and Graduate Scenarios.",
        ],
        "expected_urls": [
            "https://www.shl.com/products/product-catalog/view/shl-verify-interactive-g/",
            "https://www.shl.com/products/product-catalog/view/graduate-scenarios/",
        ],
    },
]


def call_chat(messages: list) -> dict:
    try:
        response = requests.post(BASE_URL, json={"messages": messages}, timeout=35)
        if response.status_code != 200:
            print(f"    HTTP {response.status_code}: {response.text[:100]}")
            return None
        return response.json()
    except Exception as e:
        print(f"    Request error: {e}")
        return None


def validate_schema(data: dict) -> bool:
    if not isinstance(data, dict):
        return False
    if "reply" not in data or not isinstance(data["reply"], str):
        return False
    if "recommendations" not in data or not isinstance(data["recommendations"], list):
        return False
    if "end_of_conversation" not in data or not isinstance(data["end_of_conversation"], bool):
        return False
    for rec in data["recommendations"]:
        if not all(k in rec for k in ["name", "url", "test_type"]):
            return False
    return True


def run_conversation(conv: dict) -> dict:
    messages = []
    final_recommendations = []
    schema_errors = 0
    turns_used = 0
    turn_times = []

    for user_turn in conv["turns"]:
        messages.append({"role": "user", "content": user_turn})
        turns_used += 1

        turn_start = time.time()
        data = call_chat(messages)
        turn_time = time.time() - turn_start
        turn_times.append(turn_time)

        if data is None:
            schema_errors += 1
            messages.append({"role": "assistant", "content": "I encountered an error."})
            continue

        if not validate_schema(data):
            schema_errors += 1
            print(f"    Schema error on turn {turns_used}: {str(data)[:100]}")
            messages.append({"role": "assistant", "content": "I encountered an error."})
            continue

        messages.append({"role": "assistant", "content": data["reply"]})

        if data["recommendations"]:
            final_recommendations = data["recommendations"]

        if data["end_of_conversation"]:
            break

        time.sleep(0.3)

    return {
        "final_recommendations": final_recommendations,
        "turns_used": turns_used,
        "schema_errors": schema_errors,
        "max_turn_time": max(turn_times) if turn_times else 0,
        "total_time": sum(turn_times),
    }


def recall_at_k(predicted_urls: list, expected_urls: list) -> float:
    if not expected_urls:
        return 0.0
    predicted_set = set(predicted_urls)
    hits = sum(1 for url in expected_urls if url in predicted_set)
    return hits / len(expected_urls)


def evaluate():
    print("=" * 60)
    print("SHL RECOMMENDER EVALUATION")
    print(f"Endpoint: {BASE_URL}")
    print("=" * 60)

    total_recall = 0.0
    total_schema_errors = 0
    results = []

    for conv in CONVERSATIONS:
        print(f"\n▶ {conv['name']}")
        result = run_conversation(conv)

        predicted_urls = [r["url"] for r in result["final_recommendations"]]
        recall = recall_at_k(predicted_urls, conv["expected_urls"])
        total_recall += recall
        total_schema_errors += result["schema_errors"]

        print(f"  Turns used     : {result['turns_used']}")
        print(f"  Recommendations: {len(result['final_recommendations'])}")
        print(f"  Recall@10      : {recall:.2f}")
        print(f"  Total time     : {result['total_time']:.1f}s")
        print(f"  Max turn time  : {result['max_turn_time']:.1f}s {'⚠ SLOW' if result['max_turn_time'] > 25 else '✓'}")

        if result["schema_errors"] > 0:
            print(f"  Schema errors  : {result['schema_errors']}")

        if recall < 1.0:
            missing = [
                u.split("view/")[1].rstrip("/")
                for u in conv["expected_urls"]
                if u not in set(predicted_urls)
            ]
            print(f"  Missing        : {missing}")

        results.append({
            "name": conv["name"],
            "recall": recall,
            "turns": result["turns_used"],
            "schema_errors": result["schema_errors"],
            "max_turn_time": result["max_turn_time"],
        })

    mean_recall = total_recall / len(CONVERSATIONS)
    max_overall = max(r["max_turn_time"] for r in results)

    print("\n" + "=" * 60)
    print(f"MEAN RECALL@10     : {mean_recall:.3f}")
    print(f"TOTAL SCHEMA ERRORS: {total_schema_errors}")
    print(f"MAX TURN TIME      : {max_overall:.1f}s {'⚠ RISK' if max_overall > 25 else '✓ OK'}")
    print("=" * 60)


if __name__ == "__main__":
    evaluate()