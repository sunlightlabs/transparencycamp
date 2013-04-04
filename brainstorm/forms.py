from akismet import Akismet
from django.forms import ModelForm, ValidationError
from django.conf import settings
from brainstorm.models import Idea


class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'name', 'email', 'description',)

    def __init__(self, request, *args, **kwargs):
        super(IdeaForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean(self):
        request = self.request
        ak = Akismet(settings.AKISMET_KEY, 'http://transparencycamp.org/ideas/')
        ak.verify_key()
        if ak.comment_check(self.cleaned_data.get('description').decode('ascii', 'ignore'), {
                'comment_author': self.cleaned_data.get('name').decode('ascii', 'ignore'),
                'comment_author_email': self.cleaned_data.get('email'),
                'user_ip': request.META.get('HTTP_X_FOWARDED_FOR', request.META['REMOTE_ADDR']),
                'user_agent': request.META.get('HTTP_USER_AGENT'), }):
            raise ValidationError("Your submission contained known spam.")
        return super(IdeaForm, self).clean()
