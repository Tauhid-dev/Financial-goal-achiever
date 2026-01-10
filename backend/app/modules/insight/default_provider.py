from .provider import InsightProvider

class DeterministicProvider(InsightProvider):
    """
    Simple template‑based provider – no AI, no external calls.
    It builds a readable paragraph using only the data supplied.
    """

    def generate(self, financial_summary, goal_result) -> str:
        # Extract needed fields (keys are guaranteed by the caller)
        income = financial_summary.get("income", 0.0)
        surplus = financial_summary.get("surplus", 0.0)
        savings_rate = financial_summary.get("savings_rate", 0.0)

        required = goal_result.get("required_savings_per_month", 0.0)
        feasible = goal_result.get("feasible", False)

        # Build a deterministic explanation
        lines = [
            f"The family currently earns ${income:,.2f} per month.",
            f"After expenses, the monthly surplus is ${surplus:,.2f} "
            f"({savings_rate:.1f}% of income).",
        ]

        if feasible:
            lines.append(
                f"The goal is feasible: you need to save ${required:,.2f} each month, "
                f"which is within the available surplus."
            )
        else:
            lines.append(
                f"The goal is not feasible: you would need to save ${required:,.2f} each month, "
                f"which exceeds the current surplus by ${required - surplus:,.2f}."
            )

        # Simple actionable suggestion
        if not feasible:
            lines.append(
                "Consider reducing variable expenses or extending the time horizon "
                "to lower the required monthly savings."
            )
        else:
            lines.append(
                "You can proceed with the plan. Maintaining the current spending pattern "
                "should allow you to reach the target."
            )

        return " ".join(lines)
