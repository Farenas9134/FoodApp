// @ts-ignore
import "../../css/FoodCard.css"
// @ts-ignore
import cookies from "../../assets/foodPics/cookies.jpg"
import { FaStar, FaStarHalfAlt } from 'react-icons/fa';
import { CiClock2 } from 'react-icons/ci'
import { BiDish, BiSolidDoughnutChart } from 'react-icons/bi'
import { useNavigate } from "react-router-dom";

interface FoodCardProps{
    title: string;
    image_url: string;
    rating: number;
    total_time: number;
    servings: string;
    missing_ingredients?: number;
    pantry_ratio?: number;
    recipe_id: number;
}

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
                            isFull ? <FaStar fill="#F9AE67"/> :
                            isHalf ? <FaStarHalfAlt fill="#F9AE67"/>:
                            <FaStar fill="#D3D3D3"/>
                        }
                    </span>
                )
            })}
        </div>
    )
}

function FoodCard(
    { title, image_url, rating, total_time, servings, missing_ingredients, pantry_ratio, recipe_id}
    : FoodCardProps) {

    const navigate = useNavigate();

    const handleViewRecipe = () => {
        navigate(`/recipe/${recipe_id}`);
    };

    return (
        <div className="FoodCard">
            <div className="image-frame">
                <img 
                    src={image_url || cookies} 
                    alt="Placeholder recipe image"
                    className="card-image"/>
            </div>
            <div className="recipe-info">
                <div className="recipe-rating">
                    {/* 3 PLACED FOR NOW TO SEE EFFECTS. SHOULD BE NONE OR MSG IF RATING MISSING */}
                    <RecipeRatingStars rating={rating || 0} />
                </div>
                < div className="recipe-name">
                    {title || 'Recipe Name Missing'}
                </div>
                < div className="recipe-stats">
                    <div className="recipe-stats-box">
                        <CiClock2/>
                        {total_time || 'N/A'}
                    </div>
                    <div className="recipe-stats-box">
                        <BiDish/>
                        {servings || 'N/A'}
                    </div>
                </div>
            </div>
            <div className="pantry-info">
                <div>
                    <BiSolidDoughnutChart size={"2.5em"}/>
                </div>
                <div className="pantry-text">
                    <div className="pantry-ratio">
                        pantry ratio: {pantry_ratio || 'N/A'}
                    </div>
                    missing ingredients: {missing_ingredients ?? 'N/A'}
                </div>
            </div>
            <button 
                type="button"
                className="w-[90%] h-[2.5em] bg-[#183C04] text-white flex items-center justify-center text-[1em] rounded-[0.625em] shadow-[0_0.375em_0.25em_grey]> hover:bg-green-700 hover:scale-105 hover:cursor-pointer" 
                onClick={handleViewRecipe}>
                    View Recipe
            </button>
        </div>
    )
}

export default FoodCard