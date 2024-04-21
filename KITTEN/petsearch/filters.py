# petsearch/filters.py

from KITTEN.models import Pet

def filter_pets_by_type(pet_type):
    """
    Filter pets by pet type.

    Args:
        pet_type (str): Type of pet to filter by.

    Returns:
        QuerySet: QuerySet of pets filtered by the specified type.
    """
    return Pet.objects.filter(pet_type=pet_type)

def filter_pets_by_age(age):
    """
    Filter pets by age.

    Args:
        age (float): Age of pets to filter by.

    Returns:
        QuerySet: QuerySet of pets filtered by the specified age.
    """
    return Pet.objects.filter(age=age)

# Add more filter functions as needed based on other attributes of the Pet model
