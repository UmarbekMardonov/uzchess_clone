import django.contrib.admin.views.main


class DynPaginationChangeList(django.contrib.admin.views.main.ChangeList):
    def __init__(
        self,
        request,
        model,
        list_display,
        list_display_links,
        list_filter,
        date_hierarchy,
        search_fields,
        list_select_related,
        list_per_page,
        list_max_show_all,
        list_editable,
        model_admin,
        sortable_by,
        search_help_text,
    ):
        page_param = request.GET.get("list_per_page", None)
        if page_param is not None:
            # Override list_per_page if present in URL
            # Need to be before super call to be applied on filters
            list_per_page = int(page_param)
        super(DynPaginationChangeList, self).__init__(
            request,
            model,
            list_display,
            list_display_links,
            list_filter,
            date_hierarchy,
            search_fields,
            list_select_related,
            list_per_page,
            list_max_show_all,
            list_editable,
            model_admin,
            sortable_by,
            search_help_text,
        )

    def get_filters_params(self, params=None):
        """
        Return all params except IGNORED_PARAMS and 'list_per_page'
        """
        lookup_params = super(DynPaginationChangeList, self).get_filters_params(params)
        if "list_per_page" in lookup_params:
            del lookup_params["list_per_page"]
        return lookup_params


class AdminDynPaginationMixin:
    def get_changelist(self, request, *args, **kwargs):
        return DynPaginationChangeList
