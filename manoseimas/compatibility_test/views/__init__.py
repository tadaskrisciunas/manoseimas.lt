# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from manoseimas.compatibility_test.models import CompatTest
from manoseimas.compatibility_test.models import Topic


def topics_all():
        qs = Topic.objects.all()
        test = get_current_test()
        qs = qs.filter(groups__test=test)
        qs = qs.prefetch_related('groups', 'arguments')

        topics = []
        for topic in qs:
            arguments = topic.arguments.all().values(
                'id', 'name', 'description', 'supporting'
            )
            topic_votings = topic.topicvoting_set.all().values(
                'voting__id', 'voting__name', 'voting__source', 'factor',
            )
            votings = [
                {
                    'id': tv['voting__id'],
                    'name': tv['voting__name'],
                    'url': tv['voting__source'],
                    'factor': tv['factor'],
                }
                for tv in topic_votings
            ]
            topics.append({
                'id': topic.id,
                'name': topic.name,
                'group': topic.groups.first().name,
                'description': topic.description,
                'arguments': list(arguments),
                'votings': votings,
            })
        # TODO: randomise by group #153
        return topics


def get_current_test():
    return CompatTest.objects.first()


class IndexView(View):
    template_name = 'start_test.jade'

    def topics(self):
        return topics_all()

    def get(self, request):
        context = {
            'topics': self.topics(),
            'title': 'Seimo rinkimai 2016',
        }
        return render(request, self.template_name, context)


def topics_json(request):
    topics = topics_all()
    return JsonResponse({'items': topics})


class ResultsView(View):
    template_name = 'results.jade'

    def get(self, request):
        context = {
            'title': 'Seimo rinkimai 2016',
        }
        return render(request, self.template_name, context)
