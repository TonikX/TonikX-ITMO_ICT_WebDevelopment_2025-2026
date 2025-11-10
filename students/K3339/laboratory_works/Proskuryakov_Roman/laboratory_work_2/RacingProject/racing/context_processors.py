from .models import Participant

def participant_context(request):
    if not request.user.is_authenticated:
        return {}

    profile = getattr(request.user, "profile", None)
    if not profile:
        return {}

    # Ищем участника (если есть)
    participant = Participant.objects.filter(profile=profile).first()

    return {
        "participant": participant
    }
