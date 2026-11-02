// @ts-ignore
import "../css/recipes.css";
import axios from 'axios';
import { ReactElement, useEffect, useState, useRef } from "react";
import { NavigateFunction, useLocation } from "react-router-dom";
import { SuggestedRecipes, Recipe } from "../types/recipe";
import useDebounce from "../components/hooks/useDebounce";
import FoodCard from "../components/UI/FoodCard";
import SearchBar from "../components/SearchBar";
// @ts-ignore
import NathanGIF from "../assets/gifs/nathan-hungry.gif"
import { FaSearch } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const recipKeepApi = axios.create({
    baseURL: "/api"
})

function displayRecipes(recipes: Recipe[]): Array<ReactElement> {
    const recipeCards = recipes.map(
        recipe => 
            <li key={recipe.recipe_id} className="[--card-size:14px]">
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
            </li>
    )
    return recipeCards
}

function displaySuggestedRecipes(recipes: SuggestedRecipes[], navigate:NavigateFunction): React.ReactNode {
    
    const handleViewRecipe = (recipe_id: number) => {
        navigate(`/recipe/${recipe_id}`, {state: recipes} );
    };

    const suggestedRecipeResults = 
    <ul className="absolute flex flex-col bg-[#FFFFFF] font-display gap-1 w-full mx-auto rounded-4xl p-4 pt-13 text-gray-600 -mt-[44px] z-1">
        {
            recipes.map(
                recipe => 
                    <li key={recipe.recipe_id}>
                        <button 
                            className="flex gap-3 items-center ease-in-out hover:bg-gray-200 rounded-2xl p-1 hover:scale-105 hover:cursor-pointer w-full"
                            onClick={() => handleViewRecipe(recipe.recipe_id)}>
                            <FaSearch/>
                            <p>
                                {recipe.title}
                            </p>
                        </button>
                    </li>
            )
        }
    </ul>
    return suggestedRecipeResults
}

function Recipes() {
    const location = useLocation();
    const navigate = useNavigate();

    const [recipes, setRecipes] = useState<Recipe[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [searchTerm, setSearchTerm] = useState<string>('');
    const [suggestedRecipes, setSuggestedRecipes] = useState<SuggestedRecipes[]>([]);
    const [suggestedDisplayOpen, setSuggestedDisplayOpen] = useState<boolean>(false);
    const searchContainerRef = useRef<HTMLDivElement | null>(null);
    
    const debouncedSearchValue = useDebounce(searchTerm, 300);

    const suggestedAbortRef = useRef<AbortController | null>(null);
    const mainRecipesAbortRef = useRef<AbortController | null>(null);
    
    async function loadRecipes(query: string) {
        // Close suggestion display
        setSuggestedDisplayOpen(false)

        // Cancel stale/old recipe requests
        if (mainRecipesAbortRef.current) {
            mainRecipesAbortRef.current.abort();
        }
        const controller = new AbortController();
        mainRecipesAbortRef.current = controller;
        const currentSignal = controller.signal;

        setError(null);
        setIsLoading(true);

        try {
            if (query == '') {
                const response = await recipKeepApi.get('/recipes', {signal: currentSignal})
                setRecipes(response.data.recipes)
            }
            else {
                const response = await recipKeepApi.get(`/recipes/search?title=${encodeURIComponent(query)}`, {signal: currentSignal})
                setRecipes(response.data.recipes)
            }
        } catch(err) {
            // Ignore cancelled stale requests
            if (axios.isCancel(err)) {
                console.log("Previous main recipe search canceled");
                return;
            }
            if (err instanceof Error) {
                setError(err.message)
            }
            else {
                setError(`Something went wrong! Details: ${err}`)
            }
        } finally {
            if (mainRecipesAbortRef.current?.signal === currentSignal) {
                setIsLoading(false);
            }
        }
    }

    async function loadSuggestedRecipes(query: string) {
        // Cancel stale/old requests
        if (suggestedAbortRef.current) {
            suggestedAbortRef.current.abort();
        }

        // If empty, clear suggestions and stop function
        if (!query.trim()) {
            setSuggestedRecipes([]);
            return;
        }

        suggestedAbortRef.current = new AbortController();

        try {
            const response = await recipKeepApi.get(`/recipes/suggest?title=${encodeURIComponent(query)}`, {signal: suggestedAbortRef.current.signal })
            setSuggestedRecipes(response.data.recipes)
        } catch (err) {
            if (axios.isCancel(err)) {
                console.log("Previous search suggestion req. canceled")
                return;
            }

            if (err instanceof Error) {
                setError(err.message)
            } else {
                setError(`Something went wrong! Details: ${err}`)
            }
        }
    }

    // Load in default recipes
    useEffect(() => {
        loadRecipes('');
        setSearchTerm('');

        return () => {
            suggestedAbortRef.current?.abort();
            mainRecipesAbortRef.current?.abort();
        }
    }, [location.key]);

    // Debounce passed in with listener
    useEffect(() => {
        if (debouncedSearchValue.trim().length > 0) {
            loadSuggestedRecipes(debouncedSearchValue);
            setSuggestedDisplayOpen(true)
        } else {
            setSuggestedRecipes([]);
            setSuggestedDisplayOpen(false)
        }

        return () => {
            suggestedAbortRef.current?.abort();
        }
    }, [debouncedSearchValue]);

    // Listener for outside suggestion box clicks to close box
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (
                searchContainerRef.current && 
                !searchContainerRef.current.contains(event.target as Node)
            ) {
                setSuggestedDisplayOpen(false);
            }
        }

        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    return (
        <div className="relative flex flex-col w-full min-h-screen box-border mx-auto pl-[3%] pr-[3%] pt-[3%] gap-10">
            <p className="flex justify-center font-display text-[#183C04] font-medium text-2xl">Browse over 100+ community submitted recipes!</p>

            {/* SEARCHBAR NAV */}
            <div ref={searchContainerRef} className="relative w-[35%] mx-auto">
                <div className="relative z-10">
                    <SearchBar value={searchTerm} onChange={setSearchTerm} onSearch={loadRecipes} onFocus={() => setSuggestedDisplayOpen(true)}/>
                </div>
                <div>
                    {
                    (suggestedDisplayOpen) && suggestedRecipes.length >= 1 ? (
                        displaySuggestedRecipes(suggestedRecipes, navigate)
                    ) : (
                        <></>
                    )
                }
                </div>
            </div>
            
            {/* ERROR DISPLAY */}
            {error && <p className="flex justify-center items-center font-display text-xl text-black bg-[yellow]">{error}</p>}

            {/* RECIPE CARD DISPLAY */}
            <ul className="flex items-center gap-10 flex-wrap justify-center">
                {recipes.length >=1  || isLoading ? (
                    displayRecipes(recipes)
                ) : (
                    <div className="flex flex-col items-center font-display text-xl text-[#183C04] gap-4">
                        <img src={NathanGIF} width={400}/>
                        <p> Womp Womp. No recipe results</p>
                    </div>
                )
                }
            </ul>
        </div>
    );
}

export default Recipes