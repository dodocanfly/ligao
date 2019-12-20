import json
from apps.dashboard.models import Country


def insert_countries():
    # json from https://restcountries.eu/rest/v2/all
    with open('countries.json') as json_file:
        data = json.load(json_file)
        exists_counter = created_counter = 0
        for c in data:
            obj, created = Country.objects.get_or_create(
                name=c['name'],
                native_name=c['nativeName'],
                code=c['alpha3Code']
            )
            if created:
                created_counter += 1
            else:
                exists_counter += 1
        return exists_counter, created_counter
