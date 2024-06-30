from .models import Watchlist

def get_common_context(request):
    """Function to get common context data for all views"""
    if request.user.is_authenticated:
        watchlist_count = Watchlist.objects.filter(user=request.user).count()
    else:
        watchlist_count = 0
    return {
        'watchlist_count': watchlist_count
    }
