from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactoForm
from .models import Contacto


def contacto_list(request):
    query = request.GET.get('q', '').strip()
    contactos = Contacto.objects.all()
    if query:
        contactos = contactos.filter(
            Q(nombre__icontains=query) | Q(correo__icontains=query)
        )
    return render(request, 'inventario/contacto_list.html', {
        'contactos': contactos,
        'query': query,
    })


def contacto_detail(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    return render(request, 'inventario/contacto_detail.html', {'contacto': contacto})


def contacto_create(request):
    form = ContactoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('contacto_list')
    return render(request, 'inventario/contacto_form.html', {'form': form, 'modo': 'Agregar'})


def contacto_update(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    form = ContactoForm(request.POST or None, instance=contacto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('contacto_detail', pk=contacto.pk)
    return render(request, 'inventario/contacto_form.html', {
        'form': form,
        'modo': 'Editar',
        'contacto': contacto,
    })


def contacto_delete(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        contacto.delete()
        return redirect('contacto_list')
    return render(request, 'inventario/contacto_confirm_delete.html', {'contacto': contacto})