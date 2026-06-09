from agents.classification_agent import classify_incident

def generate_investigation(
    incident_description,
    github_data
):

    classification = classify_incident(
        incident_description
    )

    timeline = [
        "Investigation Started",
        f"Commit Detected: {github_data['commit_message']}",
        f"Severity Classified: {classification['severity']}"
    ]

    return {
        "severity": classification["severity"],
        "business_impact": classification["business_impact"],
        "root_cause": github_data["commit_message"],
        "timeline": timeline
    }