from django import forms


class EntrySearchForm(forms.Form):

    search = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'data_toggle': 'dropdown', 'placeholder': 'Search Entry...', 'id': 'search'})


class PostForm(forms.Form):

    title = forms.CharField(max_length=64, required=True)
    post = forms.CharField(required=True, widget=forms.Textarea)
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'name': "title", 'placeholder': "Title", "autocomplete": "false"})
        self.fields['image'].widget.attrs.update({'style': "margin-top: 30px"})
        self.fields['post'].widget.attrs.update({ 'oninput':'auto_height(this)', 'id': 'text', 'name': "post", 'placeholder': "Share your thoughts...", "autocomplete": "off"})
