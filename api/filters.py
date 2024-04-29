from rest_framework.filters import BaseFilterBackend
from django.db.models import Q

class DraftOwnerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        criteria = Q()
        status = request.GET.get('status', 'published')
        criteria &= Q(status=status)

        if status == 'draft':
            criteria &= Q(owner=request.user)

        queryset = queryset.filter(criteria)
        return queryset