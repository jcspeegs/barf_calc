#!/usr/bin/env python3


from box import Box


class Presets:
    def __init__(self, presets: dict):
        self.presets = presets
        self.ids = self._ids

    @property
    def presets(self):
        return self._presets

    @presets.setter
    def presets(self, value):
        dist_sum = {
            code: sum([v for v in attributes.values() if type(v) is float])
            for code, attributes in value.items()
        }
        for k, v in dist_sum.items():
            assert v == 1.0, f"The component distribution of {k} totals {v} not 1"

        self._presets = Box(value)
        self._ids = list(self._presets.keys())
        for id in self._ids:
            self._presets.get(id).components = Box(
                {k: v for k, v in self._presets.get(id).items() if type(v) is float}
            )


class Food:
    def __init__(self, presets, code: str, weight: float):
        self.presets = presets
        self.code = code
        self.description = self._description
        self.weight = weight
        self.components = {
            k: v * self.weight
            for k, v in self.presets.presets.get(self.code).components.items()
        }

    def __str__(self):
        ingredients = [f"{k:6s}:{v:4.1f}" for k, v in self.components.items()]
        return f'{self.description:34s}{" | ".join(["", *ingredients, ""])}'

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        assert value in self.presets.ids
        self._code = value
        self._description = self.presets.presets.get(value).description


class Meal:
    def __init__(self):
        self.foods = []
        self.weight = 0.0
        self.components = {}

    def __str__(self):
        ingredient_string = "\n".join(
            [f"\t{count}) {str(food)}" for count, food in enumerate(self.foods)]
        )
        if not ingredient_string:
            ingredient_string = "No ingredients added"
        ingredient_string = "\n".join(["Ingredients", ingredient_string])

        weight_string = f"Total Weight: {self.weight:,.2f} lbs"

        mix_string = "\n".join(
            [f"\t{k}:\t{v/self.weight:>5.1%}" for k, v in self.components.items()]
        )
        mix_string = "\n".join(["Mix", mix_string])

        return "\n".join(["", ingredient_string, "", weight_string, "", mix_string])

    def update_meal(self):
        self.weight = sum([food.weight for food in self.foods])
        self.components = {
            component: sum(food.components.get(component, 0) for food in self.foods)
            for component in set(
                {component for food in self.foods for component in food.components}
            )
        }

    def add_food(self, food: Food):
        self.foods.append(food)
        self.update_meal()

    def remove_food(self, item: int):
        del self.foods[item]
        self.update_meal()
