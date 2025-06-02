class Clothes:
    shoes = "👟Обувь"
    jackets = "🥼Пуховики, 🧥Куртки"
    accessories = "💍Аксессуары"
    hoodi = "👘Худи, 👖Штаны"
    t_shirt = "👕Футболки, 🩳Шорты"
    sports_equipment = "🏀Спортивный инвентарь"
    bags_and_backpacks = "👜Сумки, 🎒Рюкзаки"


class ClothesPrice:
    clothes_prices = {
        Clothes.shoes: 1890,
        Clothes.accessories: 790,
        Clothes.jackets: 1990,
        Clothes.t_shirt: 1090,
        Clothes.hoodi: 1290,
        Clothes.sports_equipment: 1490,
        Clothes.bags_and_backpacks: 1290,
    }
    clothes_delivery_price = {
        Clothes.shoes: 1390,
        Clothes.accessories: 490,
        Clothes.jackets: 1490,
        Clothes.t_shirt: 690,
        Clothes.hoodi: 790,
        Clothes.sports_equipment: 990,
        Clothes.bags_and_backpacks: 790,
    }

    clothes_commission = {
        Clothes.shoes: 500,
        Clothes.accessories: 300,
        Clothes.jackets: 500,
        Clothes.t_shirt: 400,
        Clothes.hoodi: 400,
        Clothes.sports_equipment: 500,
        Clothes.bags_and_backpacks: 500,
        
    }
