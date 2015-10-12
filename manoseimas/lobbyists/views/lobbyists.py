# -*-coding: utf-8 -*-

from django.shortcuts import render
from manoseimas.lobbyists.models import Lobbyist

def lobbyist_list(request):
    """A placeholder."""
    lobbyists = Lobbyist.objects.all()
    return render(request, 'lobbyist_list.jade', {lobbyists: lobbyists})


def lobbyist_profile(request, lobbyist_slug):
    """A profile view for a lobbyist."""

    context = {
        'name': 'Name: ' + lobbyist_slug,
    }

    return render(request, 'lobbyist_profile.jade', context)

