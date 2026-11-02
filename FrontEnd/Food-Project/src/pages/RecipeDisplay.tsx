import { useState, useEffect } from "react";
import { Recipe, RecipeIngredient } from "../types/recipe";
import { useParams } from "react-router-dom";
import axios from "axios";

const recipKeepApi = axios.create({
    baseURL: "/api"
})

function RecipeDisplay() {
    const { id } = useParams<{ id: string}>();

    // parse ID to check validity
    const recipe_id = id ? parseInt(id, 10) : NaN;
    const isValidId = !isNaN(recipe_id);

    const [recipe, setRecipe] = useState<Recipe>();
    const [ingredients, setIngredients] = useState<RecipeIngredient[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    useEffect( () => {
        async function loadRecipe(validId: number) {
            setError(null)
            setIsLoading(true)

            try {
                const response = await recipKeepApi.get(`/recipes/${validId}`)
                setRecipe(response.data.recipe)
                setIngredients(response.data.ingredients)
            } catch(err) {
                if (err instanceof Error) {
                    setError(err.message)
                }
                else {
                    setError(`Something went wrong! Details: ${err}`)
                }
            } finally {
                setIsLoading(false)
            }
        }

        if (!isValidId) {
            setError("Invalid recipe ID provided.");
            setIsLoading(false);
            return;
        }

        loadRecipe(recipe_id);
    }, [recipe_id, isValidId]);

    if (isLoading) {
        return (
        <div className="flex items-center justify-center min-h-screen">
            <p>Loading recipe...</p>
        </div>
        );
    }

    if (error) {
        return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            <p className="text-red-500">Error: {error}</p>
        </div>
        );
    }

    if (!recipe) {
        return (
            <div>
                <p className="text-red-500"> Error: Recipe undefined</p>
            </div>
        )
    }


    return (
        
        <div className="relative flex flex-col w-full min-h-screen box-border mx-auto pl-[3%] pr-[3%] pt-[3%] gap-10">
            <p>I hope this is loading</p>
            <ul>
                <li>ID: {recipe.recipe_id}</li>
                <li>Title: {recipe.title}</li>
                <li>instructions: {recipe.instructions}</li>
                <li>Tags: {recipe.tags}</li>
                <li>image url: {recipe.image_url}</li>

                <li>
                    ingredient names:
                        {
                            ingredients.map(
                                ingredient => 
                                <div className="text-green-700">
                                    {ingredient.name}
                                </div>
                            )
                        }
                </li>
            </ul>
        </div>
    )
}

export default RecipeDisplay