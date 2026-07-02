from django import forms
from .models import Order, WILAYA_CHOICES


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'phone', 'wilaya', 'city', 'address', 'note')
        widgets = {
            'note': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'border-color:var(--apricot);'
        self.fields['wilaya'].widget.attrs['class'] = 'form-select'