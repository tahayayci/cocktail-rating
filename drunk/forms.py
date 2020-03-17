from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CocktailReview, Cocktail, CocktailGroup

User = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""


class RatingForm(forms.ModelForm):
    class Meta:
        model = CocktailReview
        fields = ('taste_star', 'cost_star', 'prep_hardness_star', 'notes')

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        self.fields['taste_star'].label = "Taste"
        self.fields['cost_star'].label = "Cost"
        self.fields['prep_hardness_star'].label = "Preparation Hardness"


class CocktailForm(forms.ModelForm):
    class Meta:
        model = Cocktail
        fields = ('name', 'recipe', 'picture', 'group', 'is_alcoholic')
        widgets = {
            'recipe': forms.Textarea(attrs={'rows': 5}),
        }
