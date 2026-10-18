export interface RecipeIngredient {
    recipe_ingredient_id: number;
    recipe_id: number;
    ingredient_id: number;
    name: string;
    amount: number;
    unit: string;
    notes?: string;
    calories?: number;
    protein_g?: number;
    carbs_g?: number;
    fat_g?: number;
    is_verified?: boolean;
    created_by?: number;
    is_deleted?: boolean;
}

export interface Recipe {
    // Core recipe fields
    title: string;
    recipe_id: number;
    source_url: string;
    source_platform: string;
    instructions?: Array<string>;
    image_url: string;
    tags: Array<string>;
    submitted_by: number;
    created_by: string;
    created_at: string;
    last_updated: string;
    
    // nutritional, time, etc.
    nutrients: Array<string>;
    description: string;
    total_time: number;
    category: string;
    rating: number;
    servings: string;
}

export interface GetRecipeResponse {
  recipe: Recipe;
  ingredients: RecipeIngredient[];
}

export interface RecipesList {
    'recipes': Array<Recipe>;
    'total': string;
    'pages': string;
    'current_page': string;
    'has_next': string;
    'has_prev': string;
}