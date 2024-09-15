class Clothes:
    shoes = "👟Обувь"
    jackets = "🥼Пуховики, 🧥Куртки"
    hoodi = "👘Худи, Толстовки, Штаны, Джинсы"
    t_shirt = "👕Футболки, Шорты"
    accessories = "💍Аксессуары"


class ClothesPrice:
    clothes_prices = {
        Clothes.shoes: 1890,
        Clothes.accessories: 790,
        Clothes.jackets: 1990,
        Clothes.t_shirt: 1090,
        Clothes.hoodi: 1290,
    }
    clothes_delivery_price = {
        Clothes.shoes: 1390,
        Clothes.accessories: 490,
        Clothes.jackets: 1490,
        Clothes.t_shirt: 690,
        Clothes.hoodi: 790,
    }

    clothes_commission = {
        Clothes.shoes: 500,
        Clothes.accessories: 300,
        Clothes.jackets: 500,
        Clothes.t_shirt: 400,
        Clothes.hoodi: 400,
    }
