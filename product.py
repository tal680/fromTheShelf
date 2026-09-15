def create():
    product_dict = {}

def donators_dict_create():
    donators_dict = {}

def add(donation_dict, product_dict):
    for key, value in donation_dict.items():
        product_dict[key] = value
    return product_dict

def get(ask_dict, product_dict):
    for i in product_dict.keys():
        if i in ask_dict[0]:
            product_dict[i] -= ask_dict[1]

def add_donator(donators_dict, don):
    donators_dict[don] = ''

def add_to_donators(donators_dict, don, product_dict):
    donators_dict[don] = add(donators_dict, product_dict)