from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.db.models.functions import Round
from django.db.models import Avg, Count
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render

from .forms import RegisterForm, RatingForm, CocktailForm
from .models import Cocktail, CocktailReview

User = get_user_model()


def user_is_not_logged_in(user):
    return not user.is_authenticated


@user_passes_test(user_is_not_logged_in, login_url='home')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            registration = form.save(commit=False)
            registration.is_expert = False
            registration.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        cocktails = Cocktail.objects.filter(
            is_active=1
        ).annotate(
            avg_taste=Round(Avg('cocktailreview__taste_star')),
            avg_cost=Round(Avg('cocktailreview__cost_star')),
            avg_prep=Round(Avg('cocktailreview__prep_hardness_star'))
        ).order_by('name')

        # avg_expert = Cocktail.objects.filter(
        #     is_active=1, cocktailreview__user__is_expert=1, cocktailreview__user__is_active=1
        # ).annotate(
        #     avg_taste=Avg('cocktailreview__taste_star'),
        #     count_taste=Count('cocktailreview__taste_star'),
        #     avg_cost=Avg('cocktailreview__cost_star'),
        #     count_cost=Count('cocktailreview__cost_star'),
        #     avg_prep=Avg('cocktailreview__prep_hardness_star'),
        #     count_prep=Avg('cocktailreview__prep_hardness_star')
        # )
        #
        # avg_norm = Cocktail.objects.filter(
        #     is_active=1, cocktailreview__user__is_expert=0, cocktailreview__user__is_active=1
        # ).annotate(
        #     avg_taste=Avg('cocktailreview__taste_star'),
        #     count_taste=Count('cocktailreview__taste_star'),
        #     avg_cost=Avg('cocktailreview__cost_star'),
        #     count_cost=Count('cocktailreview__cost_star'),
        #     avg_prep=Avg('cocktailreview__prep_hardness_star'),
        #     count_prep=Avg('cocktailreview__prep_hardness_star')
        # )

        return render(request, self.template_name, {'cocktails': cocktails})


def search(request):
    search_word = request.GET.get('search')

    if search_word is not None and search_word != '' and len(search_word) >= 3:

        cocktails = Cocktail.objects.filter(
            name__icontains=search, is_active=1
        ).annotate(
            avg_taste=Round(Avg('cocktailreview__taste_star')),
            avg_cost=Round(Avg('cocktailreview__cost_star')),
            avg_prep=Round(Avg('cocktailreview__prep_hardness_star'))
        ).order_by('name')

    else:

        cocktails = Cocktail.objects.annotate(
            avg_taste=Round(Avg('cocktailreview__taste_star')),
            avg_cost=Round(Avg('cocktailreview__cost_star')),
            avg_prep=Round(Avg('cocktailreview__prep_hardness_star'))
        ).filter(is_active=1).order_by('name')

    return render(request, 'results.html', {'cocktails': cocktails})


class RateView(LoginRequiredMixin, View):
    form_class = RatingForm
    template_name = 'rate.html'

    def get(self, request, cocktail):

        obj = Cocktail.objects.get(id=cocktail)

        if obj.user == request.user and obj.is_active == 0:
            return redirect('home')

        cocktail = Cocktail.objects.annotate(
            avg_taste=Round(Avg('cocktailreview__taste_star')),
            avg_cost=Round(Avg('cocktailreview__cost_star')),
            avg_prep=Round(Avg('cocktailreview__prep_hardness_star'))
        ).get(id=cocktail)

        form = self.form_class()

        return render(request, self.template_name, {'cocktail': cocktail, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = User.objects.get(username=request.user)
            rate.cocktail = Cocktail.objects.get(id=self.kwargs['cocktail'])
            rate.save()
            return redirect('review', cocktail=self.kwargs['cocktail'])

        return render(request, self.template_name, {'cocktail': self.kwargs['cocktail'], 'form': form})


def edit_cocktail(request, cocktail):
    obj = Cocktail.objects.get(id=cocktail)

    if request.user == obj.user and obj.is_active == 1:
        form = CocktailForm(request.POST or None, files=request.FILES or None,
                            instance=Cocktail.objects.get(id=cocktail))

        if request.POST and form.is_valid():
            form.save()

            return redirect('home')

        return render(request, 'edit_cocktail.html', {'form': form})

    return redirect('home')


def delete_cocktail(request, cocktail):
    if request.user == Cocktail.objects.get(id=cocktail).user:
        cocktail = Cocktail.objects.get(id=cocktail)
        cocktail.is_active = 0
        cocktail.save()

    return redirect('home')


def review(request, cocktail):
    if request.user == Cocktail.objects.get(id=cocktail).is_active == 0:
        return redirect('home')

    reviews = CocktailReview.objects.filter(cocktail_id=cocktail).order_by('-user__is_expert')

    return render(request, 'review.html', {'reviews': reviews, 'cocktail': cocktail})


@login_required(login_url='login')
def add_cocktail(request):
    if request.method == "POST":
        form = CocktailForm(request.POST, request.FILES)

        if form.is_valid():
            cocktail = form.save(commit=False)
            cocktail.user = User.objects.get(username=request.user)
            cocktail.is_active = True
            cocktail.save()
            return redirect('home')

    else:
        form = CocktailForm(request.POST, request.FILES)

    return render(request, 'add_cocktail.html', {'form': form})
