#!/usr/bin/env python

import click
import yaml
import barf_calc as bc
import re
from importlib.resources import files


PRESETS = files("barf_calc").joinpath("presets.yaml")


def food_type_weight(presets, weight=None, item=None):
    string = "\n".join(
        [
            f"\t{c}) {presets.presets.get(i).description}"
            for c, i in enumerate(presets.ids)
        ]
    )
    click.echo(string)

    while item not in [str(opt) for opt in range(len(presets.ids))]:
        item = input("Choose a foodtype to add: ")

    while type(weight) != float:
        try:
            weight = float(input("Enter weight in lbs: "))
        except ValueError:
            continue

    return int(item), weight


def meal_item(meal: bc.Meal, item=None) -> int:
    click.echo(meal)
    while item not in [str(opt) for opt in range(len(meal.foods))]:
        item = input("Choose item to remove from meal: ")

    return int(item)


@click.command()
@click.option(
    "--presets",
    type=click.File("r"),
    default=PRESETS,
    help="YAML list of food types and their composition",
)
def barf_calc(presets, meal: bc.Meal = bc.Meal()):
    presets = yaml.safe_load(presets)
    presets = bc.Presets(presets)

    click.echo("Welcome to BARFCalc!")
    menu = "(a)dd, (r)emove, (l)ist, (q)uit"
    response = ""
    while not re.fullmatch("^[Qq]$", response):
        response = input(menu + ": ")

        if re.fullmatch("^[Aa]$", response):
            # Add item of Food to meal
            item, weight = food_type_weight(presets)
            food = bc.Food(presets, presets.ids[item], weight)
            meal.add_food(food)

        elif re.fullmatch("^[Ll]$", response):
            click.echo(meal)

        elif re.fullmatch("^[Rr]$", response):
            # Remove item from meal
            item = meal_item(meal)
            click.echo(f"Removing {item}) {meal.foods[item]}")
            meal.remove_food(item)


if __name__ == "__main__":
    barf_calc()
