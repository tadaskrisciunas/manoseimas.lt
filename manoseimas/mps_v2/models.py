from django.db import models
from autoslug import AutoSlugField

from django.utils.translation import ugettext_lazy as _

from sboard.models import NodeForeignKey


class CrawledItem(models.Model):
    source = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def get_mp_full_name(mp):
    return mp.full_name


class ParliamentMember(CrawledItem):
    slug = AutoSlugField(populate_from=get_mp_full_name)
    source_id = models.CharField(max_length=16)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.CharField(max_length=16, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    candidate_page = models.URLField(blank=True, null=True)
    raised_by = models.ForeignKey('PoliticalParty', blank=True, null=True)
    photo = models.ImageField(upload_to='profile_images',
                              blank=True, null=True)
    term_of_office = models.CharField(max_length=32, blank=True, null=True)

    office_address = models.TextField(blank=True, null=True)
    constituency = models.CharField(max_length=128, blank=True, null=True)
    party_candidate = models.BooleanField(default=True)
    groups = models.ManyToManyField('Group', through='GroupMembership',
                                    related_name='members')

    biography = models.TextField(blank=True, null=True)

    @property
    def full_name(self):
        return u' '.join([self.first_name, self.last_name])

    def __unicode__(self):
        return self.full_name

    @property
    def fractions(self):
        return self.groups.filter(type=Group.TYPE_FRACTION)

    @property
    def other_group_memberships(self):
        # Not fraction groups
        return GroupMembership.objects.filter(member=self)\
            .exclude(group__type=Group.TYPE_FRACTION).select_related('group')

    def get_statement_count(self):
        return self.statements.filter(as_chairperson=False).count()

    def get_long_statement_count(self):
        return self.statements.filter(as_chairperson=False).\
            filter(word_count__gte=50).count()

    def get_discussion_contribution_percentage(self):
        all_discussions = StenogramTopic.objects.count()
        contributed_discusions = StenogramStatement.objects.\
            filter(speaker=self, as_chairperson=False).\
            aggregate(topics=models.Count('topic_id',
                                          distinct=True))
        return (float(contributed_discusions['topics'])
                / all_discussions * 100.0) if all_discussions else 0.0

    @property
    def votes(self):
        # Avoiding circular imports
        from manoseimas.votings.models import get_mp_votes
        return get_mp_votes(self.source_id)

    @property
    def all_statements(self):
        return self.statements.all()


class PoliticalParty(CrawledItem):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Group(CrawledItem):
    TYPE_GROUP = 'group'
    TYPE_COMMITTEE = 'committee'
    TYPE_COMMISSION = 'commission'
    TYPE_FRACTION = 'fraction'
    TYPE_PARLIAMENT = 'parliament'

    GROUP_TYPES = (
        (TYPE_GROUP, _('Group')),
        (TYPE_COMMITTEE, _('Committee')),
        (TYPE_COMMISSION, _('Commission')),
        (TYPE_FRACTION, _('Fraction')),
        (TYPE_PARLIAMENT, _('Parliament')),
    )

    name = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from='name')
    type = models.CharField(max_length=64,
                            choices=GROUP_TYPES)

    class Meta:
        unique_together = (('name', 'type'))

    def __unicode__(self):
        return u'{} ({})'.format(self.name, self.type)

    @property
    def active_members(self):
        return self.members.filter(groupmembership__until=None)


class GroupMembership(CrawledItem):
    member = models.ForeignKey(ParliamentMember)
    group = models.ForeignKey(Group)
    position = models.CharField(max_length=128)
    since = models.DateField(blank=True, null=True)
    until = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'{} - {} ({})'.format(self.group.name,
                                      self.member.full_name,
                                      self.position)


class Stenogram(CrawledItem):
    source_id = models.CharField(max_length=16, db_index=True)
    date = models.DateField()
    sitting_no = models.IntegerField()
    sitting_name = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'{} Nr. {}'.format(self.date, self.sitting_no)


class StenogramTopic(CrawledItem):
    stenogram = models.ForeignKey(Stenogram, related_name='topics')
    title = models.TextField()
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return self.title[:160]


class StenogramStatement(CrawledItem):
    topic = models.ForeignKey(StenogramTopic, related_name='statements')
    speaker = models.ForeignKey(ParliamentMember, related_name='statements',
                                blank=True, null=True)
    speaker_name = models.CharField(max_length=64)
    as_chairperson = models.BooleanField(default=False)
    text = models.TextField()
    word_count = models.PositiveIntegerField(default=0)

    def get_speaker_name(self):
        return self.speaker.full_name if self.speaker else self.speaker_name

    def __unicode__(self):
        return u'{}: {}'.format(self.get_speaker_name(), self.text[:160])


class Voting(models.Model):
    stenogram_topic = models.ForeignKey(StenogramTopic, related_name='votings')
    node = NodeForeignKey()
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ('stenogram_topic', 'node')


class Ranking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    votes_rank = models.IntegerField(default=0)
    statement_count_rank = models.IntegerField(default=0)
    long_statement_count_rank = models.IntegerField(default=0)
    discusion_contribution_percentage_rank = models.IntegerField(default=0)

    class Meta:
        abstract = True


class MPRanking(Ranking):
    target = models.OneToOneField(ParliamentMember,
                                  related_name='ranking')


class GroupRanking(Ranking):
    target = models.OneToOneField(Group,
                                  related_name='ranking')
