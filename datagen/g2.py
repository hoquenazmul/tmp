# form.py
from django import forms

class EnvSelectionForm(forms.Form):
    environment = forms.ChoiceField(choices=[('default', 'Default'), ('qa', 'QA'), ('uat', 'UAT')], label='Select Environment')
    num_records = forms.IntegerField(min_value=1, label='Number of Records')

class ScenarioSelectionForm(forms.Form):
    SCENARIOS = [
        ('scenario1', 'Scenario 1'),
        ('scenario2', 'Scenario 2'),
        ('scenario3', 'Scenario 3'),
    ]
    scenario = forms.ChoiceField(choices=SCENARIOS, label='Select Scenario')
    num_records = forms.IntegerField(min_value=1, label='Number of Records')

# scenarios.py
FIELDS = {
    'field1': (10, ''),  # Required field, no default value
    'field2': (8, ''),   # Required field, no default value
    'field3': (12, ''),  # Required field, no default value
    'field4': (15, 'default4'),  # Optional field with default value
    'field5': (20, 'default5'),  # Optional field with default value
    'field6': (10, 'default6'),  # Optional field with default value
    'field7': (8, 'default7'),   # Optional field with default value
    'field8': (12, 'default8'),  # Optional field with default value
    'field9': (15, 'default9'),  # Optional field with default value
    'field10': (20, 'default10'),# Optional field with default value
}

SCENARIO_FIELDS = {
    'scenario1': {
        'field1': 'value1',
        'field2': 'value2',
        'field3': 'value3',
    },
    'scenario2': {
        'field1': 'value4',
        'field2': 'value5',
        'field3': 'value6',
    },
    'scenario3': {
        'field1': 'value7',
        'field2': 'value8',
        'field3': 'value9',
    },
}

# utils.py
def generate_input_file(scenario, num_records):
    from .scenarios import FIELDS, SCENARIO_FIELDS

    scenario_fields = SCENARIO_FIELDS.get(scenario, {})
    lines = []

    for _ in range(num_records):
        record = []
        for field, (length, default) in FIELDS.items():
            value = scenario_fields.get(field, default)
            record.append(value.ljust(length)[:length])
        lines.append(''.join(record))

    return '\n'.join(lines)

# views.py
from django.http import HttpResponse
from django.shortcuts import render
from .forms import EnvSelectionForm, ScenarioSelectionForm
from .utils import generate_input_file

def home(request):
    env_form = EnvSelectionForm(request.POST or None)
    scenario_form = ScenarioSelectionForm(request.POST or None)
    test_data = None

    if request.method == 'POST':
        if env_form.is_valid():
            env = env_form.cleaned_data['environment']
            num_records = env_form.cleaned_data['num_records']
            try:
                customers = Customers.objects.using(env).values()
                print(customers)
            except Exception as e:
                test_data = []
                print(f"Failed to fetch data from {env}: {e}")

        if scenario_form.is_valid():
            scenario = scenario_form.cleaned_data['scenario']
            num_records = scenario_form.cleaned_data['num_records']
            input_file_content = generate_input_file(scenario, num_records)

            response = HttpResponse(input_file_content, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="{scenario}_input.txt"'
            return response

    return render(request, 'index.html', {
        'env_form': env_form,
        'scenario_form': scenario_form,
        'data': test_data
    })

# template
<!DOCTYPE html>
<html>
<head>
    <title>Test Data Generator</title>
</head>
<body>
    <h1>Test Data Generator</h1>
    <form method="post">
        {% csrf_token %}
        <h2>Environment Selection</h2>
        {{ env_form.as_p }}
        <h2>Scenario Selection</h2>
        {{ scenario_form.as_p }}
        <button type="submit">Generate Input File</button>
    </form>
</body>
</html>
