from datetime import datetime

from django.conf import settings

from project.kiwipycon.sponsor.models import Sponsor

def sponsors(request):
    sponsors = Sponsor.objects.all()
    gold_sponsors = sponsors.filter(type='gold')
    silver_sponsors = sponsors.filter(type='silver')
    schwag_sponsors = sponsors.filter(type='schwag')
    return {
            'sponsors': {'gold': gold_sponsors,
                         'silver': silver_sponsors,
                         'schwag': schwag_sponsors}
    }

