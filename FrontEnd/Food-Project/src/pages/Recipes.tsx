// @ts-ignore
import "../css/recipes.css";
import { useEffect, useState } from "react";
import { GetRecipeResponse, RecipesList, Recipe } from "../types/recipe";
import FoodCard from "../components/UI/FoodCard";

async function fetchRecipes(): Promise<RecipesList> {
    const response = await fetch('/api/recipes');
    if (!response.ok) {
        const errBody = await response.json();
        throw new Error(`${response.status}: ${errBody.error}`)
    }
    const data = await response.json();
    return data;
}

function Recipes() {
    const [recipes, setRecipes] = useState<Recipe[]>([]);
    const [searchTerm, setSearchTerm] = useState<string | ''>('');
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function fetchData(){
            try {
                const data = await fetchRecipes();
                setRecipes(data.recipes);
            }   catch (err) {
                if (err instanceof Error) {
                    setError(err.message)
                }
                else {
                    setError(`Something went wrong! Details: ${err}`)
                }
            }
        }
            fetchData();
    }, []);

    if (error) {
        return <div>Error: {error}</div>
    }

    return (
        <div className="flex flex-col w-full min-h-screen box-border mx-auto pl-[3%] pr-[3%] pt-[3%] gap-10">
            <p className="flex justify-center font-display text-[#183C04] font-medium text-2xl">Browse over 100+ community submitted recipes!</p>

            <div className="flex justify-center font-display">
                <input
                    type="text"
                    placeholder="Search recipes by name, id, or tags"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="bg-[#FFFFFF] rounded-4xl p-1.5 border-1 border-[#CCC] text-[18px] w-[35%]"
                />
            </div>
            
            <div className="flex items-center-safe gap-10 flex-wrap justify-center">
            {recipes.map((recipe) => (
                <div key={recipe.recipe_id} className="[--card-size:14px]">
                    <FoodCard 
                        title={recipe.title}
                        image_url={recipe.image_url}
                        rating={recipe.rating} 
                        total_time={recipe.total_time} 
                        servings={recipe.servings} 
                        // need pantry info here
                        missing_ingredients={0} 
                        pantry_ratio= {0.9}
                        recipe_id={recipe.recipe_id}/>
                </div>
                ))}
            </div>
        </div>
    );
}

export default Recipes