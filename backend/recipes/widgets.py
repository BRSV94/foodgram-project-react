from django import forms
from django.utils.html import format_html

class ColorPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('path/to/colorpicker.css',),
        }
        js = ('path/to/colorpicker.js',)

    def render(self, name, value, attrs=None, renderer=None):
        rendered = super().render(name, value, attrs, renderer)
        color_picker_html = '''
            <div id="color-picker"></div>
            <script>
                // Add your color picker JS initialization code here
            </script>
        '''
        return format_html(rendered + color_picker_html)