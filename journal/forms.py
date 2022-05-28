from django import forms


class EntrySearchForm(forms.Form):

    search = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'data_toggle': 'dropdown', 'placeholder': 'Search Entry...', 'id': 'search'})
