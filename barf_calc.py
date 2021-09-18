#!/usr/bin/env python3

import re


class Food:
    '''
    bone: percent of bone in Food
    meat: percent of mean in Food
    organ: percent of organ in Food
    fruit: percent of fruit in Food
    vege: percent of vegetables in Food
    '''

    presets = {'chwhl':     {'description': 'Chicken: Whole (no organs)',
                             'bone': 0.32, 'meat': 0.68},
               'chdrum':    {'description': 'Chicken: Drumsticks',
                             'bone': 0.27, 'meat': 0.73},
               'meat':      {'description': 'Pure meat', 'meat': 1.},
               'fruit':     {'description': 'Fruit', 'fruit': 1.},
               'vege':      {'description': 'Vegetables', 'vege': 1.},
               'orgchlvr':  {'description': 'Organs: Chicken Liver',
                             'organ': 1.},
               'orgbflvr':  {'description': 'Organs: Beef Liver',
                             'organ': 1.},
               'orgchgiz':  {'description': 'Organs: Chicken Hearts & Gizzards',
                             'organ': 1.},
               }

    _registry = {}
    _total_wt = {'weight': 0., 'bone': 0., 'meat': 0., 'vege': 0., 'fruit': 0.,
                 'organ': 0.}

    def __init__(self, weight: float, description: str,
                 organ: float = 0., bone: float = 0., meat: float = 0.,
                 fruit: float = 0., vege: float = 0.):
        self.weight = weight
        self.description = description
        self._composition = {'organ': organ * weight, 'fruit': fruit * weight,
                             'vege': vege * weight, 'bone': bone * weight,
                             'meat': meat * weight, }

    def __str__(self):
        '''How to display individual food items '''
        lst = [f'{k:6s}:{v:4.1f}' for k, v in self._composition.items()
               if v != 0.]
        return f'{self.description:34s}|{"|".join(lst)}'

    @staticmethod
    def list_presets(presets: dict):
        for i, v in enumerate(presets.values()):
            description = v['description']
            print(f'\t{i}) {description}')

    @staticmethod
    def display_total_wt(wt: dict):
        exclusions = ['weight', ]
        categories = [c for c in wt.keys() if c not in exclusions]
        print(f'Total Weight: {wt["weight"]:5.1f}\n')
        print('Mix')
        for category in categories:
            print(f'\t{category}:\t{wt[category]/wt["weight"]:>5.1%}')

    @classmethod
    def display_meal(cls):
        print('\nIngredients')
        for i, v in enumerate(cls._registry.values()):
            print(f'\t{i}) {v}')
        print()
        cls.display_total_wt(cls._total_wt)

    @classmethod
    def add(cls):
        '''Add instance of Food using presets'''
        cls.list_presets(cls.presets)

        # Get foodtype
        response = None
        while response not in range(len(cls.presets.keys())):
            try:
                response = int(input('Choose a foodtype to add: '))
            except ValueError:
                pass

        # Get weight
        weight = None
        while weight is None:
            try:
                weight = float(input('Enter weight in lbs: '))
            except Exception:
                pass

        config = list(cls.presets.values())[response]
        cls_name = list(cls.presets.keys())[response]+str(len(cls._registry))
        cls._registry[cls_name] = cls(weight, **config)
        cls._total_wt = cls._registry[cls_name].update_total(cls._total_wt)

    def update_total(self, _total: dict):
        _total['weight'] += self.weight
        for category in self._composition.keys():
            _total[category] += self._composition[category]

        return _total


def barf_calc():
    help = '(a)dd, (r)emove, (l)ist, (q)uit'
    print('Welcome to BARFCalc!')
    response = ''
    while not re.fullmatch('^[Qq]$', response):
        # Food.display_meal()
        response = input(help+': ')
        if re.fullmatch('^[Aa]$', response):
            Food.add()
        elif re.fullmatch('^[Ll]$', response):
            Food.display_meal()


def main():
    barf_calc()


if __name__ == '__main__':
    main()
