import os
import pymongo
from pprint import pprint
import operator
import re

import datetime
from bson.objectid import ObjectId
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for
# from flask_session import Session
from pymongo import MongoClient
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# from helpers import TODO: Import all helper functions if they're created


# Connect to Mongo DB
# TODO: LOl I need to not have my user/pass in here.
# TODO: Currently this is just using the test collection.
client = pymongo.MongoClient(
    "mongodb+srv://lblais:LcbL348900@cluster0.kvipt.mongodb.net/website_data_test?retryWrites=true&w=majority")
db = client.website_data_test
col = db.recipes_test

# Configure application
app = Flask(__name__)


# Go to new recipe import page
@app.route("/")
def index():
    # TODO: Create an Index Page.  For now, simply redirecting to add_recipe.html
    return redirect("/add_recipe")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("/search.html", recipes=col.find(), count=col.find().count())

    if request.method == "POST":
        # GET QUERY FROM FORM
        q = request.form.get("search")

        # QUERY DB W/ THAT STRING
        query = col.find({"$text": {"$search": q}})
        count = query.count()

        return render_template("/search.html", recipes=query, count=count)


# Render Recipe Import Page
@app.route("/add_recipe", methods=["GET", "POST"])
def input_new_recipe():
    # Get Mixtypes
    # TODO: This should eventually shift to unique mixtypes in the db?
    # TODO: All should eventually transition to a desc frequency search with a cutoff point
    MIXTYPES = ["Shaken", "Stirred", "Built", "Dry-Shake", "Reverse Dry-Shake", "Whip Shake"]
    for mix in col.distinct("mixtype"):
        if mix in MIXTYPES:
            continue
        else:
            MIXTYPES.append(mix)


    # Get Glassmods
    GLASSMODS = ["Absinthe-Rinsed", "Mezcal-Rinsed", "Salt-Rim", "Half-Rimmed w/ Salt"]
    for glassMod in col.distinct("glass_mods"):
        if glassMod in GLASSMODS:
            continue
        else:
            GLASSMODS.append(glassMod)

    # GET POURTYPE #TODO: MAKE THIS GET DISTINCT FROM DB
    POURTYPES = [
        "Strain",
        "Double Strain",
        "Dirty Pour"
    ]
    for pour in col.distinct("pour"):
        if pour in POURTYPES:
            continue
        else:
            POURTYPES.append(pour)

    # Get Icetypes (Eventually remove hard-coded options)
    ICETYPES = ["Neat (No Ice)", "Large Cube", "Crushed Ice", "Pebble Ice", "Shaved Ice", "Cubes"]
    for ice in col.distinct("ice_type"):
        if ice in ICETYPES:
            continue
        else:
            ICETYPES.append(ice)

    # Get Glasstypes
    GLASSTYPES = col.distinct("glassware")

    # If GET, display symbol Search Box #TODO: CHANGE BACK TO REG ADD_RECIPE
    if request.method == "GET":
        return render_template("/add_recipe_2.html", MIXTYPES=MIXTYPES,
                               GLASSTYPES=GLASSTYPES, ICETYPES=ICETYPES,
                               GLASSMODS=GLASSMODS, POURTYPES=POURTYPES)

    # If POST, add to DB and reload add_recipe.html
    if request.method == "POST":

        # Get form data as python dict. Simple k:v pairs for list of size 1, k:v(type list) if more than 1 item
        result = {
            key: value[0] if len(value) == 1 else value
            for key, value in request.form.lists()
        }

        # TODO: Validate form input

        # Magic List of the subfields of ingredients
        magicList = ["qty", "unit", "ingredient", "ing_category"]

        # Create List of Lists with matching indexes for each ingredient
        zipLists = []
        for ind, key in enumerate(magicList):
            tmpCol = []
            for val in result[magicList[ind]]:
                tmpCol.append({key: val})
            zipLists.append(tmpCol)
            del result[key]

        # Create array of ingredients {qty:x}, {unit:x}, and {ingredient:x}
        NumIngredients = len(zipLists[0])
        ingArray = []
        for i in range(NumIngredients):
            row = {}
            for zipList in zipLists:
                # TODO: VALIDATE EMPTIES : if ziplist[i].val
                row.update(zipList[i])
            ingArray.append(row)

        # Add the correctly formatted ingredient array to the results dict.
        result["ingredients"] = ingArray

        # Add Timestamp to results
        result["timestamp"] = datetime.datetime.utcnow()

        # Insert into recipe collection, reload page #TODO: CHANGE BACK TO REG ADD_RECIPE
        col.insert_one(result)
        return redirect("/add_recipe")


@app.route("/recipe/<recipe_id>", )
def recipe(recipe_id):
    recipe = col.find_one({'_id': ObjectId(recipe_id)})

    return render_template("/recipe.html", recipe=recipe)


@app.route("/about")
def about():
    return render_template("/about.html")


@app.route("/stats")
def stats():
    arr = col.distinct("ingredients.ingredient")
    tmp = {}

    for ing in arr:
        freq = col.find({"ingredients.ingredient": ing}).count()
        tmp[ing] = freq

    ingredients = dict(sorted(tmp.items(), key=operator.itemgetter(1), reverse=True))

    return render_template("/stats.html", ingredients=ingredients)

# Ripped from: https://stackoverflow.com/questions/34704997/jquery-autocomplete-in-flask
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    field = request.args.get('n')
    print(field)
    # TODO: Make work for ingredient (as a child of ingredient)
    s = request.args.get('q')
    query = col.find({"$text": {"$search": s}})

    results = []
    for x in query:
        # If ingredient, index in correctly
        if field == 'ingredient':
            for val in x['ingredients']:
                if val['ingredient'] in results:
                    continue
                elif re.search(".*"+s+".*", val['ingredient']):
                    results.append(val['ingredient'])
                else:
                    continue
        else:
            val = x[field]
            if val in results:
                continue
            results.append(val)
    return jsonify(matching_results=results)
