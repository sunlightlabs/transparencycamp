from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_delete

ALLOW_ALL, REQUIRE_LOGIN, DISALLOW_ALL = range(3)
SUBSITE_POST_STATUS = (
    (ALLOW_ALL, 'Allow All Posts'),
    (REQUIRE_LOGIN, 'Require Login'),
    (DISALLOW_ALL, 'Allow No Posts'),
)

TOTAL, FRECENCY = range(2)
SCORING_CHOICES = (
    (TOTAL, 'Total Score'),
    (FRECENCY, 'Frecency'),
)


class Subsite(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    scoring_algorithm = models.IntegerField(default=TOTAL, choices=SCORING_CHOICES)
    post_status = models.IntegerField(default=ALLOW_ALL, choices=SUBSITE_POST_STATUS)

    theme = models.CharField(help_text='name of base theme template', max_length=100)

    idea_label = models.CharField(max_length=128, default="idea", help_text="The lowercase name by which ideas are referenced in this subsite.")
    ideas_per_page = models.IntegerField(default=10)
    upvote_label = models.CharField(max_length=255, default="Vote Up", help_text="The text of the button to upvote. HTML allowed.")
    upvotes_label = models.CharField(max_length=255, blank=True, default="{} Up", help_text="The text of the indicator of the current number of upvotes. '{}' will be substituted with the number. HTML allowed.")
    allow_downvote = models.BooleanField(default=True)
    downvote_label = models.CharField(max_length=255, default="Vote Down", help_text="The text of the button to downvote. HTML allowed.")
    downvotes_label = models.CharField(max_length=255, blank=True, default="{} Down", help_text="The text of the indicator of the current number of downvotes. '{}' will be substituted with the number. HTML allowed.")
    voted_label = models.CharField(max_length=255, default="Clear Vote", help_text="HTML allowed.")

    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ideas_popular', args=[self.slug])

    def user_can_post(self, user):
        if self.post_status == DISALLOW_ALL:
            return False
        elif self.post_status == ALLOW_ALL:
            return True
        elif self.post_status == REQUIRE_LOGIN:
            return not user.is_anonymous()

    def max_vote_count(self):
        return self.ideas.annotate(num_votes=models.Count('votes')).order_by('-num_votes')[0].num_votes


class IdeaManager(models.Manager):

    def with_user_vote(self, user):
        return self.extra(select={'user_vote': 'SELECT value FROM brainstorm_vote WHERE idea_id=brainstorm_idea.id AND user_id=%s'}, select_params=[user.id])


class Idea(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=75, help_text="Will not be published.")
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    score = models.IntegerField(default=0)

    timestamp = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, null=True, related_name='ideas')
    subsite = models.ForeignKey(Subsite, related_name='ideas')

    objects = IdeaManager()

    class Meta:
        ordering = ('-score',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('idea_detail', args=[self.subsite_id, self.id])

    def calculate_score(self):
        if self.subsite.scoring_algorithm is FRECENCY:
            raise NotImplementedError('Frecency isn\'t ready yet :`(')
        else:
            try:
                score = self.votes.aggregate(score=models.Sum('value'))['score'] or 0
                upvotes = self.votes.up().count()
                downvotes = self.votes.down().count()
                return (score, upvotes, downvotes)
            except:
                return (0, 0, 0)


class VoteManager(models.Manager):
    def up(qs):
        return qs.filter(value=1)

    def down(qs):
        return qs.filter(value=-1)


class Vote(models.Model):
    user = models.ForeignKey(User, related_name='idea_votes')
    idea = models.ForeignKey(Idea, related_name='votes')
    value = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    objects = VoteManager()

    def __unicode__(self):
        return '%s %s on %s' % (self.user, self.value, self.idea)

    class Meta:
        unique_together = (('user', 'idea'),)
        ordering = ('-timestamp',)


def update_idea_votes(sender, instance, *args, **kwargs):
    idea = instance.idea
    (idea.score,
     idea.upvotes,
     idea.downvotes) = idea.calculate_score()
    idea.save()

post_save.connect(update_idea_votes, sender=Vote)
post_delete.connect(update_idea_votes, sender=Vote)
