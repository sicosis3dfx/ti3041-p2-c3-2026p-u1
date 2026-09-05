from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactoForm
from .models import Contacto


# Vista para listar contactos y buscar por nombre o correo
def contacto_list(request):
    # Capturamos lo que el usuario escribe en la barra de búsqueda (método GET)
    query = request.GET.get('q', '').strip()
    contactos = Contacto.objects.all()

    # Si hay texto en la búsqueda, filtramos los contactos
    if query:
        # Usamos Q con el operador | (OR) para buscar coincidencia en nombre o correo
        # icontains busca sin importar mayúsculas o minúsculas
        contactos = contactos.filter(
            Q(nombre__icontains=query) | Q(correo__icontains=query)
        )

    # Pasamos los contactos y el texto buscado al template
    return render(request, 'contactos/contacto_list.html', {
        'contactos': contactos,
        'query': query,
    })


# Vista para ver los detalles de un contacto por su id
def contacto_detail(request, pk):
    # Trae el contacto según su id; si no existe lanza error 404
    contacto = get_object_or_404(Contacto, pk=pk)
    return render(request, 'contactos/contacto_detail.html', {'contacto': contacto})


# Vista para crear un nuevo contacto
def contacto_create(request):
    # Si la petición es POST cargamos los datos enviados, sino iniciamos el formulario vacío
    form = ContactoForm(request.POST or None)

    # Validamos que sea método POST y que los datos ingresados sean válidos
    if request.method == 'POST' and form.is_valid():
        form.save()
        # Una vez guardado volvemos a la lista principal
        return redirect('contacto_list')

    return render(request, 'contactos/contacto_form.html', {'form': form, 'modo': 'Agregar'})


# Vista para editar los datos de un contacto existente
def contacto_update(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    # Le pasamos la instancia para que el formulario venga con los datos actuales
    form = ContactoForm(request.POST or None, instance=contacto)

    # Si se envían cambios válidos, se guardan en la base de datos
    if request.method == 'POST' and form.is_valid():
        form.save()
        # Redirigimos a la vista de detalle de ese mismo contacto
        return redirect('contacto_detail', pk=contacto.pk)

    return render(request, 'contactos/contacto_form.html', {
        'form': form,
        'modo': 'Editar',
        'contacto': contacto,
    })


# Vista para borrar un contacto con confirmación
def contacto_delete(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)

    # Solo eliminamos cuando el usuario confirma mediante POST
    if request.method == 'POST':
        contacto.delete()
        return redirect('contacto_list')

    # Si es GET mostramos la plantilla que pregunta si está seguro
    return render(request, 'contactos/contacto_confirm_delete.html', {'contacto': contacto})


# Vista para borrar múltiples contactos con confirmación previa
def contacto_bulk_delete(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')

        # Si no se seleccionó ningún contacto, volvemos a la lista principal
        if not selected_ids:
            return redirect('contacto_list')

        # Si el usuario ya confirmó la eliminación masiva
        if request.POST.get('confirmar') == '1':
            Contacto.objects.filter(pk__in=selected_ids).delete()
            return redirect('contacto_list')

        # Si aún no confirma, traemos los contactos para mostrarlos en la pantalla de confirmación
        contactos = Contacto.objects.filter(pk__in=selected_ids)
        if not contactos.exists():
            return redirect('contacto_list')

        return render(request, 'contactos/contacto_bulk_confirm_delete.html', {
            'contactos': contactos,
            'selected_ids': selected_ids,
        })

    # Si se intenta acceder por GET directo, redirigimos a la lista
    return redirect('contacto_list')