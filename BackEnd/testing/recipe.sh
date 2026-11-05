#!/bin/bash

curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "admin@dev.com",
    "password": "admin"
  }'

# curl -X POST http://localhost:5000/api/recipes \
#   -H "Content-Type: application/json" \
#   -b cookies.txt \
#   -d '{
#     "title": "Browned Butter Chocolate Chip Cookies",
#     "created_by": "Tessa Arias",
#     "tags": ["dessert", "cookies", "chocolate"],
#     "nutrients": [],
#     "rating": 5,
#     "source_url": "https://handle-the-heat.com/browned-butter-chocolate-chip-cookies",
#     "source_platform": "Web",
#     "category": "Dessert",
#     "total_time": 228,
#     "servings": "25 Large Cookies",
#     "description": "Chewy, melty centers, crisp edges, and a rich, nutty brown butter flavor make these some of the best chocolate chip cookies. Best of all, no mixer is required \u2014 just simple steps for bakery-worthy cookies the first time and every time after that!",
#     "image_url": "https://handletheheat.com/wp-content/uploads/2021/10/brown-butter-chocolate-chip-cookie-SQUARE.png",
#     "recipe_ingredients": [
#       "2 sticks (227 grams) unsalted butter",
#       "1/2 cup (100 grams) granulated sugar",
#       "1 1/4 cups (250 grams) lightly packed dark brown sugar",
#       "1 1/2 cups (190 grams) all-purpose flour",
#       "1 cup (127 grams) bread flour",
#       "1 teaspoon baking soda",
#       "1/4 teaspoon baking powder",
#       "1 teaspoon fine sea salt",
#       "2 large eggs plus 1 egg yolk, at room temperature",
#       "2 teaspoons vanilla extract",
#       "1 1/2 cups (255 grams) semisweet chocolate chips",
#       "1 cup (140 grams) semisweet chocolate baking wafers (from Guittard or Valrhona)*",
#       "flaky sea salt (optional)"
#     ],
#     "instructions": [
#       "In a small saucepan set over medium heat, melt the butter. Swirling the pan occasionally, continue to cook the butter. It should become foamy with audible cracking and popping noises.",
#       "Once the crackling stops, continue to swirl the pan until the butter develops a nutty aroma and brown bits start to form at the bottom. When the bits are amber in color, about 2 to 3 minutes after the popping stops, remove from heat and pour into a mixing bowl. Note: You do NOT need to measure the butter after browning, I have engineered this recipe to account for the average water loss.",
#       "Add in the sugars, stir, then set aside to cool completely.",
#       "In a medium or large bowl, combine the flours, baking soda, baking powder, and salt.",
#       "Add the eggs, egg yolk, and vanilla to the browned butter mixture, and stir with a rubber spatula until combined. Slowly stir in the flour mixture until just combined. Stir in the chocolate chips and wafers.",
#       "Wrap the dough in plastic wrap and refrigerate for at least 2 hours, preferably overnight, but no more than 72 hours. Let the dough sit at room temperature until just soft enough to scoop.",
#       "Meanwhile, preheat oven to 350\u00baF. Line baking sheets with parchment paper.",
#       "Divide the dough into 3-tablespoon sized balls using a cookie scoop and drop onto prepared baking sheets, leaving about 3 inches between each piece of dough to spread.",
#       "Bake for 11 to 13 minutes, or until golden brown. Sprinkle with flaky sea salt, if desired. Let cool for 5 minutes before removing to wire racks to cool completely."
#     ]
#   }'

# curl -X DELETE http://localhost:5000/api/recipes/10 \
#   -H "Content-Type: application/json" \
#   -b cookies.txt \