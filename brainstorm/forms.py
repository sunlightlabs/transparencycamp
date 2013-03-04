from django.forms import ModelForm
from brainstorm.models import Idea


class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'name', 'email', 'description',)
