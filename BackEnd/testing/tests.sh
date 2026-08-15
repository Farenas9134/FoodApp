#!/bin/bash

# run in a bash terminal with "bash tests.sh"

# Creating a curl command:
# 'curl url' -> makes a simple GET request to the url
# -X sets the HTTP method
# -d send body data in your request
# -H adds custome headers 'Content-Type: application/json'
# -u pass login info username:password
# -v print the full request and response details for debugging

# ===================================================

# QUICK LOGIN
# curl -X POST http://127.0.0.1:5000/login   -H "Content-Type: application/json"   -d '{"email":"bash-test@gmail.com", "password":"bash"}'   -c cookies.txt

# REUSE COOKIES COMMAND
# curl blah blah -b cookies.txt

# ===================================================

# Base config (change as needed if the port is diff)
URL="http://127.0.0.1:5000"

# Counter variables
TEST_COUNT=0
PASSED=0
FAILED=0

run_test() {
    local expected_status="$1"
    local label="$2"
    # shift arguments so remainder can be passed to curl
        # (1,2,3) -> shift -> (2,3)
    shift 2 # this would remove expected_status and label from argumemts

    TEST_COUNT=$((TEST_COUNT + 1))

    # Run request and capture response
    local response
    response=$(curl -s -i "$@")

    # Extract HTTP status code from the first header line
    local status_code
    status_code=$(echo "$response" | head -n 1 | awk '{print $2}' | tr -d '\r')

    # Uncomment if you want to see passed tests
    # echo -e "\n====================="
    # echo " TEST #$TEST_COUNT: $label"
    # echo "=========================="
    # echo "$response"

    # Eval assertion
    if [ "$status_code" -eq "$expected_status" ] 2>/dev/null; then
        echo -e "\033[0;32m[PASS]\033[0m Status: $status_code"
        PASSED=$((PASSED + 1))
    else
        # Only print details when test fails (tests are long af)
        echo -e "\n=========================="
        echo " TEST #$TEST_COUNT: $label"
        echo "=========================="
        echo "$response"
        echo -e "\033[0;31m[FAIL]\033[0m Expected $expected_status, got '$status_code'"
        FAILED=$((FAILED + 1))
    fi
}

# --- API TESTS ---

# format -> run_test [expected status] [test description] [curl command args]

# ============= TESTING AUTHORIZATION ROUTES ================
# 1. User Sign Up
run_test 201 "POST sign up new user" \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "email": "bash-test2@gmail.com",
        "name": "Bash Tester2",
        "password": "bash2"
    }' \
    "$URL/signup"

run_test 400 "POST sign up with existing email" \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "email": "bash-test2@gmail.com",
        "name": "Bash Tester2",
        "password": "bash2"
    }' \
    "$URL/signup"


# 2. User Log In
run_test 201 "POST login with proper credentials" \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "email": "bash-test2@gmail.com",
        "password": "bash2"
    }' \
    -c cookies.txt \
    "$URL/login"

run_test 400 "POST login with improper credentials" \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "email": "bash-test2@gmail.com",
        "password": "bash3"
        }' \
    -c cookies.txt \
    "$URL/login"

# 3. Save recipes
run_test 201 "POST save recipe" \
    -X POST \
    -H "Content-Type: application/json" \
    -b cookies.txt \
    "$URL/user/recipes/3"

# 4. Delete recipes
run_test 200 "DELETE saved recipe" \
    -X DELETE \
    -H "Content-Type: application/json" \
    -b cookies.txt \
    "$URL/user/recipes/3"

run_test 404 "DELETE recipe you haven't saved" \
    -X DELETE \
    -H "Content-Type: application/json" \
    -b cookies.txt \
    "$URL/user/recipes/1"

# 5. Delete user
run_test 200 "DELETE user profile" \
    -X DELETE \
    -H "Content-Type: application/json" \
    -b cookies.txt \
    "$URL/user"

# 6. Forgot password
run_test 200 "POST forgot password" \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "email": "bash-test2@gmail.com"
        }' \
    -b cookies.txt \
    "$URL/forgot-password"

TOKEN=$(python -m sqlite3 instance/db.sqlite \
    "SELECT reset_token FROM user WHERE email='bash-test2@gmail.com';")

echo "Token: $TOKEN"

