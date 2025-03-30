from django import forms
from django.shortcuts import render
from django.http import HttpResponse

# Define field specifications
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

# Form to accept user input
class TestDataForm(forms.Form):
    SCENARIO_CHOICES = [
        ("scenario_a", "Scenario A"),
        ("scenario_b", "Scenario B"),
        ("default", "Default Scenario"),
    ]
    scenario = forms.ChoiceField(choices=SCENARIO_CHOICES, label="Select Scenario")
    num_records = forms.IntegerField(min_value=1, max_value=1000, label="Number of Records")

# Function to generate test data as a string
def generate_test_data(scenario_key, num_records):
    lines = []
    for _ in range(num_records):
        field_values = []
        for field, (length, default_value) in FIELD_DEFINITIONS.items():
            # Apply scenario override if available
            value = SCENARIO_OVERRIDES.get(scenario_key, {}).get(field, default_value)
            
            # Ensure the value matches the fixed length
            field_values.append(value.ljust(length)[:length])
        
        # Combine fields into a single fixed-width row
        lines.append("".join(field_values))
    
    return "\n".join(lines)

# View to handle form submission and return file
def test_data_view(request):
    if request.method == "POST":
        form = TestDataForm(request.POST)
        if form.is_valid():
            scenario = form.cleaned_data["scenario"]
            num_records = form.cleaned_data["num_records"]

            # Generate test data as a string
            file_content = generate_test_data(scenario, num_records)

            # Create a response with file content as an attachment
            response = HttpResponse(file_content, content_type="text/plain")
            response["Content-Disposition"] = f'attachment; filename="test_data.txt"'
            return response
    else:
        form = TestDataForm()

    return render(request, "test_data_form.html", {"form": form})


# html template
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
        <h2>Generate Test Data</h2>
        <form method="post" class="mt-3">
            {% csrf_token %}
            {{ form|crispy }}
            <button type="submit" class="btn btn-primary">Download Test Data</button>
        </form>
    </div>
</body>
</html>
