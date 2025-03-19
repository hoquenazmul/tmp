from django import forms

ENV_CHOICES = [
    ('qa', 'QA'),
    ('uat', 'UAT'),
    ('qa2', 'QA2'),
]

CRITERIA_CHOICES = [
    ('criteria1', 'Criteria 1'),
    ('criteria2', 'Criteria 2'),
    ('criteria3', 'Criteria 3'),
]

class TestDataForm(forms.Form):
    env = forms.ChoiceField(
        choices=ENV_CHOICES,
        widget=forms.RadioSelect,
        initial='qa',
        label="Select Environment"
    )
    criteria = forms.ChoiceField(
        choices=CRITERIA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Test Criteria"
    )
    record_count = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Number of Records",
        help_text="Enter the number of records to generate (minimum 1)."
    )
    customization_needed = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        label="Need Customization?"
    )
    display_all_fields = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
        label="Display All Fields?"
    )



============================================
{% load crispy_forms_tags %}

<div class="container mt-4">
    <h2 class="mb-4">Generate Test Data</h2>

    {% if messages %}
        {% for message in messages %}
            <div class="alert {{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        {% endfor %}
    {% endif %}

    <form method="post">
        {% csrf_token %}
        
        <!-- Render form with crispy -->
        {{ form|crispy }}

        <!-- Submit and Reset Buttons -->
        <div class="mt-3">
            <button type="submit" class="btn btn-primary">Generate Test Data</button>
            <button type="reset" class="btn btn-secondary">Clear</button>
        </div>
    </form>
</div>


------------------------------------------------------------

from django import forms

ENV_CHOICES = [
    ('qa', 'QA'),
    ('uat', 'UAT'),
    ('qa2', 'QA2'),
]

CRITERIA_CHOICES = [
    ('criteria1', 'Criteria 1'),
    ('criteria2', 'Criteria 2'),
    ('criteria3', 'Criteria 3'),
]

class TestDataForm(forms.Form):
    env = forms.ChoiceField(
        choices=ENV_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        initial='qa',
        label="Select Environment"
    )
    criteria = forms.ChoiceField(
        choices=CRITERIA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Test Criteria"
    )
    record_count = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Number of Records",
        help_text="Enter the number of records to generate (minimum 1)."
    )
    customization_needed = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        label="Need Customization?"
    )
    display_all_fields = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        label="Display All Fields?"
    )

    # Overriding the __init__ method to customize radio buttons using custom widget
    def __init__(self, *args, **kwargs):
        super(TestDataForm, self).__init__(*args, **kwargs)
        # Applying Bootstrap's button group style to radio buttons
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': 'btn-check'})
                field.widget.choices = [(value, label) for value, label in field.choices]
==============================================================
{% load crispy_forms_tags %}

<div class="container mt-4">
    <h2 class="mb-4">Generate Test Data</h2>

    {% if messages %}
        {% for message in messages %}
            <div class="alert {{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        {% endfor %}
    {% endif %}

    <form method="post">
        {% csrf_token %}
        
        <!-- Render Environment (with radio button group) -->
        <div class="mb-3">
            <label for="env" class="form-label">Select Environment</label>
            <div class="btn-group" role="group" aria-label="Environment radio button group">
                {% for value, label in form.env.field.choices %}
                    <input type="radio" class="btn-check" id="env_{{ value }}" name="env" value="{{ value }}" {% if form.env.value == value %} checked {% endif %} autocomplete="off">
                    <label class="btn btn-outline-primary" for="env_{{ value }}">{{ label }}</label>
                {% endfor %}
            </div>
        </div>

        <!-- Render Criteria (Bootstrap select style) -->
        <div class="mb-3">
            <label for="criteria" class="form-label">Test Criteria</label>
            {{ form.criteria|crispy }}
        </div>

        <!-- Render Record Count (Bootstrap form control style) -->
        <div class="mb-3">
            <label for="record_count" class="form-label">Number of Records</label>
            {{ form.record_count|crispy }}
        </div>

        <!-- Render Customization Needed (Radio button group) -->
        <div class="mb-3">
            <label for="customization_needed" class="form-label">Need Customization?</label>
            <div class="btn-group" role="group" aria-label="Customization radio button group">
                {% for value, label in form.customization_needed.field.choices %}
                    <input type="radio" class="btn-check" id="customization_needed_{{ value }}" name="customization_needed" value="{{ value }}" {% if form.customization_needed.value == value %} checked {% endif %} autocomplete="off">
                    <label class="btn btn-outline-primary" for="customization_needed_{{ value }}">{{ label }}</label>
                {% endfor %}
            </div>
        </div>

        <!-- Render Display All Fields (Radio button group) -->
        <div class="mb-3">
            <label for="display_all_fields" class="form-label">Display All Fields?</label>
            <div class="btn-group" role="group" aria-label="Display All Fields radio button group">
                {% for value, label in form.display_all_fields.field.choices %}
                    <input type="radio" class="btn-check" id="display_all_fields_{{ value }}" name="display_all_fields" value="{{ value }}" {% if form.display_all_fields.value == value %} checked {% endif %} autocomplete="off">
                    <label class="btn btn-outline-primary" for="display_all_fields_{{ value }}">{{ label }}</label>
                {% endfor %}
            </div>
        </div>

        <!-- Submit and Reset Buttons -->
        <div class="mt-3">
            <button type="submit" class="btn btn-primary">Generate Test Data</button>
            <button type="reset" class="btn btn-secondary">Clear</button>
        </div>
    </form>
</div>
==============================================================================
