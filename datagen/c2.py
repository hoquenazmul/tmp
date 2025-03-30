# constants.py

#constants.py
# Define field specifications (Fixed length and default values)
FIELD_DEFINITIONS = {
    "field1": (8, "12345678"),
    "field2": (10, "DEFAULT2"),
    "field3": (15, ""),
    "field4": (12, "ABCDEF123456"),
    "field5": (10, "FIELD5VAL"),
    "field6": (8, "DEFAULT6"),
    "field7": (6, "123456"),
    "field8": (14, ""),
    "field9": (9, "999999999"),
    "field10": (5, "XXXXX"),
    "field11": (10, "DEFAULT11"),
    "field12": (7, "7777777"),
    "field13": (20, ""),
    "field14": (4, "0000"),
    "field15": (3, "XYZ"),
}

# Scenario-based overrides
SCENARIO_OVERRIDES = {
    "scenario_a": {"field2": "SPECIALA", "field6": "SCENA6", "field11": "SCENA11"},
    "scenario_b": {"field2": "SPECIALB", "field6": "SCENB6", "field11": "SCENB11"},
}

# Constraints
MIN_RECORDS = 1
MAX_RECORDS = 1000


# forms.py
from django import forms
from .constants import MIN_RECORDS, MAX_RECORDS

class TestDataForm(forms.Form):
    SCENARIO_CHOICES = [
        ("scenario_a", "Scenario A"),
        ("scenario_b", "Scenario B"),
        ("default", "Default Scenario"),
    ]
    
    scenario = forms.ChoiceField(choices=SCENARIO_CHOICES, label="Select Scenario")
    num_records = forms.IntegerField(
        min_value=MIN_RECORDS,
        max_value=MAX_RECORDS,
        label="Number of Records",
        error_messages={
            "min_value": f"Minimum {MIN_RECORDS} records required.",
            "max_value": f"Maximum {MAX_RECORDS} records allowed.",
        }
    )


# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .forms import TestDataForm
from .constants import FIELD_DEFINITIONS, SCENARIO_OVERRIDES

def generate_test_data(scenario_key, num_records):
    """Generate test data records based on the selected scenario."""
    lines = []
    
    for _ in range(num_records):
        field_values = [
            # Apply scenario override if available, else use default
            SCENARIO_OVERRIDES.get(scenario_key, {}).get(field, default).ljust(length)[:length]
            for field, (length, default) in FIELD_DEFINITIONS.items()
        ]
        
        # Combine all fields into a single fixed-width row
        lines.append("".join(field_values))

    return "\n".join(lines)

def test_data_view(request):
    """Handle test data generation and file response."""
    if request.method == "POST":
        form = TestDataForm(request.POST)
        
        if form.is_valid():
            scenario = form.cleaned_data["scenario"]
            num_records = form.cleaned_data["num_records"]
            file_content = generate_test_data(scenario, num_records)

            # Prepare response for file download
            response = HttpResponse(file_content, content_type="text/plain; charset=utf-8")
            response["Content-Disposition"] = 'attachment; filename="test_data.txt"'
            response["Cache-Control"] = "no-store"
            return response
    else:
        form = TestDataForm()

    return render(request, "test_data_form.html", {"form": form})


{% load crispy_forms_tags %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Data Generator</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h2 class="text-center">Test Data Generator</h2>
        <p class="text-muted text-center">Select a scenario and enter the number of records to generate test data.</p>

        <div class="card shadow-sm p-4 mt-3">
            <form method="post" class="needs-validation" novalidate>
                {% csrf_token %}
                {{ form|crispy }}
                <button type="submit" class="btn btn-primary w-100 mt-3">Download Test Data</button>
            </form>
        </div>
    </div>

    <script>
        // Simple Bootstrap 5 Form Validation
        (function () {
            'use strict'
            var forms = document.querySelectorAll('.needs-validation')
            Array.prototype.slice.call(forms).forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()
                    }
                    form.classList.add('was-validated')
                }, false)
            })
        })();
    </script>
</body>
</html>
