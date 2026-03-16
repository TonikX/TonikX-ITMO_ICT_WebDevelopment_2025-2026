from django import template

register = template.Library()

@register.filter
def format_lap_time(duration):
    if duration:
        total_seconds = int(duration.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        milliseconds = int((duration.total_seconds() - total_seconds) * 1000)
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    return "-"