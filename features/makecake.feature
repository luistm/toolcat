Feature: Make a cake

    As a User,
    I want to see the recipe for a cake,
    So i know how to make one

    Scenario: Build a cake from a random list of ingredients
        Given a random list of cake ingredients
        When a recipe is asked
        Then a recipe is provided