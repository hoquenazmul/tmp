from django.shortcuts import render

from datagen.models import Customers
from .forms import EnvSelectionForm


def home(request):
    form = EnvSelectionForm(request.POST or None)
    test_data = None

    if request.method == 'POST' and form.is_valid():
        env = form.cleaned_data['environment']

        # new_customer = Customers.objects.using(env).create(
        #     name='testing5',
        #     age=25,
        #     country='New Velly'
        # )
        try:
            customers = Customers.objects.using(env).values()
            print(customers)

        except Exception as e:
            test_data = []
            print(f"Failed to fetch data from {env}: {e}")

    return render(request, 'index.html', {
        'form': form,
        'data': test_data
    })