import { Component, useEffect } from "react"
import FoodCard from "../components/UI/FoodCard.tsx"
import PhoneFrame from "../components/UI/PhoneFrame.tsx"

// @ts-ignore
import "../css/home.css"

function Home() {
    return (
        <div className="page">
            <div className="top-sec">
                <div className="body">
                    <div className="sub-title">
                        Never lose a recipe to your feed again
                    </div>
                    <div className="desc">
                        <p>
                            Save recipes straight from TikTok and Instagram. ReciKeep pulls out the ingredients and steps automatically.
                        </p>
                        <p>
                            Then it checks what you've already got in your kitchen, so you always know what's actually cookable tonight. 
                        </p>                    
                    </div>
                </div>
                <div className="foodcard-stack">
                    <div className="card1">
                        <FoodCard/>
                    </div>
                    <div className="card2">
                        <FoodCard/>
                    </div>
                    <div className="card3">
                        <FoodCard/>
                    </div>
                </div>
            </div>
            <div className="bot-sec">
                <div>
                    <p className="subheader" id="1">How it works</p>
                    <p className="cps">COPY • PASTE • SAVE</p>
                </div>
            </div>
            <PhoneFrame></PhoneFrame>
        </div>
    )
}

// function Home(){
//     useEffect(() => {
//         console.log("Fetching recipes");

//         fetch('/api/recipes')
//          .then((response) => {
//             if (!response.ok) {
//                 throw new Error('HTTP error!');
//             }
//             return response.json()
//          })
//           .then((data) => {
//             console.log("Recipes returned from Flask:", data);
//           });
//     }, []);

//     return (
//         <div>
//             <h1>Major Food App</h1>
//             <p>Hello!</p>
//         </div>
//     )
// }

export default Home