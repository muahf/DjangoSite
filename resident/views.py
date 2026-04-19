from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import (
    PathogenForm,
    RegistrationForm,
    ResearcherForm,
    UmbrellaAuthenticationForm,
)
from .models import Pathogen, Researcher


def staff_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('resident:login')}?next={request.path}")
        if not request.user.is_staff:
            messages.warning(
                request,
                'Уровень допуска недостаточен. Доступно только главное меню.',
            )
            return redirect('resident:home')
        return view_func(request, *args, **kwargs)

    return _wrapped


@ensure_csrf_cookie
@cache_control(no_store=True)
def register(request):
    if request.user.is_authenticated:
        return redirect('resident:home')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация завершена. Войдите в систему.')
            return redirect('resident:login')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


@ensure_csrf_cookie
@cache_control(no_store=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('resident:home')
    if request.method == 'POST':
        form = UmbrellaAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('resident:home')
    else:
        form = UmbrellaAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('resident:home')


# 🏠 HOME: гости — только смешивание (guests.html); авторизованные — полный портал
def home(request):
    context = {
        'total_pathogens': Pathogen.objects.count(),
        'available_pathogens': Pathogen.objects.filter(is_available=True).count(),
        'total_researchers': Researcher.objects.count(),
        'recent_pathogens': Pathogen.objects.order_by('-id')[:6],
    }
    if request.user.is_authenticated:
        return render(request, 'resident/home.html', context)
    return render(request, 'guests.html', context)


# 🧬 PATHOGENS

@staff_required
def pathogen_list(request):
    pathogens = Pathogen.objects.all()
    return render(request, 'resident/pathogen.html', {
        'mode': 'list',
        'pathogens': pathogens
    })


@staff_required
def pathogen_detail(request, pk):
    pathogen = get_object_or_404(Pathogen, pk=pk)
    return render(request, 'resident/pathogen.html', {
        'mode': 'detail',
        'pathogen': pathogen
    })


@staff_required
def pathogen_create(request):
    if request.method == 'POST':
        form = PathogenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('resident:pathogen')
    else:
        form = PathogenForm()

    return render(request, 'resident/pathogen.html', {
        'mode': 'form',
        'form': form
    })


@staff_required
def pathogen_update(request, pk):
    pathogen = get_object_or_404(Pathogen, pk=pk)

    if request.method == 'POST':
        form = PathogenForm(request.POST, request.FILES, instance=pathogen)
        if form.is_valid():
            form.save()
            return redirect('resident:pathogen_detail', pk=pk)
    else:
        form = PathogenForm(instance=pathogen)

    return render(request, 'resident/pathogen.html', {
        'mode': 'form',
        'form': form
    })


@staff_required
def pathogen_delete(request, pk):
    pathogen = get_object_or_404(Pathogen, pk=pk)

    if request.method == 'POST':
        pathogen.delete()
        return redirect('resident:pathogen')

    return render(request, 'resident/pathogen.html', {
        'mode': 'delete',
        'pathogen': pathogen
    })


# 👨‍🔬 RESEARCHERS

@staff_required
def researcher_list(request):
    researchers = Researcher.objects.all()
    return render(request, 'resident/researcher.html', {
        'mode': 'list',
        'researchers': researchers
    })


@staff_required
def researcher_detail(request, pk):
    researcher = get_object_or_404(Researcher, pk=pk)
    return render(request, 'resident/researcher.html', {
        'mode': 'detail',
        'researcher': researcher
    })


@staff_required
def researcher_create(request):
    if request.method == 'POST':
        form = ResearcherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resident:researcher')
    else:
        form = ResearcherForm()

    return render(request, 'resident/researcher.html', {
        'mode': 'form',
        'form': form
    })


@staff_required
def researcher_update(request, pk):
    researcher = get_object_or_404(Researcher, pk=pk)

    if request.method == 'POST':
        form = ResearcherForm(request.POST, instance=researcher)
        if form.is_valid():
            form.save()
            return redirect('resident:researcher_detail', pk=pk)
    else:
        form = ResearcherForm(instance=researcher)

    return render(request, 'resident/researcher.html', {
        'mode': 'form',
        'form': form
    })


@staff_required
def researcher_delete(request, pk):
    researcher = get_object_or_404(Researcher, pk=pk)

    if request.method == 'POST':
        researcher.delete()
        return redirect('resident:researcher')

    return render(request, 'resident/researcher.html', {
        'mode': 'delete',
        'researcher': researcher
    })