from enum import StrEnum

class Gender(StrEnum):
    """ User gender"""
    male = "Male"
    female = "Female"

    @classmethod
    def choices(cls):
        return [(gender.name, gender.value) for gender in cls]


class UserRole(StrEnum):
    """Role of the user in a system"""
    owner = "Owner"
    tenant = "Tenant"
    admin = "Admin"

    @classmethod
    def choices(cls):
        return [(role.name, role.value) for role in cls]


class HouseType(StrEnum):
    """Type of the housing place"""
    house = "House"
    room = "Room"
    apartment = "Apartment"
    studio = "Studio"

    @classmethod
    def choices(cls):
        return [(house_type.name, house_type.value) for house_type in cls]


class AmenityCategory(StrEnum):
    """
    Category of house comfortability:
    Basic: wi-fi,shared kitchen/bathroom, heating

    Comfort: Air conditioning, Full kitchen/bathroom,
    washing machine, TV, Elevator(If needed)

    Premium: Modern furniture/renovations(dishwasher,smart home),
    personal parking spot/garage,
    balcony/terrace, Pool/Sauna(For Houses)
    """
    basic = "Basic"
    comfort = "Comfort"
    premium = "Premium"

    @classmethod
    def choices(cls):
        return [(amen_categ.name, amen_categ.value) for amen_categ in cls]


class BookingStatus(StrEnum):
    """Current status of booking"""
    pending = "Pending"
    rejected = "Rejected"
    confirmed = "Confirmed"
    cancelled = "Cancelled"
    completed = "Completed"

    @classmethod
    def choices(cls):
        return [(book_stat.name, book_stat.value) for book_stat in cls]


class VerificationStatus(StrEnum):
    """Status of verification"""
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"

    @classmethod
    def choices(cls):
        return [(verif_stat.name, verif_stat.value) for verif_stat in cls]
