from django.shortcuts import render, get_object_or_404, redirect
from .models import Pathogen, Researcher
from .forms import PathogenForm, ResearcherForm


# 🏠 HOME
def home(request):
    context = {
        'total_pathogens': Pathogen.objects.count(),
        'available_pathogens': Pathogen.objects.filter(is_available=True).count(),
        'total_researchers': Researcher.objects.count(),
        'recent_pathogens': Pathogen.objects.order_by('-id')[:6],
    }
    return render(request, 'resident/home.html', context)


# 🧬 PATHOGENS

def pathogen_list(request):
    pathogens = Pathogen.objects.all()
    return render(request, 'resident/pathogen.html', {
        'mode': 'list',
        'pathogens': pathogens
    })


def pathogen_detail(request, pk):
    pathogen = get_object_or_404(Pathogen, pk=pk)
    return render(request, 'resident/pathogen.html', {
        'mode': 'detail',
        'pathogen': pathogen
    })


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

def researcher_list(request):
    researchers = Researcher.objects.all()
    return render(request, 'resident/researcher.html', {
        'mode': 'list',
        'researchers': researchers
    })


def researcher_detail(request, pk):
    researcher = get_object_or_404(Researcher, pk=pk)
    return render(request, 'resident/researcher.html', {
        'mode': 'detail',
        'researcher': researcher
    })


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


def researcher_delete(request, pk):
    researcher = get_object_or_404(Researcher, pk=pk)

    if request.method == 'POST':
        researcher.delete()
        return redirect('resident:researcher')

    return render(request, 'resident/researcher.html', {
        'mode': 'delete',
        'researcher': researcher
    })