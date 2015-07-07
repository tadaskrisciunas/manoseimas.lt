from django.shortcuts import render
from django.db.models import Prefetch
from django.utils.safestring import mark_safe

from manoseimas.mps_v2.models import ParliamentMember, GroupMembership, Group


def mp_profile(request, mp_slug):
    mp_qs = ParliamentMember.objects.select_related('ranking', 'raised_by')

    mp_qs = mp_qs.prefetch_related(
        Prefetch(
            'groupmembership',
            queryset=GroupMembership.objects.select_related('group').filter(
                until=None,
                group__type__in=(Group.TYPE_COMMITTEE,
                                 Group.TYPE_COMMISSION),
                group__displayed=True
            ),
            to_attr='committees'))
    mp_qs = mp_qs.prefetch_related(
        Prefetch(
            'groupmembership',
            queryset=GroupMembership.objects.select_related('group').filter(
                until=None,
                group__type=Group.TYPE_GROUP,
                group__displayed=True),
            to_attr='other_groups'))
    mp_qs = mp_qs.prefetch_related(ParliamentMember.FractionPrefetch())
    mp = mp_qs.get(slug=mp_slug)

    mp_qs = mp_qs.prefetch_related(
        Prefetch(
            'groupmembership',
            queryset=GroupMembership.objects.select_related('group').filter(
                group__type=Group.TYPE_FRACTION,
                group__displayed=True).order_by('-since'),
            to_attr='all_fractions'))
    mp = mp_qs.get(slug=mp_slug)

    profile = {'full_name': mp.full_name}
    if mp.fraction:
        profile["fraction_name"] = mp.fraction.name
        profile["fraction_slug"] = mp.fraction.slug
    else:
        profile["fraction_name"] = None

    profile['raised_by'] = mp.raised_by.name if mp.raised_by else None
    profile['office_address'] = mp.office_address
    profile['constituency'] = mp.constituency
    profile['slug'] = mp_slug

    top_collaborators = mp.top_collaborators.prefetch_related(
        ParliamentMember.FractionPrefetch()
    )

    stats = {
        'statement_count': mp.statement_count,
        'long_statement_count': mp.long_statement_count,
        'long_statement_percentage': mp.get_long_statement_percentage,
        'contributed_discussion_percentage':
            mp.discussion_contribution_percentage,
        'votes': mp.votes,
        'vote_percent': mp.vote_percentage,
        'proposed_projects': mp.proposed_law_project_count,
        'passed_projects': mp.passed_law_project_count,
        'passed_project_percentage': mp.passed_law_project_ratio,
    }

    context = {
        'profile': profile,
        'positions': mp.positions,
        'groups': mp.other_groups,
        'all_fractions': mp.all_fractions,
        'committees': mp.committees,
        'biography': mark_safe(mp.biography),
        'stats': stats,
        'photo_url': mp.photo.url,
        'ranking': mp.ranking,
        'top_collaborating_mps': top_collaborators,
    }

    return render(request, 'profile.jade', context)
