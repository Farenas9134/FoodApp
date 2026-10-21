# ReciKeep Backend API

Flask + Flask-Login + SQLAlchemy (SQLite). All request/response bodies are JSON unless noted.

## Contents

1. [Conventions](#conventions)
2. [Auth](#auth)
3. [Recipes](#recipes)
4. [Ingredients](#ingredients)
5. [Pantry](#pantry)
6. [User, saved recipes, and follows](#user-saved-recipes-and-follows)
7. [Admin / debug routes](#admin--debug-routes)
8. [Data shapes](#data-shapes)
9. [Known quirks to plan around](#known-quirks-to-plan-around)

---

## Conventions

**Authentication.** Session-cookie based (Flask-Login). `POST /login` sets the cookie. The frontend must send cookies on every request. Routes marked 🔒 require a logged-in user.

**Pagination.** List endpoints accept `?page=1&per_page=10` and return:

```json
{
  "<items_key>": [ ... ],
  "total": 42,
  "pages": 5,
  "current_page": 1,
  "has_next": true,
  "has_prev": false
}
```

`per_page` is capped at 100 on all `GET /` routes where pagination is present.

**Errors.** Most errors look like:

```json
{ "error": "Human-readable message", "details": "Extra info or 'Refer to documentation...'" }
```


---

## Auth

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/signup` | – | Create account |
| POST | `/login` | – | Log in, sets session cookie |
| GET | `/logout` | 🔒 | Log out |
| POST | `/forgot-password` | – | Generate a reset token |
| POST | `/reset-password/<token>` | – | Set a new password |

### POST `/signup`

```json
{ "email": "abc@def.com", "name": "Turtles", "password": "secret" }
```

- `201`: `{ "message": "User created successfully", "user": { "email", "name" } }`
- `400`: invalid JSON, missing fields, or email already registered (each has a distinct `error` message)

### POST `/login`

```json
{ "email": "abc@def.com", "password": "secret" }
```

- `200`: `{ "message": "Successful login" }` (+ session cookie)
- `400`: missing fields, unknown email, or wrong password (each has a distinct `error` message).

### GET `/logout` 🔒

- `200`: `{ "message": "Successful logout" }`
- `401`: Missing authorization/login creds 

### POST `/forgot-password`

```json
{ "email": "abc@def.com" }
```

- `200`: `{ "message": "Password reset link successfully sent to your email" }`
- `400`: missing email or user doesn't exist.
- Stores a 1-hour token on the user. **No email is actually sent yet**

### POST `/reset-password/<token>`

```json
{ "email": "abc@def.com", "password": "newSecret" }
```

- `200`: `{ "message": "Password successfully reset" }`
- `400`: missing email/password, or invalid/expired token.

---

## Recipes

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/recipes` | 🔒 | Create a recipe |
| GET | `/recipes` | – | Paginated list (newest first) |
| GET | `/recipes/<recipe_id>` | – | Full recipe + ingredients |
| GET | `/recipes/search` | – | Filter by fields |
| GET | `/recipes/recent` | – | Recipes from the last 7 days |
| PUT | `/recipes/<int:recipe_id>` | 🔒 | Update (owner only) |
| DELETE | `/recipes/<int:recipe_id>` | 🔒 | Delete (owner only) |

### POST `/recipes` 🔒

**Every** field below must be present in the body, or you get a `400` listing what's missing.

```json
{
  "title": "Garlic Butter Chicken",
  "source_url": "https://example.com/post/123",
  "source_platform": "instagram",
  "created_by": "some_influencer",
  "description": "Quick weeknight chicken",
  "category": "main course",
  "servings": "4",
  "total_time": 35,
  "rating": 4.5,
  "image_url": "https://example.com/img.jpg",
  "instructions": ["Season chicken", "Sear 5 min per side", "eat"],
  "nutrients": [],
  "tags": {},
  "recipe_ingredients": ["2 lbs chicken breast", "3 cloves garlic, minced", "2 tbsp butter"]
}
```

- `recipe_ingredients` here is a **list of raw strings**. They're parsed server-side (`ingredient_parser`) into name / amount / unit / notes. Ingredients that don't exist yet are auto-created (unverified, owned by the submitting user).
- `submitted_by` is set from the logged-in user. Don't send it.
- `201`: `{ "message": "Recipe created successfully", "recipe": {…} }`
- `400`: bad JSON, missing fields, zero ingredients, or duplicate (`source_url` is globally unique; `title` is unique per user). `details` contains the raw exception text.

### GET `/recipes`

Query: `page`, `per_page` (max 100).
Returns `{ "recipes": [...], ...pagination }`.

### GET `/recipes/<recipe_id>`

```json
{
  "recipe": { "...all recipe fields, including instructions..." },
  "ingredients": [
    { "name": "chicken breast", "recipe_ingredient_id": 12, "amount": 2.0, "unit": "pound", "notes": "" }
  ]
}
```

- `404` (HTML) if not found.

### GET `/recipes/search`

Query params are recipe field names. Each value is matched with a case-insensitive "contains", and **all conditions are ANDed**. A param can be repeated.

```
/recipes/search?title=chicken&category=main&tags=spicy&tags=quick
```

Searchable: `title`, `description`, `category`, `servings`, `source_platform`, `source_url`, `created_by`, `submitted_by`, `tags`, `nutrients`, `rating`, `total_time`.
**Not** searchable: `instructions`, `image_url`, timestamps, and ingredients.

- No query params at all returns empty → `{ "recipes": [] }` (no pagination keys).
- Otherwise returns the standard paginated shape with `recipes` (no `instructions`). `page` and `per_page` are accepted.

### GET `/recipes/recent`

Recipes created in the last 7 days, newest first. Returns `{ "recipes": [...], "total", "pages", "current_page", "has_next", "has_prev" }`

### PUT `/recipes/<int:recipe_id>` 🔒

Owner only (`403` otherwise). Send any subset of recipe fields with updated information.

```json
{
  "title": "New title",
  "rating": 4.0,
  "recipe_ingredients": [
    { "name": "chicken breast", "amount": 1.5, "unit": "lb" },
    { "name": "olive oil", "amount": 2, "unit": "tbsp" }
  ]
}
```

- !!! `recipe_ingredients` here is a **list of objects** (`name`, `amount`, `unit`), unlike POST, which takes raw strings.
- The list is treated as the new full set: ingredients matched by name are updated, new names are added, and any existing ingredient **not in your list is removed**.
- Field values are type-checked against the column's Python type (e.g. `rating` must be a float, so send `4.0`, not `4`). Wrong type → `400`.
- `title` / `source_url` collisions → `400`.
- `200`: `{ "message", "recipe": {…}, "ingredients": [...] }`

### DELETE `/recipes/<int:recipe_id>` 🔒

Owner only. 
- `200`: `{ "message": "Recipe deleted successfully" }`. Its `RecipeIngredient` rows are removed with it.

---

## Ingredients

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/ingredients` | 🔒 | Create a custom ingredient |
| GET | `/ingredients` | optional | Paginated visible ingredients |
| GET | `/ingredients/<ingredient_id>` | optional | One ingredient |
| GET | `/ingredients/search?q=` | optional | Name search |
| PUT | `/ingredients/<ingredient_id>` | 🔒 | Edit (creator only) |
| DELETE | `/ingredients/<ingredient_id>` | 🔒 | Delete (creator only) |

**Visibility rule:** logged-out users see only verified (staple) ingredients. Logged-in users see verified ones plus their own. Soft-deleted ingredients are always hidden.

### POST `/ingredients` 🔒

```json
{ "name": "Chicken Breast", "calories": 165, "protein_g": 31, "carbs_g": 0, "fat_g": 3.6 }
```

All five fields are required. The name is trimmed and lowercased.

- `201`: `{ "message": "Ingredient created successfully", "ingredient": {…} }`
- `400`: missing body, missing fields, or an ingredient with that name already exists.

### GET `/ingredients` and GET `/ingredients/search?q=chick`

Paginated; response key is `ingredients`. Search is a case-insensitive "contains" on `name` (Ex. 'CHick' would return 'chicken').
- `200`: `{ "ingredients": [...], "total", "pages", "current_page", "has_next", "has_prev" }`

### GET `/ingredients/<ingredient_id>`

- `200`: `{ "ingredient": {…} }`
- `404` if not found or not visible.

### PUT `/ingredients/<ingredient_id>` 🔒

Editable: `name`, `calories`, `protein_g`, `carbs_g`, `fat_g`, `is_deleted`. 
- `403`: Verified (staple) ingredients cannot be edited. Only the creator of ingredient can edit.
- `200`: `{ "message", "ingredient": {…} }`

### DELETE `/ingredients/<ingredient_id>` 🔒

When deleted, and live recipes still reference ingredient, then it's soft-deleted (hidden but still referenced). Otherwise it's removed completely. Both cases return 200.
- `200`, `{ "message": "Ingredient deleted successfully!" }`.
- `403`: Not creator of ingredient.

---

## Pantry

All routes 🔒.

| Method | Path | Purpose |
|---|---|---|
| GET | `/pantry` | List the user's pantry |
| POST | `/pantry` | Add ingredients by id |
| DELETE | `/pantry` | Remove ingredients by id |
| GET | `/pantry-match` | Recipes ranked by pantry overlap |

### GET `/pantry`

`200`: `{ "pantry": [ { "name": "...", "pantry_id": 3, "user_id": 1 } ] }`

### POST `/pantry` / DELETE `/pantry`

```json
{ "ingredients": [1, 5, 9] }
```

A list of **ingredient ids**. Invalid, invisible, and already-present ids are skipped.

- POST `200`: `{ "message": "Successfully added N ingredients into User Pantry" }`, or a message saying all were already present. `400` if none of the ids are valid.
- DELETE `200`: `{ "message": "Successfully removed given ingredients from pantry!" }`, or a message saying none were in the pantry.
- An empty/missing `ingredients` list returns `200` with `{ "message": "No ingredients provided" }`.

### GET `/pantry-match`

Query: `min_match_percentage` as a **fraction from 0 to 1** (default `0.8`; invalid values fall back to `0.8`). Not paginated.

```json
{
  "recipes_matched": [
    {
      "...recipe fields (no instructions)...": "",
      "match_info": {
        "total_required": 8,
        "total_matched": 7,
        "missing_count": 1,
        "match_percentage": 87.5
      }
    }
  ]
}
```

Sorted by match ratio, then by number of ingredients (both descending). Recipes with zero ingredient rows never appear.

---

## User, saved recipes, and follows

All routes 🔒.

| Method | Path | Purpose |
|---|---|---|
| GET | `/user` | Greeting with current user's id |
| DELETE | `/user` | Delete account |
| GET | `/user/recipes` | Saved recipes (paginated, newest saved first) |
| POST | `/user/recipes/<recipe_id>` | Save a recipe |
| DELETE | `/user/recipes/<recipe_id>` | Unsave a recipe |
| POST | `/user/follow/<user_id>` | Follow a user |
| DELETE | `/user/unfollow/<user_id>` | Unfollow a user |
| GET | `/user/followers` | Who follows me (paginated) |
| GET | `/user/followings` | Who I follow (paginated) |

- **GET `/user`** → `{ "message": "hello _____! Your id is 1" }`. It's a string, not structured user data.
- **GET `/user/recipes`** → `{ "saved_recipes": [...], ...pagination }`
- **POST `/user/recipes/<recipe_id>`** → `201`: `{ "message": "success", "recipe_saved": "<title> successfully saved to users recipes" }`. `404` (HTML) if the recipe doesn't exist.
- **DELETE `/user/recipes/<recipe_id>`** → `200`: `{ "message": "Recipe deleted successfully" }`; `404` JSON if it wasn't saved. (This only removes the *saved* link, not the recipe.)
- **POST `/user/follow/<user_id>`** → `201`: `{ "message": "You have successfully followed <name>" }`. `404` unknown user, `400` if following yourself.
- **DELETE `/user/unfollow/<user_id>`** → returns `{ "message": "You have successfully unfollowed <name>" }`. Same `404` / `400` cases.
- **GET `/user/followers`** → `{ "followers": [ { "user_id", "name", "email" } ], ...pagination }`
- **GET `/user/followings`** → `{ "following": [ { "user_id", "name", "email" } ], ...pagination }`
- **DELETE `/user`** → deletes the user's saved recipes, their submitted recipes, and the account, then logs out. `200`: `{ "message": "Successfully deleted user and attached recipes!" }`.

---

## Admin / debug routes

Not meant for the frontend.

| Method | Path | Notes |
|---|---|---|
| GET | `/all-users` | 🔒 + admin only. Lists users with follower/following counts. Marked "testing route only". |
| GET | `/recipeIng` | Admin only. Paginated dump of every `RecipeIngredient` row (key: `recipe Ingredient`), used to verify cascade deletes. |

---

## Data shapes

**Recipe**

| Field | Type | Notes |
|---|---|---|
| `recipe_id` | int | |
| `title` | string (≤100) | unique per submitting user |
| `source_url` | string (≤1000) | globally unique |
| `source_platform` | string | |
| `instructions` | JSON | list of steps |
| `image_url` | string | |
| `description` | string (≤1000) | |
| `category` | string | |
| `servings` | string | |
| `total_time` | int | |
| `rating` | float | 0–5 |
| `nutrients` | JSON | |
| `tags` | JSON | |
| `submitted_by` | int | user id |
| `created_by` | string | influencer / original author name |
| `created_at`, `last_updated` | ISO-8601 string | UTC |

**Ingredient**

| Field | Type | Notes |
|---|---|---|
| `id` | int | Use this id for `POST`/`DELETE /pantry` |
| `name` | string (≤100) | trimmed and lowercased on create |
| `calories` | float | required on create |
| `protein_g` | float | required on create |
| `carbs_g` | float | required on create |
| `fat_g` | float | required on create |
| `is_verified` | bool | `true` = staple ingredient, admin-managed |
| `created_by` | int or null | id of the user who created it |
| `is_deleted` | bool | soft-delete flag; deleted ingredients are hidden from lists |

**Recipe ingredient** (items in `GET /recipes/<id>` → `ingredients`)

All **Ingredient** fields above, plus:

| Field | Type | Notes |
|---|---|---|
| `recipe_ingredient_id` | int | id of the link row, not the ingredient |
| `amount` | float | defaults to 0.0 |
| `unit` | string | may be empty |
| `notes` | string (≤200) | parser comments, e.g. "minced" |

Note: `id` is the ingredient's id; `recipe_ingredient_id` identifies this recipe's usage of it.

**Pantry item** (items in `GET /pantry` → `pantry`)

All **Ingredient** fields above, plus:

| Field | Type | Notes |
|---|---|---|
| `pantry_id` | int | id of the pantry row |
| `user_id` | int | owner of the pantry |

**Saved recipe** (items in `GET /user/recipes` → `saved_recipes`)

Returned as full **Recipe** objects (including `instructions`), ordered by when they were saved.

**User summary** (items in `GET /user/followers` and `GET /user/followings`)

| Field | Type |
|---|---|
| `user_id` | int |
| `name` | string |
| `email` | string |

**Match info** (added to each recipe in `GET /pantry-match`)

| Field | Type | Notes |
|---|---|---|
| `total_required` | int | ingredients the recipe needs |
| `total_matched` | int | how many are in the user's pantry |
| `missing_count` | int | `total_required - total_matched` |
| `match_percentage` | float | 0–100, rounded to 1 decimal |

**Pagination envelope** (all paginated list endpoints)

| Field | Type |
|---|---|
| `total` | int |
| `pages` | int |
| `current_page` | int |
| `has_next` | bool |
| `has_prev` | bool |

---

## Known bugs/issues/oddities

1. **POST and PUT `/recipes` disagree on `recipe_ingredients`.** POST takes raw strings (`"2 cups flour"`); PUT takes `{name, amount, unit}` objects and deletes anything omitted.
2. **Password reset doesn't send email.** It only stores the token.
- TBD needs more testing tbh