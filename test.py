from faker import Faker

# Erstelle ein Faker-Objekt für deutsche Namen
fake = Faker('de_DE')

# Generiere einen deutschen Namen
deutscher_name = fake.name()
print(deutscher_name)