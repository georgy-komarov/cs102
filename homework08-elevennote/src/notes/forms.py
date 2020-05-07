from django import forms

from .models import Note, Tag


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body']

    field_order = ['title', 'tags', 'body']

    tags = forms.CharField(label='Tags', widget=forms.TextInput(attrs={'data-role': 'tagsinput',
                                                                       'placeholder': 'Add a tag',
                                                                       'class': 'd-block w-25'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is not None:
            existing_tags = ','.join(map(str, self.instance.tags.all()))
            if existing_tags:
                self.fields['tags'].widget.attrs['value'] = existing_tags

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tags_list = tags.split(',')
        max_length = Tag._meta.get_field('name').max_length
        cleaned_tags = list(filter(lambda tag: 0 < len(tag) < max_length, tags_list))

        if len(cleaned_tags) != len(tags_list):
            raise forms.ValidationError(f'Tag name must not exceed {max_length} characters! '
                                        f'Please, remove these tags: {", ".join(set(tags_list) - set(cleaned_tags))}')
        return cleaned_tags

    def save(self, commit=True):
        instance = super().save(commit=commit)

        tags = self.cleaned_data.get('tags')
        instance.tags.clear()

        for tag in tags:
            tag, created = Tag.objects.get_or_create(name=tag)
            instance.tags.add(tag)

        instance.save()
        return instance
