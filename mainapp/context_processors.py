from basketapp.models import Basket


def basket(request):
    data = []
    if request.user.is_authenticated:
        data = Basket.objects.filter(user=request.user)

    return {
        'baskets': data
    }
