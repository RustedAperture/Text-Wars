class store(object):
    def __init__(self, name, items={}, categories=[]):
        self.name = name
        self.items = items
        self.categories = categories

    def NewItem(self, name, cost, category, userVariable):
        if category in self.items.keys():
            self.items[category].update({name: [cost, userVariable]})
        else:
            self.categories.append(category)
            self.items.update({category: {name: [cost, userVariable]}})

    def display(self, category):
        item = self.items[category].keys()
        cost = self.items[category].values()
        print(category)
        print(str('-')*20)
        for i, c, n in zip(item, cost, range(len(item))):
            print('{}. {} - ${}'.format(n+1, i, c[0]))
