from faker import Faker
from random import choice, randint, uniform
from sqlalchemy.orm import Session
from app.models import Product, User, Interaction
from app.database import engine, Base

# Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

fake = Faker()
session = Session(bind=engine)

# 1. Tạo Users
users = []
for _ in range(20):  # 20 users
    user = User(
        name=fake.name(),
        email=fake.unique.email()
    )
    users.append(user)
session.add_all(users)
session.commit()

# 2. Tạo Products
categories = ["Sports", "Electronics", "Clothing", "Toys", "Books"]
origins = ["France", "Vietnam", "China", "USA", "Germany"]

products = []
for _ in range(30):  # 30 products
    product = Product(
        name=fake.word().capitalize(),
        description=fake.sentence(),
        price=round(uniform(5, 500), 2),
        category=choice(categories),
        origin=choice(origins)
    )
    products.append(product)
session.add_all(products)
session.commit()

# 3. Tạo Interactions
interaction_types = ["click", "view", "purchase"]
interactions = []

for _ in range(100):  # 100 interactions
    interaction = Interaction(
        user_id=choice(users).id,
        product_id=choice(products).id,
        type=choice(interaction_types),
        timestamp=fake.date_time_this_year()
    )
    interactions.append(interaction)

session.add_all(interactions)
session.commit()

print("Dữ liệu giả đã được thêm vào database!")
