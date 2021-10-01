#!/usr/bin/env python3

import re
import yaml


class Food:
    '''
    weight: total weight of food
    bone: percent of bone in food
    meat: percent of meat in food
    vege: percent of vegetables in Food
    fruit: percent of fruit in Food
    organ: percent of organ in food
    '''

    # Collection of Food objects
    _registry = []

    # Track total weight by category
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
        ''' How to display individual food items '''
        lst = [f'{k:6s}:{v:4.1f}' for k, v in self._composition.items()
               if v != 0.]
        return f'{self.description:34s}|{"|".join(lst)}'

    @staticmethod
    def list_presets(presets: list):
        ''' Print presets '''
        for i, v in enumerate(presets):
            description = v['description']
            print(f'\t{i}) {description}')

    @staticmethod
    def display_total_wt(wt: dict):
        ''' Print toal mix by category'''
        exclusions = ['weight', ]
        categories = [c for c in wt.keys() if c not in exclusions]
        print(f'Total Weight: {wt["weight"]:5.1f}\n')
        print('Mix')
        for category in categories:
            print(f'\t{category}:\t{wt[category]/wt["weight"]:>5.1%}')

    @staticmethod
    def get_preset(presets: list) -> int:
        ''' Get foodtype to add'''
        response = None
        while response not in range(len(presets)):
            try:
                response = int(input('Choose a foodtype to add: '))
            except ValueError:
                continue

        return response

    @classmethod
    def display_meal(cls):
        ''' Print complete meal information'''
        print('\nIngredients')
        # individual items
        for i, v in enumerate(cls._registry):
            print(f'\t{i}) {v}')
        print()
        # Meal mix by category
        cls.display_total_wt(cls._total_wt)

    @classmethod
    def add(cls, weight: float, config: dict):
        ''' Add new Food instance'''
        obj = cls(weight, **config)

        # Update _registry
        cls._registry.append(obj)

        # Update totals
        cls._total_wt = obj.update_total(cls._total_wt)

    @staticmethod
    def get_item_weight(response=None):
        ''' Get weight'''
        weight = None
        while weight is None:
            if response is None:
                response = input('Enter weight in lbs: ')
            try:
                weight = float(response)
            except Exception:
                response = None
                continue

        return weight

    def update_total(self, _total: dict):
        ''' _total is a dictionary tracking meal mix by category'''
        _total['weight'] += self.weight
        for category in self._composition.keys():
            _total[category] += self._composition[category]

        return _total


def barf_calc(presets):
    menu = '(a)dd, (r)emove, (l)ist, (q)uit'
    print('Welcome to BARFCalc!')
    response = ''
    while not re.fullmatch('^[Qq]$', response):
        response = input(menu+': ')

        if re.fullmatch('^[Aa]$', response):
            # Get item type and weight
            Food.list_presets(presets)
            preset = Food.get_preset(presets)
            config = presets[preset]
            weight = Food.get_item_weight()

            # Add instance of Food
            Food.add(weight, config)

        elif re.fullmatch('^[Ll]$', response):
            Food.display_meal()


def main():
    config = 'presets.yaml'
    with open(config, 'r') as fl:
        presets = yaml.safe_load(fl)

    barf_calc(presets)


if __name__ == '__main__':
    main()
