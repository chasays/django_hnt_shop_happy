from django.forms.widgets import Textarea

class WangEditorWidget(Textarea):
    template_name = 'happy_shop/widgets/wangeditor.html'

    class Media:
        css = {
            'all': ('happy_shop/css/wangeditor.css',)
        }
        js = (
            'admin/js/vendor/jquery/jquery.min.js',
            'happy_shop/js/wangeditor/editor.js'
        )