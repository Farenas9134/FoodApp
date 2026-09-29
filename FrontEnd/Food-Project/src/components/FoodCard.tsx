// @ts-ignore
import "../css/FoodCard.css"
// @ts-ignore
import cookies from "../assets/cookies.jpg"
import { FaStar } from 'react-icons/fa';
import { CiClock2 } from 'react-icons/ci'
import { BiDish, BiSolidDoughnutChart } from 'react-icons/bi'

function FoodCard(){
    return (
        <div className="FoodCard">
            <div className="image-frame">
                <img 
                    src={cookies} 
                    alt="Placeholder recipe image"
                    className="card-image"/>
            </div>
            <div className="recipe-info">
                <div className="recipe-rating">
                    <FaStar fill="#F9AE67"/>
                    <FaStar fill="#F9AE67"/>
                    <FaStar fill="#F9AE67"/>
                    <FaStar fill="#F9AE67"/>
                    <FaStar fill="#F9AE67"/>
                </div>
                < div className="recipe-name">
                    Chocolate Chip Cookies
                </div>
                < div className="recipe-stats">
                    <div className="recipe-stats-box">
                        <CiClock2/>
                        CookTime
                    </div>
                    <div className="recipe-stats-box">
                        <BiDish/>
                        Serving Size
                    </div>
                </div>
            </div>
            <div className="pantry-info">
                <div>
                    <BiSolidDoughnutChart size={35}/>
                </div>
                <div className="pantry-text">
                    <div className="pantry-ratio">
                        pantry ratio
                    </div>
                    missing ingredients
                </div>
            </div>
            <div className="button">
                View Recipe
            </div>
        </div>
    )
}

export default FoodCard