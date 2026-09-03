from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactoForm
from .models import Contacto


def contacto_list(request):
    """
    Vista para listar los contactos y realizar búsquedas (Caso 3: Buscar contactos por nombre o correo).
    - Captura el parámetro de consulta 'q' enviado por GET.
    - Utiliza operadores de decisión (if) y el operador lógico OR (|) mediante objetos Q de Django.
    """
    query = request.GET.get('q', '').strip()
    contactos = Contacto.objects.all()

    # Estructura de decisión: si el usuario ingresó un término de búsqueda, filtramos
    if query:
        # Operador lógico OR (|) para buscar coincidencias parciales (icontains) en nombre o correo
        contactos = contactos.filter(
            Q(nombre__icontains=query) | Q(correo__icontains=query)
        )

    return render(request, 'contactos/contacto_list.html', {
        'contactos': contactos,
        'query': query,
    })


def contacto_detail(request, pk):
    """
    Vista para consultar el detalle de un contacto específico por su Primary Key (ID).
    Si no existe, devuelve una respuesta 404 de manera segura.
    """
    contacto = get_object_or_404(Contacto, pk=pk)
    return render(request, 'contactos/contacto_detail.html', {'contacto': contacto})


def contacto_create(request):
    """
    Vista para agregar un nuevo contacto personal (Caso 3: Agregar contactos).
    - Maneja peticiones GET para renderizar el formulario vacío.
    - Maneja peticiones POST para validar y persistir los datos en la base de datos.
    """
    form = ContactoForm(request.POST or None)

    # Estructura de decisión: validar si la petición es POST y si los datos son válidos
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('contacto_list')

    return render(request, 'contactos/contacto_form.html', {'form': form, 'modo': 'Agregar'})


def contacto_update(request, pk):
    """
    Vista para editar los datos de un contacto existente.
    - Carga la instancia actual del contacto.
    - Si se envía vía POST y pasa la validación, actualiza los datos y redirige al detalle.
    """
    contacto = get_object_or_404(Contacto, pk=pk)
    form = ContactoForm(request.POST or None, instance=contacto)

    # Estructura de decisión para procesar la actualización
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('contacto_detail', pk=contacto.pk)

    return render(request, 'contactos/contacto_form.html', {
        'form': form,
        'modo': 'Editar',
        'contacto': contacto,
    })


def contacto_delete(request, pk):
    """
    Vista para eliminar un contacto con confirmación previa.
    - GET: Muestra la pantalla de confirmación.
    - POST: Confirma la eliminación y redirige al listado general.
    """
    contacto = get_object_or_404(Contacto, pk=pk)

    # Estructura de decisión: solo ejecuta el borrado si la petición es POST
    if request.method == 'POST':
        contacto.delete()
        return redirect('contacto_list')

    return render(request, 'contactos/contacto_confirm_delete.html', {'contacto': contacto})