# Формы Tutorial

## CarForm

```python
class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'color', 'state_number', 'vin']
```

## OwnerForm

```python
class OwnerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
```

## DriverLicenseForm

```python
class DriverLicenseForm(forms.ModelForm):
    class Meta:
        model = DriverLicense
        fields = ['license_number', 'license_type', 'issue_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
        }
```