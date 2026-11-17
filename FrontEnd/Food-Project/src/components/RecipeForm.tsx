import { useState, useEffect } from "react";
import Select, {MultiValue} from 'react-select'

export type RecipeFormValues = {
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

interface FormText {
    instructions: string,
    recipe_ingredients: string
}

const emptyFormText: FormText = {
  instructions: '',
  recipe_ingredients: '',
};

type RecipeFormProps = {
    onSubmit: (values: RecipeFormValues) => void;
}

function RecipeForm({ onSubmit }: RecipeFormProps) {
    const [form, setForm] = useState<RecipeFormValues>(emptyRecipe);
    const [formText, setFormText] = useState<FormText>(emptyFormText);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = e.target;

        if (name === 'recipe_ingredients' || name === 'instructions') {
            setFormText(prev => ({ ...prev, [name]: value}))
        }
        // Prev: latest version of form
        // ...prev -> copies every existing field/info into a new RecipeFormValues object
        // [name]:value -> key lookup? Name is the field changed, value is the text/well value
        else {
            setForm(prev => ({ ...prev, [name]: value }));
        }
    }

    const handleAddItem = (e: React.KeyboardEvent<HTMLTextAreaElement>, fieldname: 'instructions'|'recipe_ingredients') => {
        if (e.key === 'Enter') {
            e.preventDefault()
            if (!formText[fieldname].trim()){return}
            setForm(prev => ({ ...prev, [fieldname]: [...prev[fieldname], formText[fieldname]] }))
            setFormText(prev => ({ ...prev, [fieldname]: ''}))
        }
    }

    const handleTagsChanges = (selectedOptions: MultiValue<TagOption>) => {
        const selectedValues = selectedOptions ? selectedOptions.map(option => option.value) : [];
        setForm(prev => ({...prev, tags: selectedValues}))
    }

    const handlePaste = (e: React.ClipboardEvent<HTMLTextAreaElement>, fieldname: 'instructions'|'recipe_ingredients') => {
        e.preventDefault()
        const pastedText = e.clipboardData.getData('text');
        const lines = pastedText.split(/\r?\n/)
        const cleanLines = lines.map((step) =>
            step.replace(/[\u25A2□☐+-]+/g, '').trim()
        ).filter((step) => step !== '');
        setForm(prev => ({ ...prev, [fieldname]: [...prev[fieldname], ...cleanLines]}))
    }

    const handleSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();
        onSubmit(form);
    }

    useEffect(() => {
        console.log(form)
    }, [form])

    return (
        <form onSubmit={handleSubmit}>
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
                    <option value={"Dessert"}>Dessert</option>
                </select>
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
                    form.instructions.length > 0 ? (
                        <ul className="flex flex-col bg-white/90 p-4 mb-3 rounded-2xl text-sm gap-1.5">
                        {
                        form.instructions.map((step, id) => 
                            <li key={id} className="flex gap-3">
                                <p>{id + 1}:</p>
                                <p>{step}</p>
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
                    value={formText.instructions} 
                    onChange={handleChange}
                    onPaste={(e) => handlePaste(e, 'instructions')}/>
                <input type="button" value="Clear" onClick={() => setForm(prev => ({ ...prev, instructions: [] }))}/>
            </div>

            <div className="flex flex-col col-span-full">
                <label>Recipe Ingredients:</label>
                {
                    form.recipe_ingredients.length > 0 ? (
                        <ul className="flex flex-col bg-white/90 p-4 mb-3 rounded-2xl text-sm gap-1.5">
                        {
                        form.recipe_ingredients.map((ing, id) => 
                            <li key={id} className="flex gap-3">
                                <p>{id + 1}:</p>
                                <p>{ing}</p>
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
                    value={formText.recipe_ingredients}
                    onChange={handleChange}
                    onPaste={(e) => handlePaste(e, 'recipe_ingredients')}/>
                <input type="button" value="Clear" onClick={() => setForm(prev => ({ ...prev, recipe_ingredients:[] })) }/>
            </div>
            {/* submit button */}
            <input 
                type='submit' 
                name="submit" 
                value="Submit" 
                className="col-span-full flex mx-auto bg-white w-fit rounded-full px-2 py-0.5 text-med shadow hover:bg-green-500 cursor-pointer"/>
        </fieldset>
        </form>
    )
}

export default RecipeForm