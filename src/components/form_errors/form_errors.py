from django_components import component

@component.register("form_errors")
class PaginationNavigation(component.Component):
    template_name = "form_errors/template.html"

    def get_context_data(self, error_list, extra_classes=""):
        return {
            "error_list": error_list,
            "extra_classes": extra_classes
        }