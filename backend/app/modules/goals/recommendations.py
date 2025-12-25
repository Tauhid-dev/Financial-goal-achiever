from .schema import SavingsGoal
from .projection import project_time_to_goal

def recommend_adjustments(goal: SavingsGoal) -> list[str]:
    """
    Generate simple rule‑based suggestions to improve goal achievability.
    - If the goal is not achievable, suggest increasing monthly contribution.
    - If achievable, suggest how many months could be saved by increasing contribution
      by $200 or reducing expenses by 10 %.
    Returns a list of human‑readable recommendation strings.
    """
    recommendations = []
    proj = project_time_to_goal(goal)

    if not proj["is_achievable"]:
        recommendations.append(
            "Increase monthly contribution above 0 to make the goal achievable."
        )
        return recommendations

    # Suggest a $200 increase in contribution
    increased = goal.monthly_contribution + 200
    if increased > 0:
        temp_goal = SavingsGoal(
            id=goal.id,
            name=goal.name,
            target_amount=goal.target_amount,
            current_amount=goal.current_amount,
            monthly_contribution=increased,
            target_date=goal.target_date,
        )
        new_proj = project_time_to_goal(temp_goal)
        months_saved = proj["months_required"] - new_proj["months_required"]
        if months_saved > 0:
            recommendations.append(
                f"Increase monthly savings by $200 to reach the goal {months_saved} month(s) earlier."
            )

    # Suggest a 10 % expense reduction (treated as extra contribution)
    extra_from_expenses = goal.monthly_contribution * 0.10
    temp_goal = SavingsGoal(
        id=goal.id,
        name=goal.name,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        monthly_contribution=goal.monthly_contribution + extra_from_expenses,
        target_date=goal.target_date,
    )
    new_proj = project_time_to_goal(temp_goal)
    months_saved = proj["months_required"] - new_proj["months_required"]
    if months_saved > 0:
        recommendations.append(
            f"Reduce expenses by 10 % (≈${extra_from_expenses:.2f} extra savings) to reach the goal {months_saved} month(s) earlier."
        )

    return recommendations
