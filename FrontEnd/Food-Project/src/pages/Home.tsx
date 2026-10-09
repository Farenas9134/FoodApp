import * as React from "react"
import * as Scrollytelling from '@bsmnt/scrollytelling';
import FoodCard from "../components/UI/FoodCard.tsx"
import PhoneFrame from "../components/UI/PhoneFrame.tsx"
// @ts-ignore
import instaCookies from "../assets/backgrounds/instaCookies.png";
// @ts-ignore
import phoneLogoScreen from "../assets/backgrounds/Phone-Logo-Screen.png"

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
            
            {/* Bottom section --- Scrollytelling */}
            <Scrollytelling.Root debug={{ label: "phone" }}>
                <Scrollytelling.Pin childHeight={"100vh"} pinSpacerHeight={'400vh'} top={0}>
                    <div className="flex flex-col w-full gap-[140px] h-[100vh] overflow-hidden">
                        
                        <Scrollytelling.Animation 
                        tween={{
                            start:0,
                            end:10,
                            fromTo: [
                                {y: 400, opacity: .5},
                                {y:0, opacity:1},
                            ],
                        }}>
                            <div className="flex flex-col items-center">
                                <p className="subheader" id="1">How it works</p>
                                <p className="cps">COPY • PASTE • SAVE</p>
                            </div>
                        </Scrollytelling.Animation>

                        <Scrollytelling.Animation 
                        tween={{
                            start:0,
                            end:15,
                            fromTo: [
                                {y: 600, opacity: 0},
                                {y:0, opacity:1},
                            ],
                        }}>
                            <div className="absolute bottom-0 text-[40px] font-display font-semibold text-[#1F3A28]">
                                ↓ Scroll
                            </div>
                        </Scrollytelling.Animation>

                        <Scrollytelling.Animation
                        tween={{
                            start: 0,
                            end: 25,
                            fromTo: [
                                { y: 600, opacity: 0 },
                                { y: 0, opacity: 1 },
                            ],
                        }}
                        >
                            <div className="flex items-center flex-col">
                                <PhoneFrame picture={instaCookies} />
                            </div>
                        </Scrollytelling.Animation>
                    </div>

                </Scrollytelling.Pin>
            </Scrollytelling.Root>
        </div>
    )
}

export default Home