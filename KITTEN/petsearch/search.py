# petsearch/search.py

from KITTEN.models import Pet

def search_pets_by_name(query):
    """
    Search for pets by name.

    Args:
        query (str): Query string to search for in pet names.

    Returns:
        QuerySet: QuerySet of pets matching the search query in their names.
    """
    return Pet.objects.filter(name__icontains=query)

def search_pets_by_breed(query):
    """
    Search for pets by breed.

    Args:
        query (str): Query string to search for in pet breeds.

    Returns:
        QuerySet: QuerySet of pets matching the search query in their breeds.
    """
    return Pet.objects.filter(breed__icontains=query)

def search_pets_by_type(query):
    """
    Search pets by pet type.

    Args:
        query (str): Search query for pet type.

    Returns:
        QuerySet: QuerySet of pets matching the search query for pet type.
    """
    return Pet.objects.filter(pet_type__icontains=query)
# Add more search functions as needed based on other attributes of the Pet model
