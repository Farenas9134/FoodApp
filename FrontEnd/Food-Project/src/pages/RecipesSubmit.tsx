import { useState, useEffect } from "react"
import Select, {MultiValue} from 'react-select'

type RecipeFormValues = {
    title: string;
    source_url: string;
    source_platform: string;
    created_by: string;
    description: string;
    category: string;
    servings: string;
    total_time: string;
    image_url: string;
    tags: string[];
    nutrients: string[];
    instructions: string[];
    recipe_ingredients: string[];
}

const emptyRecipe: RecipeFormValues = {
    title: "", source_url: "", source_platform: "", created_by: "",
    description: "", category: "", servings: "", total_time: "",
    image_url: "", tags: [], nutrients: [], instructions: [], recipe_ingredients: [],
};

type TagOption = {
    value: string;
    label: string;
};

const recipeTags: TagOption[] = [
    {value:'vegetarian', label: 'Vegetarian'},
    {value:'vegan', label: 'Vegan'},
    {value:'gluten-free', label: 'Gluten Free'},
    {value:'high-protein', label: 'High Protein'},
    {value:'low-calorie', label: 'Low Calorie'},
    {value:'halaal', label: 'Halaal'},
]

function RecipesSubmit() {
    const [form, setForm] = useState<RecipeFormValues>(emptyRecipe);
    const [instructionsText, setInstructionsText] = useState<string>('');
    const [instructions, setInstructions] = useState<Array<string>>([]);
    const [ingredientText, setIngredientText] = useState<string>('');
    const [ingredients, setIngredients] = useState<Array<string>>([]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        if (name === 'instructions') {
            setInstructionsText(value)
        }
        else if (name === 'recipe_ingredients') {
            setIngredientText(value)
        }
        // Prev: latest version of form
        // ...prev -> copies every existing field/info into a new RecipeFormValues object
        // [name]:value -> key lookup? Name is the field changed, value is the text/well value
        else {
            setForm(prev => ({ ...prev, [name]: value }));
        }
    }

    const handleAddItem = (e: React.KeyboardEvent<HTMLTextAreaElement>, fieldname: string) => {
        if (e.key === 'Enter') {
            e.preventDefault()
            if (fieldname === 'instructions' && instructionsText.trim()) {
                const updatedInstructions = [...instructions, instructionsText];
                setInstructions(updatedInstructions);
                setInstructionsText('');
                setForm(prev => ({ ...prev, instructions: updatedInstructions }));
            }
            if (fieldname === 'recipe_ingredients' && ingredientText.trim()) {
                const updatedIngredients = [...ingredients, ingredientText];
                setIngredients(updatedIngredients);
                setIngredientText('');
                setForm(prev => ({ ...prev, recipe_ingredients: updatedIngredients }));
            }
        }
    }

    const handleTagsChanges = (selectedOptions: MultiValue<TagOption>) => {
        const selectedValues = selectedOptions ? selectedOptions.map(option => option.value) : [];
        setForm(prev => ({...prev, tags: selectedValues}))
    }

    useEffect(() => {
        console.log('form:', form)
        console.log('instructions', instructions)
        console.log('ingredients', ingredients)
    }, [form, instructions, ingredients])

    return (
        <div className="relative flex flex-col w-full min-h-screen box-border mx-auto pl-[3%] pr-[3%] pt-[3%] gap-10">
            <form>
            <fieldset className="relative grid grid-cols-1 md:grid-cols-2 font-display text-med gap-5 border w-[50%] mx-auto p-6">
                <legend>Recipe Submission</legend>
                <div className="flex flex-col">
                    <label>Recipe Title:</label>
                    <input type="text" name="title" onChange={handleChange} value={form.title} placeholder="Recipe Title" 
                        className=" bg-white rounded-full px-2 py-1" required/>
                </div>
                <div className="flex flex-col">
                    <label>Recipe URL:</label>
                    <input type="text" name="source_url" onChange={handleChange} value={form.source_url} placeholder="Recipe URL" 
                        className=" bg-white rounded-full px-2 py-1"/>
                </div>
                <div className="flex flex-col">
                    <label>Recipe Platform:</label>
                    <select name="source_platform" value={form.source_platform} onChange={handleChange} 
                        className="bg-white rounded-full px-2 py-1 invalid:text-[#5b5b5b]" required>
                        <option value={''} disabled>Select recipe platform</option>
                        <option value={"Instagram"}>Instagram</option>
                        <option value={"TikTok"}>TikTok</option>
                        <option value={"Webpage"}>Webpage</option>
                        <option value={"Personal Recipe"}>Personal Recipe</option>
                    </select>
                </div>
                <div className="flex flex-col">
                    <label>Recipe Author:</label>
                    <input type="text" name="created_by" onChange={handleChange} value={form.created_by} placeholder="Recipe Author" 
                        className=" bg-white rounded-full px-2 py-1"/>
                </div>
                <div className="flex flex-col">
                    <label>Category:</label>
                    <select name="category" value={form.category} onChange={handleChange} 
                        className="bg-white rounded-full px-2 py-1 invalid:text-[#5b5b5b]" required>
                        <option value={''} disabled>Select recipe category</option>
                        <option value={"Breakfast"}>Breakfast</option>
                        <option value={"Lunch"}>Lunch</option>
                        <option value={"Dinner"}>Dinner</option>
                        <option value={"Dessert"}>Dessert</option>                    </select>
                </div>
                <div className="flex flex-col">
                    <label>Servings:</label>
                    <input type="text" name="servings" onChange={handleChange} value={form.servings} placeholder="Servings" 
                        className=" bg-white rounded-full px-2 py-1" required/>
                </div>
                <div className="flex flex-col">
                    <label>Overall Time:</label>
                    <input type="text" name="total_time" onChange={handleChange} value={form.total_time} placeholder="Recipe overall time" 
                        className=" bg-white rounded-full px-2 py-1" required/>
                </div>
                <div className="flex flex-col">
                    <label>Recipe Image WIP (drop? upload?):</label>
                    <input type="text" name="image_url" onChange={handleChange} value={form.image_url} placeholder="Recipe image" 
                        className=" bg-white rounded-full px-2 py-1"/>
                </div>

                <div className="flex flex-col col-span-full">
                    <label>Recipe Tags</label>
                    <Select isMulti name="tags" options={recipeTags} value={recipeTags.filter(option => form.tags.includes(option.value))}
                        onChange={handleTagsChanges} className="bg-white invalid:text-[#5b5b5b]">
                    </Select>
                </div>
                
                <div className="flex flex-col col-span-full">
                    <label>Recipe Description:</label>
                    <textarea name="description" onChange={handleChange} value={form.description} rows={3} 
                        className=" bg-white resize-none p-2 rounded" placeholder="Recipe Description..."></textarea>
                </div>
                <div className="flex flex-col col-span-full">
                    <label>Recipe Steps:</label>
                    {
                        instructions.length > 0 ? (
                            <ul>
                            {
                            instructions.map((step, id) => 
                                <li key={id} className="">
                                    {id + 1}: {step}
                                </li>
                            )}
                            </ul>
                        ):
                        <></>
                    }
                    <textarea 
                        name="instructions" 
                        rows={3} 
                        className=" bg-white resize-none p-2 rounded" 
                        placeholder="Add an instruction and press Enter..." 
                        onKeyDown={(e) => handleAddItem(e, 'instructions')}
                        value={instructionsText} 
                        onChange={handleChange}/>
                    <input type="button" name="clear-inst" value="Clear" onClick={() => setInstructions([])}></input>
                </div>

                <div className="flex flex-col col-span-full">
                    <label>Recipe Ingredients:</label>
                    {
                        ingredients.length > 0 ? (
                            <ul>
                            {
                            ingredients.map((ing, id) => 
                                <li key={id} className="">
                                    {id + 1}: {ing}
                                </li>
                            )}
                            </ul>
                        ):
                        <></>
                    }
                    <textarea 
                        name="recipe_ingredients" 
                        rows={3} 
                        className=" bg-white resize-none p-2 rounded" 
                        placeholder="Add an ingredient and press Enter..." 
                        onKeyDown={(e) => handleAddItem(e, 'recipe_ingredients')}
                        value={ingredientText}
                        onChange={handleChange}/>
                    <input type="button" name="clear-inst" value="Clear" onClick={() => setIngredients([])}></input>
                </div>
                {/* submit button */}
                <input type='submit' name="submit" value="Submit" className="col-span-full flex mx-auto bg-white w-fit rounded-full px-2 py-0.5 text-med shadow hover:bg-green-500 cursor-pointer"/>
            </fieldset>
            </form>

            <div className="relative w-64">
</div>
        </div>
    )
}

export default RecipesSubmit