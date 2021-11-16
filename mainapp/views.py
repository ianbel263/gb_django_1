from django.shortcuts import render


# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop'
    }
    return render(request, 'index.html', context)


def products(request):
    context = {
        'title': 'GeekShop - Каталог',
        'products': [
            {
                'name': 'Худи черного цвета с монограммами adidas Originals',
                'price': '6 090,00',
                'desc': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.',
                'img_url': 'vendor/img/products/Adidas-hoodie.png'
            },
            {
                'name': 'Синяя куртка The North Face',
                'price': '23 725,00',
                'desc': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.',
                'img_url': 'vendor/img/products/Blue-jacket-The-North-Face.png'
            },
            {
                'name': 'Коричневый спортивный oversized-топ ASOS DESIGN',
                'price': '3 390,00',
                'desc': 'Материал с плюшевой текстурой. Удобный и мягкий.',
                'img_url': 'vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png'
            },
            {
                'name': 'Черный рюкзак Nike Heritage',
                'price': '2 340,00',
                'desc': 'Плотная ткань. Легкий материал.',
                'img_url': 'vendor/img/products/Black-Nike-Heritage-backpack.png'
            },
            {
                'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
                'price': '13 590,00',
                'desc': 'Гладкий кожаный верх. Натуральный материал.',
                'img_url': 'vendor/img/products/Black-Dr-Martens-shoes.png'
            },
            {
                'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
                'price': '2 890,00',
                'desc': 'Легкая эластичная ткань сирсакер Фактурная ткань.',
                'img_url': 'vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png'
            },
        ]
    }
    return render(request, 'products.html', context)
