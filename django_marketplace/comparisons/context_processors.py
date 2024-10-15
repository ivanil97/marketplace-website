from comparisons.services.comparison_service import get_comparison_count


def comparison_count(request):
    return {
        'comparison_count': get_comparison_count(request)
    }
