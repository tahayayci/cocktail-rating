from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.db.models.functions import Round, Coalesce, Cast
from django.db.models import Avg, Count, OuterRef, Sum, Subquery, F, FloatField, When, Case, IntegerField
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


def cocktail_query(extra_filters={}):
    # Subquery preparations
    normal_reviews = CocktailReview.objects.filter(
        cocktail=OuterRef("pk"),
        user__is_expert=False
    )
    expert_reviews = CocktailReview.objects.filter(
        cocktail=OuterRef("pk"),
        user__is_expert=True
    )

    query = Cocktail.objects.filter(
        is_active=1,
        **extra_filters
    ).annotate(
        total_taste=Coalesce(Subquery(normal_reviews.values('cocktail_id').annotate(tmp=Sum('taste_star')).values('tmp')), 0) + 2*Coalesce(Subquery(expert_reviews.values('cocktail_id').annotate(tmp=Sum('taste_star')).values('tmp')), 0),
        total_cost=Coalesce(Subquery(normal_reviews.values('cocktail_id').annotate(tmp=Sum('cost_star')).values('tmp')), 0) + 2*Coalesce(Subquery(expert_reviews.values('cocktail_id').annotate(tmp=Sum('cost_star')).values('tmp')), 0),
        total_prep=Coalesce(Subquery(normal_reviews.values('cocktail_id').annotate(tmp=Sum('prep_hardness_star')).values('tmp')), 0) + 2*Coalesce(Subquery(expert_reviews.values('cocktail_id').annotate(tmp=Sum('prep_hardness_star')).values('tmp')), 0),
        user_count=Coalesce(Subquery(normal_reviews.values('cocktail_id').annotate(tmp=Count('id')).values('tmp')), 0) + 2*Coalesce(Subquery(expert_reviews.values('cocktail_id').annotate(tmp=Count('id')).values('tmp')), 0)
    ).annotate(
        avg_taste=Case(
            When(user_count=0, then=0),
            default=Cast(Round(Cast(F('total_taste'), FloatField()) / Cast(F('user_count'), FloatField())), IntegerField())
        ),
        avg_cost=Case(
            When(user_count=0, then=0),
            default=Cast(Round(Cast(F('total_cost'), FloatField()) / Cast(F('user_count'), FloatField())), IntegerField())
        ),
        avg_prep=Case(
            When(user_count=0, then=0),
            default=Cast(Round(Cast(F('total_prep'), FloatField()) / Cast(F('user_count'), FloatField())), IntegerField())
        ),
    ).order_by('name')

    return query


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        cocktails = cocktail_query()
        paginator = Paginator(cocktails, 12)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {'page_obj': page_obj, 'search': False})


def search(request):
    search_word = request.GET.get('search')

    if search_word is not None and search_word != '' and len(search_word) >= 3:
        cocktails = cocktail_query(extra_filters={'name__icontains': search_word})
        return render(request, 'results.html', {'page_obj': cocktails, 'search': True})

    else:
        cocktails = cocktail_query()
        paginator = Paginator(cocktails, 12)
        page_number = request.GET.get('page')
        return render(request, 'results.html', {'page_obj': paginator.get_page(page_number), 'search': False})


class RateView(LoginRequiredMixin, View):
    form_class = RatingForm
    template_name = 'rate.html'

    def get(self, request, cocktail):
        cocktail = cocktail_query().get(id=cocktail)

        if cocktail.user == request.user or cocktail.is_active == 0:
            return redirect('home')

        # Check whether there is a review exist
        rating = CocktailReview.objects.filter(user=request.user, cocktail=cocktail).first()
        if rating is not None:
            form = self.form_class(initial={
                'notes': rating.notes,
                'cost_star': rating.cost_star,
                'taste_star': rating.taste_star,
                'prep_hardness_star': rating.prep_hardness_star,
            })
        else:
            form = self.form_class()

        return render(request, self.template_name, {'cocktail': cocktail, 'form': form})

    def post(self, request, *args, **kwargs):
        rating = CocktailReview.objects.filter(user=request.user, cocktail_id=self.kwargs['cocktail']).first()
        form = self.form_class(instance=rating, data=request.POST)

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
    cocktail = Cocktail.objects.get(id=cocktail)

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
