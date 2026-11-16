import { useState, useEffect } from "react"
import RecipeForm, {RecipeFormValues } from "../components/RecipeForm"

function RecipesSubmit() {
    const [showRecipeForm, setShowRecipeForm] = useState<boolean>(false);

    const handleSubmit = (values: RecipeFormValues) => {
        // Do fetch stuff here, need cookies
        console.log('submitting', values);
    }

    return (
        <div className="font-display relative flex flex-col w-full min-h-screen box-border mx-auto p-[3%] gap-10">
            <div className="flex flex-col items-center mx-auto gap-5 w-full">
                <input
                    type="text"
                    placeholder="Insert Link"
                    className="bg-white rounded-full px-3 text-lg w-1/2">
                </input>
                <button
                    onClick={() => setShowRecipeForm(!showRecipeForm)}
                    className="bg-white cursor-pointer rounded-full px-2 text-lg hover:bg-green-400">
                    Manual Option
                </button>
            </div>
            {(showRecipeForm) ?  (
                <RecipeForm onSubmit={handleSubmit}/>
            ): <></>}
        </div>
    )
}

export default RecipesSubmit