# 7. Reset password
run_test 200 "POST reset password" \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{
        "password": "newbash"
        }' \
    -b cookies.txt \
    "$URL/reset-password/$TOKEN"


# ============= TESTING RECIPE ROUTES ================

# # 1. GET all recipes
# run_test 200 "GET all recipes" "$URL/recipes"

# # 2. Submit New Recipe
# run_test 201 "POST submit recipe with all fields" \
#     -X POST \
#     -H "Content-Type: application/json" \
#     -d '{
#         "title": "Change Me!",
#         "source_url": "changeMe.com",
#         "source_platform": "Instagram",
#         "ingredients": "Changes, Life, Unemployment",
#         "instructions": "step 1) Change Everything. Step 2) Be better",
#         "image_url": "change.jpg",
#         "created_by": "Chef Change"
#     }' \
#     "$URL/recipes-submit"

# run_test 400 "POST submit existing recipe" \
#     -X POST \
#     -H "Content-Type: application/json" \
#     -d '{
#         "title": "Change Me!",
#         "source_url": "changeMe.com",
#         "source_platform": "Instagram",
#         "ingredients": "Changes, Life, Unemployment",
#         "instructions": "step 1) Change Everything. Step 2) Be better",
#         "image_url": "change.jpg",
#         "created_by": "Chef Change"
#     }' \
#     "$URL/recipes-submit"

# run_test 401 "POST submit recipe with missing fields" \
#     -X POST \
#     -H "Content-Type: application/json" \
#     -d '{
#         "source_url": "Missing.com",
#         "source_platform": "Missing title",
#         "ingredients": "Bad Bad if added",
#         "instructions": "step 1) Change Everything. Step 2) Be better",
#         "image_url": "missing.jpg",
#         "created_by": "Chef Missing"
#     }' \
#     "$URL/recipes-submit"

# run_test 400 "POST submit recipe with empty JSON" \
#     -X POST \
#     -H "Content-Type: application/json" \
#     -d '{}' \
#     "$URL/recipes-submit"

# run_test 400 "POST submit recipe with broken JSON syntax" \
#     -X POST \
#     -H "Content-Type: application/json" \
#     -d '{"title": "Broken", "source_url":}' \
#     "$URL/recipes-submit"

# # 3. Search Recipe
# run_test 200 "Search /recipes/search "Change Me"" \
#     -H "Content-Type: application/json" \
#     "$URL/recipes/search?q=Change+Me"

# # 4. Update Recipe
# run_test 200 "Update recipe you own" \
#     -X PUT \
#     -H "Content-Type: application/json" \
#     -d '{
#         "title" : "Changed You!",
#         "tags" : "silly, testy, unreal"
#     }' \
#     "$URL/recipes/20"

# run_test 403 "Update recipe you don't own" \
#     -X PUT \
#     -H "Content-Type: application/json" \
#     -d '{
#         "title" : "Changed You Woops Not Good!"
#     }' \
#     "$URL/recipes/1"

# run_test 400 "PUT recipe title that conflicts with existing recipe" \
#     -X PUT \
#     -H "Content-Type: application/json" \
#     -d '{ "title": "Christmas pie" }' \
#     "$URL/recipes/20"

# # 5. Delete Recipe
# run_test 200 "DELETE recipe you own" \
#     -X DELETE \
#     -H "Content-Type: application/json" \
#     "$URL/recipes/20"

# run_test 401 "DELETE recipe you don't own" \
#     -X DELETE \
#     -H "Content-Type: application/json" \
#     "$URL/recipes/1"

# # 6. Search for Recipes
# run_test 200 "Search for an existing recipe" \
#     "$URL/recipes/1"

# run_test 404 "Search for a recipe that doesn't exist" \
#     "$URL/recipes/99999999999"

# run_test 404 "GET recipe with non-integer ID" \
#     "$URL/recipes/abc"

# # 7. General Edge Cases
# run_test 405 "POST to /recipes (Method Not Allowed)" \
#     -X POST \
#     "$URL/recipes"

echo ""
echo "==============="
echo "TEST RESULTS:"
echo "==== TOTAL TEST: $TEST_COUNT"
echo "==== TEST PASSED: $PASSED"
echo "==== TEST FAILED: $FAILED"