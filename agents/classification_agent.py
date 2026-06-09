def classify_incident(description):

    description = description.lower()

    if "payment" in description:
        return {
            "severity": "Critical",
            "business_impact": "Revenue Loss"
        }

    elif "memory leak" in description:
        return {
            "severity": "High",
            "business_impact": "Performance Degradation"
        }

    elif "timeout" in description:
        return {
            "severity": "High",
            "business_impact": "Service Disruption"
        }

    else:
        return {
            "severity": "Low",
            "business_impact": "Minor Issue"
        }