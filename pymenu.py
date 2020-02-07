'''
A menu helper class that will help to create menus

'''


class menu(object):
    '''
    Attributes:
        Name: name of the menu
        items: dict of items in the menu
        parent: the menu to go back to on empty input
    '''

    def __init__(self, name, items={}, parent=None):
        self.name = name
        self.items = items
        self.parent = parent

    def populate(self, item):
        '''
        a quick way to populate an entire menu
            item: accepts a list of items in the menu
        '''
        for i in item:
            self.newItems(i)

    def newItems(self, item, func=None):
        if isinstance(item, menu) and not func:
            func = item.name.lower()
        func = item if not func else func
        self.items.update({item: func})

    def newSubMenu(self, name, parent):
        newMenu = menu(name.title())
        newMenu.items = {}
        newMenu.parent = parent
        return newMenu

    def display(self):
        print('{} Menu'.format(self.name))
        print(str('-')*20)
        for n, i in enumerate(self.items.keys()):
            if isinstance(i, menu):
                print('{}. {}'.format(n+1, i.name.title()))
            else:
                print('{}. {}'.format(n+1, i.title()))
