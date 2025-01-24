from django import forms

class BaseStyledForm(forms.ModelForm):
    """
    A base form to define common widget styles for consistent theming.
    """
    
    base_widget_attrs = {
        'class': 'h100 bor-0 w-100 rounded-xxl p-2 ps-5 font-xssss text-grey-500 fw-500 border-light-md theme-dark-bg',
        'placeholder': ''
    }
    
    def apply_widget_attrs(self, field_name, placeholder):
        """
        Apply the base widget attributes and set a specific placeholder.
        """
        
        if field_name in self.fields:
            self.fields[field_name].widget.attrs.update({**self.base_widget_attrs, 'placeholder': placeholder})