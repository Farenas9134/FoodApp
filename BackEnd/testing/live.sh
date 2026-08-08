#!/bin/bash

# run in a bash terminal with "bash live.sh"

# Creating a curl command:
# 'curl url' -> makes a simple GET request to the url
# -X sets the HTTP method
# -d send body data in your request
# -H adds custome headers 'Content-Type: application/json'
# -u pass login info username:password
# -v print the full request and response details for debugging

URL="http://127.0.0.1:5000"

# Recipe route testing
RESULT=$(curl -v $URL"/recipes")
echo $RESULT

RESULT=$(
    curl -i -X POST -H "Content-Type: application/json" -d '{
    "title": "Change Me!",
    "source_url": "changeMe.com",
    "source_platform": "Instagram",
    "ingredients": "Changes, Life, Unemployment",
    "instructions": "step 1) Change Everything. Step 2) Be better",
    "image_url": "change.jpg",
    "created_by": "Chef Change"
    }' http://127.0.0.1:5000/recipes-submit
)
echo $RESULT

RESULT=$(
    curl -i -X PUT -H "Content-Type: application/json" -d '{
    "title": "Changed You!"
    }' http://127.0.0.1:5000/recipes/2
    )
echo $RESULT
