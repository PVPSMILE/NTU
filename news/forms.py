from news.models import PublicationModel,Tags,Status
from django.forms import ModelForm, TextInput, PasswordInput, CheckboxInput, Textarea, FileInput, NumberInput,BaseForm,Form
from django import forms
class PublicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PublicationForm, self).__init__(*args, **kwargs)
        self.fields["review"].required = True
    class Meta:
        model = PublicationModel
        exclude = ('name', 'discription','title_image', 'author', 'date_of_create','time_of_create','date_of_update','time_of_update','tags','status','type')
        fields = ['review']
        widgets = {
            "review": Textarea(attrs={
                "class": "form-control",
                "type": "text",
                "id": "Review",
                "name": "Review"
            }),
        }
class ArticleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields["tags"] = forms.ModelChoiceField(queryset=Tags.objects.all())
        self.fields["name"] = forms.CharField(label="Title",widget=TextInput(attrs={
                "class": "form-control",
                "type": "text",
                "id": "discription",
                "name": "discription"
            }),)
    class Meta:
        model = PublicationModel
        fields = ['name','discription','tags','title_image']
        widgets = {
            "discription": Textarea(attrs={
                "class": "form-control",
                "type": "text",
                "id": "discription",
                "name": "discription"
            }),
        }
class NewsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['status'] = forms.ModelChoiceField(queryset=Status.objects.all())
        self.fields["review"].required = True
    class Meta:
        model = PublicationModel
        exclude = ('name', 'discription', 'title_image', 'author', 'date_of_create', 'time_of_create', 'date_of_update','time_of_update', 'tags','type')
        fields = ['status','review']
        widgets = {
            'review': Textarea(attrs={
                "class": "form-control",
                "type": "text",
                "id": 'review',
                "name": 'review'
            }),
        }
class AccountForm(Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "type": "text",
        "id": "Reason",
        "name": "Reason"
    }))