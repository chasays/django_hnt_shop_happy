from django_filters import rest_framework as filters


class MyFilterBackend(filters.DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        # print(queryset)

        kwargs = super().get_filterset_kwargs(request, queryset, view)
        
        # merge filterset kwargs provided by view class
        if hasattr(view, 'get_filterset_kwargs'):
            kwargs.update(view.get_filterset_kwargs())
        return kwargs

    def get_filterset_class(self, view, queryset=None):
        if view.detail:
            print(queryset)
            print(view.detail)
            print(view.request.query_params)
        return super().get_filterset_class(view, queryset)  