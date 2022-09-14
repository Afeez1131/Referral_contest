from django import template
from django.utils import timezone
register = template.Library()


@register.filter
def get_time(contest):
    if (timezone.now() >= contest.starting_date) and (contest.ending_date > timezone.now()):
        return "Active"
    elif timezone.now() > contest.ending_date:
        return "Ended"
    elif not (timezone.now() >= contest.starting_date) and (contest.ending_date > timezone.now()):
        return "Not Yet Time"


