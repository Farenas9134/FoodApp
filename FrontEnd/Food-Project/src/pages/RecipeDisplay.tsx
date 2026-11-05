import { useState, useEffect } from "react";
import { Recipe, RecipeIngredient } from "../types/recipe";
import { useParams } from "react-router-dom";
import axios from "axios";

//@ts-ignore
import placeholderFood from "../assets/foodPics/placeholder-food.jpg"

import { BiArrowBack, BiDish, BiDetail, BiLinkExternal, BiTagAlt } from "react-icons/bi";
import { FaStar, FaStarHalfAlt } from "react-icons/fa";
import { CiClock2, CiViewList } from "react-icons/ci";
import { PiChefHatThin } from "react-icons/pi";
import { Link } from "react-router-dom";

const recipKeepApi = axios.create({
    baseURL: "/api"
})

// Copied from foodcard, should make into component?Hook?idk what it's called
function RecipeRatingStars({ rating }: { rating: number}) {
    return (
        <div className="recipe-rating">
            {Array.from({ length:5 }).map((_, i) => {
                const isFull: boolean = i < Math.floor(rating)
                const isHalf: boolean = !isFull && i < rating && Math.round((rating - Math.trunc(rating)) * 10)/10 >= 0.4
                // Determine if full or half star
                return (
                    <span key={i}>
                        {
                            isFull ? <FaStar fill="#F9AE67" className="w-5 h-5"/> :
                            isHalf ? <FaStarHalfAlt fill="#F9AE67" className="w-5 h-5"/>:
                            <FaStar fill="#D3D3D3"/>
                        }
                    </span>
                )
            })}
        </div>
    )
}

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
        <div className="flex flex-col w-[80%] mx-auto font-display text-[#183C04] mt-2">
            {/* Go back to Recipes */}
            <div className="mb-3">
                <Link 
                    to="/recipes" 
                    className="inline-flex items-center gap-2 text-lg font-semibold text-[#183C04]/80 hover:text-[#C1622D]">
                    <BiArrowBack className="w-6 h-6" />
                    Back to Recipes
                </Link>
            </div>

            {/* Recipe QuickGuide/Info */}
            {/* grid: on defualt use 1 col. On medium screens or larger, use 2 cols */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start mb-10">
                {/* Photo Frame */}
                <div className="rounded-2xl overflow-hidden shadow-lg relative">
                    <img src={recipe.image_url || placeholderFood}
                        alt={recipe.title}
                        className="w-full h-full"/>
                    {recipe.category && (
                    <div className="absolute top-4 left-4 bg-[#FFFDF7]/90 text-[#183C04]/80 text-xs font-bold uppercase tracking-wider px-3 py-1.5 rounded-full shadow-sm">
                        {recipe.category}
                    </div>
                    )}
                </div>

                {/* Recipe details */}
                <div className="flex flex-col gap-5 justify-between">
                    {/* Recipe text based details */}
                    <div>
                        {/* Rating */}
                        <div className="flex items-center gap-1.5 mb-2">
                            <RecipeRatingStars rating={recipe.rating || 0} />
                            <div className="text-lg font-bold text-[#183C04]/80 ml-2">
                                {recipe.rating ? (
                                    <div className="flex">
                                    {recipe.rating}
                                    <p>/ 5</p>
                                    </div>
                                ) : (
                                    <p>No ratings yet</p>
                                )
                                }
                            </div>
                        </div>

                        {/* Title */}
                        {/* defualt size, small screen size, medium screen & larger size helpful af */}
                        <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[#183C04] mb-3">
                            {recipe.title}
                        </h1>

                        {/* Description */}
                        {recipe.description && (
                            <p className="text-[#183C04]/80 leading-relaxed mb-4 text-lg">
                            {recipe.description}
                            </p>
                        )}

                        {/* Tags */}
                        {recipe.tags && recipe.tags.length > 0 && (
                            <div className="flex flex-wrap gap-3 mb-6">
                                {recipe.tags.map((tag, id) => (
                                    <div
                                    key={id}
                                    className="inline-flex items-center gap-1 px-3 py-1.5 bg-[#F1F2E9] border border-[#D3D3D3] rounded-full text-sm font-medium text-[#183C04]">
                                    <BiTagAlt className="w-3.5 h-3.5 text-[#C1622D]" />
                                    {tag}
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Recipe Quick Stats Bar */}
                    <div className="grid grid-cols-3 gap-3 p-4 bg-[#FFFDF7] border border-[#EBE5D8] rounded-xl shadow-sm text-center">
                        <div className="flex flex-col items-center justify-center gap-1">
                            <CiClock2 className="w-6 h-6 text-[#C1622D] stroke-1" />
                            <div className="text-xs text-[#183C04]/60 uppercase font-bold">Time</div>
                            <div className="text-sm font-bold text-[#183C04]">{recipe.total_time ? `${recipe.total_time} mins?` : "N/A"}</div>
                        </div>
                        <div className="flex flex-col items-center justify-center gap-1 border-x border-[#EBE5D8]">
                            <BiDish className="w-6 h-6 text-[#C1622D]" />
                            <div className="text-xs text-[#183C04]/60 uppercase font-bold">Yield</div>
                            <div className="text-sm font-bold text-[#183C04]">{recipe.servings || "N/A servings"}</div>
                        </div>
                        <div className="flex flex-col items-center justify-center gap-1">
                            <BiDetail className="w-6 h-6 text-[#C1622D]" />
                            <div className="text-xs text-[#183C04]/60 uppercase font-bold">Author</div>
                            <div className="text-sm font-bold text-[#183C04]">{recipe.created_by || "Community"}</div>
                        </div>
                    </div>

                    {/* Source Link */}
                    {recipe.source_url && (
                    <a href={recipe.source_url} 
                    className="flex items-center justify-center gap-2 px-6 py-3 bg-[#183C04] hover:bg-[#122e03] text-white font-medium text-sm rounded-full shadow-sm mt-2"
                    // Google says this makes it open in new window
                    target="_blank" 
                    rel="noopener noreferrer">
                        <BiLinkExternal className="w-4 h-4" />
                        View Original Source ({recipe.source_platform || "Website"})
                    </a>
                    )}
                </div>
            </div>

            {/* Recipe Ingredients & Instructions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-start">
                {/* Ingredients */}
                <div className="bg-[#FFFDF7] border border-[#EBE5D8] rounded-2xl shadow-sm p-6">
                    <div className="flex justify-between items-center mb-2 font-semibold">
                        <div className="flex gap-1.5">
                            <CiViewList className="w-6 h-6 text-black"/>
                            <h1 className="text-xl font-bold">Ingredients</h1> 
                        </div>
                        <div className="text-xs font-normal bg-[#F1F2E9] px-2 py-0.5 rounded-full">
                            {ingredients.length} items
                            </div>
                    </div>
                    <ul className="flex flex-col divide-y divide-[#EBE5D8]">
                        {
                            ingredients.map((ingredient, id) => 
                                    <li className="flex justify-between py-3" key={id}>
                                        <div className="flex flex-col text-sm font-semibold text-[#183C04] gap-1.5">
                                            <p>{ingredient.name}</p>
                                            <p className="text-xs text-[#183C04]/60 italic">{ingredient.notes}</p>
                                        </div>
                                        <div className="text-xs font-bold text-[#C1622D] bg-[#FFF3EB] px-2 py-0.5 rounded h-fit">
                                        {ingredient.amount} {ingredient.unit}
                                        </div>
                                    </li>
                            )
                        }
                    </ul>
                </div>

                {/* Instructions */}
                <div className="bg-[#FFFDF7] border border-[#EBE5D8] rounded-xl shadow-sm col-span-2 p-6">
                    <div className="flex justify-center items-center mb-1.5 gap-1.5 font-bold">
                        <PiChefHatThin className="w-6 h-6 text-black stroke-1"/>
                        <h1 className="text-xl font-bold">Recipe Steps</h1>
                    </div>
                    <ul className="flex flex-col">
                        {
                            (recipe.instructions) && recipe.instructions.length >= 1 ? (
                                recipe.instructions.map((step, id) =>
                                        <li className="flex gap-4 items-start py-3" key={id+1}>
                                            <div className="flex items-center justify-center shrink-0 w-8 h-8 rounded-full bg-[#183C04] text-white font-bold text-sm">
                                                {id + 1}
                                            </div>
                                            <p className="text-base text-[#183C04]/90 pt-1">{step}</p>
                                        </li>
                                )
                            ) : (
                                <p>No instructions listed</p>
                            )
                        }
                    </ul>
                </div>
            </div>
        </div>
        );
    }

export default RecipeDisplay