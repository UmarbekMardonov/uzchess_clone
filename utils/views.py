from rest_framework import generics, status, views


class FilterByPermission:
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(shop__in=self.request.user.shops.all().values_list("id", flat=True))
        )
