from django.db import models

# ////////// Models //////////////
from shared.models import BaseModel
from users.models import User

# ///////// validations ////////////
from django.core.validators import FileExtensionValidator


# //////////////////////////////////////////////////////
# //////////////// MARKA       /////////////////////////
# //////////////////////////////////////////////////////
class Marka(BaseModel):
    marka = models.CharField(max_length=64, unique=True)
    photo = models.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "heic", "heif"]
            )
        ],
        upload_to="cars/marka",
    )

    def __str__(self):
        return self.name

# //////////////////////////////////////////////////////
# //////////////    CAR MODEL  /////////////////////////
# //////////////////////////////////////////////////////
class CarModel(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE, related_name="models")

    def __str__(self):
        return f"{self.marka.__str__()} {self.name} modeli"

# //////////////////////////////////////////////////////
# ////////////////    CAR COLOR    /////////////////////
# //////////////////////////////////////////////////////
class Color(BaseModel):
    color = models.CharField(max_length=64, unique=True)
    color_code = models.CharField(max_length=7 , unique=True)

    def __str__(self):
        return self.color

# //////////////////////////////////////////////////////
# //////////////// COUNTRY      ////////////////////////
# //////////////////////////////////////////////////////
class Country(BaseModel):
    country = models.CharField(max_length=64, unique=True)
    flag = models.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "jpg", "png", "heic", "heif"]
            )
        ],
        upload_to="cars/country",
    )

    def __str__(self):
        return self.country

# //////////////////////////////////////////////////////
# //////////////// FUEL        /////////////////////////
# //////////////////////////////////////////////////////
class Fuel(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# //////////////////////////////////////////////////////
# //////////////// CAR         /////////////////////////
# //////////////////////////////////////////////////////
class Car(BaseModel):

    class DRIVE_TYPES(models.TextChoices):
        FRONT = "FWD", "Front-Wheel Drive"
        BACK = "RWD", "Rear-Wheel Drive"
        All = "AWD", "All-Wheel Drive"

    class TRANSMISSION_CHOICES(models.TextChoices):
        MANUAL = "MT", "Manual Transmission"
        AUTOMATIC = "AT", "Automatic Transmission"

    class DOORS_COUNT(models.IntegerChoices):
        TWO = 2, "2 doors"
        THREE = 3, "3 doors"
        FOUR = 4, "4 doors"
        FIVE = 5, "5 doors"

    class BODY_CHOICES(models.TextChoices):
        SEDAN = "sedan", "Sedan"
        HATCHBACK = "hatchback", "Hatchback"
        SUV = "suv", "SUV"
        CROSSOVER = "crossover", "Crossover"
        COUPE = "coupe", "Coupe"
        CONVERTIBLE = "convertible", "Convertible"
        WAGON = "wagon", "Wagon"
        PICKUP = "pickup", "Pickup"
        MINIVAN = "minivan", "Minivan"

    class CONDITION_CHOICES(models.TextChoices):
        NEW = "new", "Yangi"  # Новая
        EXCELLENT = "excellent", "A'lo"  # Отличное
        GOOD = "good", "Yaxshi"  # Хорошее
        FAIR = "fair", "O'rtacha"  # Среднее
        POOR = "poor", "Yomon"  # Плохое
        DAMAGED = "damaged", "Shikastlangan"  # Повреждённая

    class AVAILABILITY_CHOICES(models.TextChoices):
        IN_STOCK = "in_stock", "Mavjud"  # В наличии
        ON_ORDER = "on_order", "Buyurtma bo'yicha"  # Под заказ
        SOLD = "sold", "Sotilgan"  # Продано (optsional)
        RESERVED = "reserved", "Band qilingan"  # Забронировано (optsional)
        
    class STATUS_CHOICES(models.TextChoices):
        DRAFT = "DF" , "Draft", 
        PUBLISHED = "PD" , "Published"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars")
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE, related_name="cars")
    car_model = models.ForeignKey(
        CarModel, on_delete=models.CASCADE, related_name="cars"
    )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cars")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="cars")
    # benzinmi gazmi balo battarmi shu 
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE, related_name="cars")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    year = models.PositiveSmallIntegerField()
    milage = models.PositiveIntegerField()
    # motor
    displacement = models.DecimalField(max_digits=2, decimal_places=1)
    # ot kuchi
    power = models.PositiveSmallIntegerField()
    drive_type = models.CharField(max_length=3, choices=DRIVE_TYPES)
    # karobka
    transmission_type = models.CharField(
        max_length=2, choices=TRANSMISSION_CHOICES, default=TRANSMISSION_CHOICES.MANUAL
    )
    doors_count = models.PositiveSmallIntegerField(choices=DOORS_COUNT.choices)
    description = models.TextField(max_length=1200)
    body = models.CharField(choices=BODY_CHOICES.choices)
    condition = models.CharField(
        max_length=10, choices=CONDITION_CHOICES.choices, default=CONDITION_CHOICES.GOOD
    )
    # bazada bor yoki yoqligi
    availability = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES.choices)
    status = models.CharField(max_length=2 , choices=STATUS_CHOICES.choices , default=STATUS_CHOICES.DRAFT)

    def is_available(self):
        return self.availability == self.AVAILABILITY_CHOICES.IN_STOCK

    def __str__(self):
        return f"model: {self.car_model.__str__()} marka: {self.marka.__str__()} price:{self.price}"

# //////////////////////////////////////////////////////
# //////////////// CAR IMAGE     ///////////////////////
# //////////////////////////////////////////////////////
class CarImage(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpeg", "jpg", "png", "heic", "heif"]
            )
        ], 
        upload_to="cars/cars"
    )
    is_main = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ["-is_main" , "order"]
        
    def __str__(self):
        return f"{self.car} - image {self.id}"
# Create your models here.
