def current_company(request):
    if request.user.is_authenticated:
        return {"current_company": getattr(request.user.profile, "company", None)}
    return {}
