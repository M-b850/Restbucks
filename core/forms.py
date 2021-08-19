from django import forms
from core.models import *
from . import choices

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].required = False

    MILK = forms.ChoiceField(choices=choices.MILK_CHOICES, widget=forms.RadioSelect(), required=False)
    SIZE = forms.ChoiceField(choices=choices.SIZE_CHOICES, widget=forms.RadioSelect(), required=False)
    SHOTS = forms.ChoiceField(choices=choices.SHOTS_CHOICES, widget=forms.RadioSelect(), required=False)
    KIND = forms.ChoiceField(choices=choices.KIND_CHOICES, widget=forms.RadioSelect(), required=False)
    
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'milk': forms.RadioSelect(),
            'size': forms.RadioSelect(),
            'shots': forms.RadioSelect(),
            'kind': forms.RadioSelect(),
        }

    def clean(self):
        custom = [
            self.cleaned_data.get('MILK'),
            self.cleaned_data.get('SIZE'),
            self.cleaned_data.get('SHOTS'),
            self.cleaned_data.get('KIND'), 
        ]

        count = 0
        for c in custom:
            if c is not None and c != '':
                count += 1
                tag = c

        if count > 1:
            raise forms.ValidationError('You can only choose one custom option.')
        try:
            tag = Tag.objects.get(name=tag.upper())
            self.cleaned_data['tag'] = tag
        except UnboundLocalError:
            pass

        product = self.cleaned_data.get('product')
        customization = self.cleaned_data.get('customization')
        if customization and tag and product:
            if tag.customization != customization:
                raise forms.ValidationError(f'This Tag : {tag} doesn\'t belong to this customization : {customization}.')

            if customization.product != product:
                raise forms.ValidationError(f'This customization : {customization} doesn\'t belong to this product : {product}.')
        
        
        return self.cleaned_data
