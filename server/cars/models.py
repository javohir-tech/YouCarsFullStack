from django.db import models

# ////////// Models //////////////
from shared.models import BaseModel
from users.models import User

# ///////// validations ////////////
from django.core.validators import FileExtensionValidator


# //////////////////////////////////////////////////////
# ////////// AVTOMABIL TYPE       //////////////////////
# //////////////////////////////////////////////////////
class AvtoMobileType(BaseModel):
    class AVTOMABIL_TYPE(models.TextChoices):
        CAR = "CR", "Car"
        COMMERCIAL_TRANSPORT = "CT", "Commercial transport"
        Motorcycles = "MO"

    name = models.CharField(
        max_length=2,
        unique=True,
        choices=AVTOMABIL_TYPE.choices,
        default=AVTOMABIL_TYPE.CAR,
    )

    def __str__(self):
        return self.name


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
        return self.marka

    def add_marka(self):
        temp_marka = self.marka.lower().strip()
        self.marka = temp_marka

    def save(self, *args, **kwargs):
        self.add_marka()
        super().save(*args, **kwargs)


# //////////////////////////////////////////////////////
# ////// Avto TYPE and MARKA         ///////////////////
# //////////////////////////////////////////////////////
class AvtoTypeMarka(BaseModel):
    avto_type = models.ForeignKey(
        AvtoMobileType, on_delete=models.CASCADE, related_name="markas"
    )
    marka = models.ForeignKey(
        Marka, on_delete=models.CASCADE, related_name="avto_types"
    )

    def __str__(self):
        return f"{self.avto_type.__str__()} and {self.marka.__str__()}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["avto_type", "marka"], name="avto_type and marka unique"
            )
        ]


# //////////////////////////////////////////////////////
# //////////////    CAR MODEL  /////////////////////////
# //////////////////////////////////////////////////////
class CarModel(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE, related_name="models")

    def add_name(self):
        temp_name = self.name.lower().strip()
        self.name = temp_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.add_name()
        super().save(*args, **kwargs)


# //////////////////////////////////////////////////////
# ////////////////    CAR COLOR    /////////////////////
# //////////////////////////////////////////////////////
class Color(BaseModel):
    color = models.CharField(max_length=64, unique=True)
    color_code = models.CharField(max_length=7, unique=True)

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
        DRAFT = "DF", "Draft"
        PUBLISHED = "PD", "Published"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars")
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE, related_name="cars")
    avto_type = models.ForeignKey(
        AvtoMobileType, on_delete=models.CASCADE, related_name="avtos"
    )
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
    # holati
    condition = models.CharField(
        max_length=10, choices=CONDITION_CHOICES.choices, default=CONDITION_CHOICES.GOOD
    )
    # bazada bor yoki yoqligi
    availability = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES.choices)
    status = models.CharField(
        max_length=2, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.DRAFT
    )
    views = models.PositiveIntegerField(default=0)

    def is_available(self):
        return self.availability == self.AVAILABILITY_CHOICES.IN_STOCK

    def __str__(self):
        return f"marka : {self.marka.__str__()} model:{self.car_model.__str__()} status:{self.status}"


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
        upload_to="cars/cars",
    )
    is_main = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-is_main", "order"]

    def __str__(self):
        return f"{self.car} - image {self.id}"


# //////////////////////////////////////////////////////
# //////////////// LIKE MODEL    ///////////////////////
# //////////////////////////////////////////////////////
class Like(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.author.__str__()} and {self.car.__str__()}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "author",
                    "car",
                ],
                name="unique_like_per_user_and_car",
            )
        ]


class DeletionStatistics(models.Model):
    sold_on_youcar = models.IntegerField(default=0, verbose_name="YouCar da sotilgan")
    sold_elsewhere = models.IntegerField(default=0, verbose_name="Boshqa joyda sotilgan")
    other_reason = models.IntegerField(default=0, verbose_name="Boshqa sabab")
    
    @classmethod
    def increment_reason(cls, reason):
        stats, created = cls.objects.get_or_create(id=1)
        
        if reason == 1:
            stats.sold_on_youcar += 1
        elif reason == 2:
            stats.sold_elsewhere += 1
        elif reason == 3:
            stats.other_reason += 1
        
        stats.save()
        return stats