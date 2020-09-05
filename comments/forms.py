from django.forms import ModelForm
from .models import Comment


class FormComment(ModelForm):
    def clean(self):
        data = self.cleaned_data
        author = data.get('author')
        email = data.get('email')
        comment = data.get('comment')

        if len(author) < 5:
            self.add_error(
                'author', 'Author must be at least 5 characters.'
            )

        if not email:
            self.add_error(
                'email', 'Email is required.'
            )

        if not email:
            self.add_error(
                'comment', 'Comment is required.'
            )


    class Meta:
        model = Comment
        fields = ('author', 'email', 'comment')
