from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.category import Category
from app.infrastructure.database.models.product import Product
from app.infrastructure.database.models.client import Client
from app.infrastructure.database.models.order import Order, OrderItem


async def init_test_data(session: AsyncSession):

    check_categories = await session.execute(select(Category))
    if check_categories.scalars().unique().all():
        return
    
    household_appliances = Category(name="Бытовая техника")
    computers = Category(name="Компьютеры")
    
    session.add_all([household_appliances, computers])
    await session.flush()
    
    washing_machines = Category(name="Стиральные машины", parent_id=household_appliances.id)
    refrigerators = Category(name="Холодильники", parent_id=household_appliances.id)
    tvs = Category(name="Телевизоры", parent_id=household_appliances.id)
    
    session.add_all([washing_machines, refrigerators, tvs])
    await session.flush()
    
    single_door = Category(name="однокамерные", parent_id=refrigerators.id)
    double_door = Category(name="двухкамерные", parent_id=refrigerators.id)
    
    laptops = Category(name="Ноутбуки", parent_id=computers.id)
    monoblocks = Category(name="Моноблоки", parent_id=computers.id)
    
    session.add_all([single_door, double_door, laptops, monoblocks])
    await session.flush()
    
    laptop_17 = Category(name='17"', parent_id=laptops.id)
    laptop_19 = Category(name='19"', parent_id=laptops.id)
    
    session.add_all([laptop_17, laptop_19])
    await session.flush()
    
    products = [
        Product(name="Стиральная машина Samsung WW70", category_id=washing_machines.id, price=Decimal("45000.00")),
        Product(name="Стиральная машина LG F2J6HS0W", category_id=washing_machines.id, price=Decimal("38000.00")),
        
        Product(name="Холодильник Атлант ХМ 4012-080", category_id=single_door.id, price=Decimal("25000.00")),
        Product(name="Холодильник Бирюса 118", category_id=single_door.id, price=Decimal("18000.00")),
        
        Product(name="Холодильник Samsung RB37", category_id=double_door.id, price=Decimal("55000.00")),
        Product(name="Холодильник LG GA-B509CQSL", category_id=double_door.id, price=Decimal("48000.00")),
        
        Product(name="Телевизор Samsung UE43", category_id=tvs.id, price=Decimal("35000.00")),
        Product(name="Телевизор LG 43UP7500", category_id=tvs.id, price=Decimal("32000.00")),
        
        Product(name='Ноутбук ASUS VivoBook 17"', category_id=laptop_17.id, price=Decimal("65000.00")),
        Product(name='Ноутбук HP Pavilion 17"', category_id=laptop_17.id, price=Decimal("58000.00")),
        
        Product(name='Ноутбук Dell Inspiron 19"', category_id=laptop_19.id, price=Decimal("75000.00")),
        Product(name='Ноутбук Lenovo IdeaPad 19"', category_id=laptop_19.id, price=Decimal("68000.00")),
        
        Product(name="Моноблок Apple iMac 24", category_id=monoblocks.id, price=Decimal("120000.00")),
        Product(name="Моноблок HP All-in-One 24", category_id=monoblocks.id, price=Decimal("85000.00")),
    ]
    
    session.add_all(products)
    await session.flush()
    
    clients = [
        Client(name="ООО Рога и Копыта", address="г. Москва, ул. Тверская, д. 1"),
        Client(name="ИП Иванов И.И.", address="г. Санкт-Петербург, пр. Невский, д. 25"),
        Client(name="ООО Технологии Будущего", address="г. Екатеринбург, ул. Ленина, д. 50"),
        Client(name="ИП Петров П.П.", address="г. Новосибирск, ул. Красный проспект, д. 100"),
        Client(name="ООО Мега Корп", address="г. Казань, ул. Баумана, д. 15"),
    ]
    
    session.add_all(clients)
    await session.flush()
    
    order1 = Order(client_id=clients[0].id)
    session.add(order1)
    await session.flush()
    
    order1_items = [
        OrderItem(order_id=order1.id, product_id=products[0].id, quantity=1, price=products[0].price),  
        OrderItem(order_id=order1.id, product_id=products[2].id, quantity=1, price=products[2].price),  
        OrderItem(order_id=order1.id, product_id=products[4].id, quantity=1, price=products[4].price),  
    ]
    
    order2 = Order(client_id=clients[1].id)
    session.add(order2)
    await session.flush()
    
    order2_items = [
        OrderItem(order_id=order2.id, product_id=products[8].id, quantity=1, price=products[8].price),  
        OrderItem(order_id=order2.id, product_id=products[10].id, quantity=1, price=products[10].price), 
    ]
    
    order3 = Order(client_id=clients[2].id)
    session.add(order3)
    await session.flush()
    
    order3_items = [
        OrderItem(order_id=order3.id, product_id=products[6].id, quantity=2, price=products[6].price),  
        OrderItem(order_id=order3.id, product_id=products[12].id, quantity=1, price=products[12].price), 
    ]
    
    order4 = Order(client_id=clients[3].id)
    session.add(order4)
    await session.flush()
    
    order4_items = [
        OrderItem(order_id=order4.id, product_id=products[1].id, quantity=1, price=products[1].price),  # Стиральная машина LG
        OrderItem(order_id=order4.id, product_id=products[3].id, quantity=2, price=products[3].price),  # Холодильники Бирюса
        OrderItem(order_id=order4.id, product_id=products[7].id, quantity=1, price=products[7].price),  # Телевизор LG
    ]
    
    order5 = Order(client_id=clients[4].id)
    session.add(order5)
    await session.flush()
    
    order5_items = [
        OrderItem(order_id=order5.id, product_id=products[9].id, quantity=1, price=products[9].price),   # Ноутбук HP 17"
        OrderItem(order_id=order5.id, product_id=products[11].id, quantity=1, price=products[11].price), # Ноутбук Lenovo 19"
        OrderItem(order_id=order5.id, product_id=products[13].id, quantity=1, price=products[13].price), # Моноблок HP
    ]
    
    all_order_items = order1_items + order2_items + order3_items + order4_items + order5_items
    session.add_all(all_order_items)
    
    await session.commit()
    print("✅ Тестовые данные успешно созданы!")
    print(f"📊 Создано:")
    print(f"   - Категорий: {len([household_appliances, computers, washing_machines, refrigerators, tvs, single_door, double_door, laptops, monoblocks, laptop_17, laptop_19])}")
    print(f"   - Товаров: {len(products)}")
    print(f"   - Клиентов: {len(clients)}")
    print(f"   - Заказов: 5")
    print(f"   - Позиций в заказах: {len(all_order_items)}")
