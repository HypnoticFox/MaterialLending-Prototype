from django_components import component

@component.register("pagination_navigation")
class PaginationNavigation(component.Component):
    template_name = "pagination_navigation/template.html"

    def get_context_data(self, page_obj, amount_on_each_side = 1, amount_on_ends = 1):
        return {
            "page_obj": page_obj,
            "page_numbers": page_obj.paginator.get_elided_page_range(number = page_obj.number, on_each_side = amount_on_each_side, on_ends = amount_on_ends)
        }