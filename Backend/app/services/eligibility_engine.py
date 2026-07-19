def _to_bool(value):
    return str(value).strip().lower() in ("true", "yes", "1")


def rule_matches(rule, profile):
    """Evaluate a single generic EligibilityRule (rule_type/rule_value) against a profile dict."""
    rule_type = (rule.rule_type or "").strip().lower()
    rule_value = rule.rule_value

    if rule_type == "min_age":
        age = profile.get("age")
        return age is not None and age >= int(rule_value)

    if rule_type == "max_age":
        age = profile.get("age")
        return age is not None and age <= int(rule_value)

    if rule_type == "min_income":
        income = profile.get("annual_income")
        return income is not None and income >= float(rule_value)

    if rule_type == "max_income":
        income = profile.get("annual_income")
        return income is not None and income <= float(rule_value)

    if rule_type == "gender":
        gender = profile.get("gender")
        return rule_value.lower() == "any" or (gender is not None and gender.lower() == rule_value.lower())

    if rule_type == "state":
        state = profile.get("state")
        return rule_value.lower() == "all india" or (state is not None and state.lower() == rule_value.lower())

    if rule_type == "category":
        category = profile.get("category")
        return category is not None and category.lower() == rule_value.lower()

    if rule_type == "occupation":
        occupation = profile.get("occupation")
        return occupation is not None and occupation.lower() == rule_value.lower()

    if rule_type == "student":
        required = _to_bool(rule_value)
        return (not required) or bool(profile.get("is_student"))

    if rule_type == "disability":
        required = _to_bool(rule_value)
        return (not required) or bool(profile.get("has_disability"))

    # Unknown rule types don't block eligibility.
    return True


def evaluate_scheme_eligibility(scheme, profile):
    """Return (is_eligible, unmet_reasons, reason_text) for a scheme against a profile dict."""
    rules = list(scheme.eligibility_rules)

    if not rules:
        return True, [], "No eligibility criteria defined for this scheme"

    unmet_reasons = []
    for rule in rules:
        try:
            matched = rule_matches(rule, profile)
        except (TypeError, ValueError):
            matched = True  # malformed rule value never blocks eligibility

        if not matched:
            label = rule.rule_name or rule.rule_type
            unmet_reasons.append(f"Does not meet '{label}' requirement")

    is_eligible = len(unmet_reasons) == 0
    reason_text = "Eligible for this scheme" if is_eligible else "; ".join(unmet_reasons)

    return is_eligible, unmet_reasons, reason_text


def calculate_recommendation_score(scheme, profile):
    """Score 0-100 = percentage of the scheme's eligibility rules the profile satisfies."""
    rules = list(scheme.eligibility_rules)

    if not rules:
        return 60.0  # baseline score for schemes with no explicit eligibility criteria

    matched_count = 0
    for rule in rules:
        try:
            if rule_matches(rule, profile):
                matched_count += 1
        except (TypeError, ValueError):
            matched_count += 1

    return round((matched_count / len(rules)) * 100, 2)


def scheme_matches_search_filters(scheme, profile, active_rule_types):
    """
    For anonymous search: only evaluate eligibility rules whose type was
    explicitly constrained by the searcher (active_rule_types). Rule types
    the searcher didn't ask about never block a scheme from matching.
    """
    if not active_rule_types:
        return True

    for rule in scheme.eligibility_rules:
        rule_type = (rule.rule_type or "").strip().lower()
        if rule_type not in active_rule_types:
            continue
        try:
            if not rule_matches(rule, profile):
                return False
        except (TypeError, ValueError):
            continue

    return True


def build_profile_from_user(user):
    occupation = (user.occupation or "").strip().lower() if user.occupation else ""
    return {
        "age": user.calculate_age(),
        "gender": user.gender,
        "annual_income": float(user.annual_income) if user.annual_income is not None else None,
        "occupation": user.occupation,
        "state": user.state,
        "category": user.category,
        "is_student": occupation == "student",
        "has_disability": False,  # not tracked on the User model; unknown defaults to False
    }


def build_profile_from_search_args(args):
    age = args.get("age")
    income = args.get("income")

    return {
        "age": int(age) if age not in (None, "") else None,
        "gender": args.get("gender"),
        "annual_income": float(income) if income not in (None, "") else None,
        "occupation": args.get("occupation"),
        "state": args.get("state"),
        "category": args.get("category"),
        "is_student": _to_bool(args.get("student")) if args.get("student") is not None else None,
        "has_disability": _to_bool(args.get("disability")) if args.get("disability") is not None else None,
    }
