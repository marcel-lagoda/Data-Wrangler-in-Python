import pandas as pd

orderline_header = ('order_id', 'product_id', 'count')

orderline = [(1, 1, 3),
             (1, 2, 1),
             (1, 3, 2),
             (2, 2, 1),
             (2, 3, 1),
             (3, 3, 1),
             (3, 4, 1),
             (3, 5, 3),
             (4, 3, 2),
             (4, 4, 1),
             (4, 5, 2)]

products_dict = {1: ['Eveline Botanica', 'body'],
                 2: ['Ziaja jojoba', 'body'],
                 3: ['Soraya', 'face'],
                 4: ['Neutrogena hydro', 'face'],
                 5: ['Nivea hairmilk', 'hair']}



product_groups_priority = {'body': 1,
                           'face': 2,
                           'hair': 3}



orderline_lists = [list(lst) for lst in orderline]

def data_prepartion(orderline, products_dict, product_groups_priority):
    """
    Basic data preparation for more advanced processing.
    This func returns embedded lists of values [order_id, count, product_group_name, product_group_priority].
    """

    data = []  # main list

    for lst in orderline_lists:
        for ind, item in enumerate(lst):
            if ind == 1:  # selecting product_id
                lst[ind] = products_dict.get(item, item)  # assign dict values
                out = lst
                for i in out:
                    if type(i) == list:
                        out.append(i[1])
                        out.pop(1)  # remove product name
                        for j in out:
                            if type(j) == str:
                                var = j
                                j = product_groups_priority.get(var, var)
                                out.append(j)
                                data.append(out)  # [[order_id, count, prod_gr_name, prod_gr_priority], ]
    return data


def add_group_power():
    """
    Assign artificial strength of priority groups.
    1 --> 3, 2 --> 2, 3 --> 1 [priority --> strength]
    """

    data = data_prepartion(orderline_lists, products_dict, product_groups_priority)
    orders = []

    for lst in data:
        if 'body' in lst:
            lst.append(3)
        elif 'face' in lst:
            lst.append(2)
        elif 'hair' in lst:
            lst.append(1)
        orders.append(lst)
    return orders  # [[order_id, count, prod_gr_name, prod_gr_priority, gr_power], ]


def product_score():
    """
    Calculate score for each product separately [product priority group * count (product quantity).
    """
    data = add_group_power()
    calculated_score = []
    for lst in data:
        evaluation = lst[1] * lst[4]
        lst.append(evaluation)
        calculated_score.append(lst)
    return calculated_score  # [[order_id, count, prod_gr_name, prod_gr_priority, gr_power, prod_score], ]


def data_cleaner():
    """Remove redundant data."""
    to_remove = [1, 3, 4]
    data = product_score()
    cleaned = [[x for i, x in enumerate(a) if i not in to_remove] for a in data]
    return cleaned  # [[order_id, prod_gr_name, prod_score]


def results():
    """Return score by product name for each order."""
    base = data_cleaner()
    df = pd.DataFrame(base)
    df.columns = ['order id', 'group', 'score']
    # result = df.groupby(['id', 'group']).groups
    result = df.groupby(['order id', 'group']).sum()
    return result


if __name__ == '__main__':
    print(results())

