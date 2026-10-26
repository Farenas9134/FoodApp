import * as React from "react";
import * as Scrollytelling from '@bsmnt/scrollytelling';
import FoodCard from "../components/UI/FoodCard.tsx";
import PhoneFrame from "../components/UI/PhoneFrame.tsx";
import { FaInstagram, FaTiktok, FaYoutube } from "react-icons/fa";

// @ts-ignore
import instaCookies from "../assets/backgrounds/instaCookies.png";
// @ts-ignore
import phoneLogoScreen from "../assets/backgrounds/Phone-Logo-Screen.png";
// @ts-ignore
import phoneLinkScreen from "../assets/backgrounds/Phone-Paste-Link.png";
// @ts-ignore
import savedRecipeScreen from "../assets/backgrounds/saved-recipe.png";
// @ts-ignore
import send from "../assets/icons/sendVG.svg";
// @ts-ignore
import link from "../assets/icons/link.svg";
// @ts-ignore
import Rarrow from "../assets/icons/Arrow-R.svg";


// @ts-ignore
import "../css/home.css";

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
                        <div>
                            <button 
                                style={{ padding: '10px 30px' }}
                                className="flex items-center bg-[#C1622D] hover:bg-[#a54f21] text-white font-display text-[26px] font-semibold rounded-full shadow-lg transition-transform hover:scale-105 active:scale-95 cursor-pointer"
                                onClick={() => window.location.href = '/signup'}
                            >
                                Start saving recipes →
                            </button>
                        </div>                
                    </div>
                </div>
                <div className="foodcard-stack">
                    <div className="card1">
                        <FoodCard 
                            title='Chocolate Chip Cookies'
                            image_url=''
                            rating={4.5} 
                            total_time={5.372846293} 
                            servings='16 servings' 
                            missing_ingredients={2} 
                            pantry_ratio= {0.9}
                            recipe_id={5}/>
                    </div>
                    <div className="card2">
                        <FoodCard
                            title='Chocolate Chip Cookies'
                            image_url=''
                            rating={4} 
                            total_time={5.372846293} 
                            servings='16 servings' 
                            missing_ingredients={2} 
                            pantry_ratio= {0.9}
                            recipe_id={5}/>
                    </div>
                    <div className="card3">
                        <FoodCard
                            title='Chocolate Chip Cookies'
                            image_url=''
                            rating={4} 
                            total_time={5.372846293} 
                            servings='16 servings' 
                            missing_ingredients={2} 
                            pantry_ratio= {0.9}
                            recipe_id={5}/>
                    </div>
                </div>
            </div>
            
            {/* Bottom section --- Scrollytelling */}
            {/* <Scrollytelling.Root debug={{ label: "phone" }}> */}
            <Scrollytelling.Root>
                <Scrollytelling.Pin childHeight={"100vh"} pinSpacerHeight={'650vh'} top={0}>
                    <div className="relative w-full h-[100vh] overflow-hidden">
                        
                        {/* State 1: Intro / How it works */}
                        <Scrollytelling.Animation
                            tween={[
                                { start: 0, end: 15, fromTo: [{ y: 100, opacity: .25 }, { y: 0, opacity: 1 }] },
                                { start: 25, end: 35, to: { y: -80, opacity: 0 } }
                            ]}
                        >
                            <div className="absolute inset-0 flex flex-col items-center top-[10vh]">
                                <p className="subheader" id="1">How it works</p>
                                <p className="cps">COPY • PASTE • SAVE</p>
                            </div>
                        </Scrollytelling.Animation>

                        <Scrollytelling.Animation
                            tween={[
                                { start: 0, end: 15, fromTo: [{ opacity: 0 }, { opacity: 1 }] },
                                { start: 20, end: 38, to: { opacity: 0 } }
                            ]}
                        >
                            <div className="absolute bottom-10 text-[40px] font-display font-semibold text-[#1F3A28]">
                                ↓ Scroll
                            </div>
                        </Scrollytelling.Animation>

                        <Scrollytelling.Animation
                            tween={[
                                { start: 0, end: 25, fromTo: [{ y: 300, opacity: 0, scale: 0.8 }, { y: 120, opacity: 1, scale: 1 }] },
                                { start: 30, end: 38, to: { y: -100, opacity: 0, scale: 0.95 } }
                            ]}
                        >
                            <div className="absolute inset-x-0 top-[180px] flex justify-center">
                                <PhoneFrame picture={phoneLogoScreen} />
                            </div>
                        </Scrollytelling.Animation>


                        {/* State 2: COPY */}
                        <Scrollytelling.Animation
                            tween={[
                                { start: 35, end: 42, fromTo: [{ y: -30, opacity: 0 }, { y: 0, opacity: 1 }] },
                                { start: 58, end: 66, to: { opacity: 0 } }
                            ]}
                        >
                            <div className="absolute top-[55px] left-0 w-full flex justify-start pl-[20px] gap-1 z-20">
                                <p id="copy" className="cps">COPY</p>
                                <p className="cps">• PASTE • SAVE</p>
                            </div>
                        </Scrollytelling.Animation>

                        <Scrollytelling.Animation
                            tween={[
                                { start: 36, end: 48, fromTo: [{ x: -100, opacity: 0 }, { x: 0, opacity: 1 }] },
                                { start: 58, end: 66, to: { x: -80, opacity: 0 } }
                            ]}
                        >
                            <div className="absolute top-[120px] left-[20px] flex flex-col gap-[30px] z-10 max-w-[50%]">
                                <p className="font-display text-[#183C04] text-[96px] font-semibold underline decoration-[#C1622D] decoration-wavy">
                                    COPY
                                </p>
                                <div className="flex flex-col gap-[20px]">
                                    <p className="font-display text-[32px] text-[#183C04]">
                                        Found a recipe you'd like to save?
                                    </p>
                                    <p className="font-display text-[26px] text-[#183C04]/80">
                                        Just tap share and copy the link to the post, video, or website!
                                    </p>
                                </div>

                                <Scrollytelling.Animation
                                    tween={[{ start: 40, end: 50, fromTo: [{ y: 30, opacity: 0 }, { y: 0, opacity: 1 }] }]}
                                >
                                    <div className="flex flex-col gap-[40px]">
                                        <div className="flex max-w-[75%] h-[27px] gap-[12px] items-center text-[#183C04]/80">
                                            <p className="font-display text-[26px]">Works on</p>
                                            <FaInstagram />
                                            <FaTiktok />
                                            <FaYoutube />
                                            <p className="font-display text-[26px]">and recipe sites</p>
                                        </div>

                                        <div className="flex w-[390px] h-[52px] gap-[20px] items-center">
                                            <div className="flex justify-center items-center w-[140px] h-full bg-[#FAFAFA] rounded-[100px] border p-[12px] gap-[9px]">
                                                <img src={send} alt="Send Icon" />
                                                <p className="font-display text-[18px] text-[#183C04] font-medium">Share</p>
                                            </div>
                                            <img src={Rarrow} alt="right arrow" className="w-[20px]" />
                                            <div className="flex justify-center items-center w-[170px] h-full bg-[#C1622D] rounded-[100px] border p-[12px] gap-[6px]">
                                                <img src={link} className="brightness-0 invert" alt="Link Icon" />
                                                <p className="font-display text-[18px] text-[#FFFFFF] font-medium">Copy Link</p>
                                            </div>
                                        </div>
                                    </div>
                                </Scrollytelling.Animation>
                            </div>
                        </Scrollytelling.Animation>

                        <Scrollytelling.Animation
                            tween={[
                                { start: 36, end: 48, fromTo: [{ x: 120, opacity: 0, scale: 0.8 }, { x: 0, opacity: 1, scale: 1 }] },
                                { start: 58, end: 66, to: { opacity: 0, scale: 0.8 } }
                            ]}
                        >
                            <div className="absolute right-[40px] top-[100px]">
                                <PhoneFrame picture={instaCookies} />
                            </div>
                        </Scrollytelling.Animation>


                        {/* State 3: PASTE */}
                        <Scrollytelling.Animation
                            tween={[
                                { start: 62, end: 72, fromTo: [{opacity: 0 }, {opacity: 1 }] },
                                { start: 82, end: 90, to: { opacity: 0 } }
                            ]}
                        >
                            <div className="absolute top-[55px] left-0 w-full flex justify-start pl-[20px] gap-1 z-20">
                                <p className="cps">COPY • </p>
                                <p id="copy" className="cps">PASTE</p>
                                <p className="cps"> • SAVE</p>
                            </div>
                        </Scrollytelling.Animation>

                        <Scrollytelling.Animation
                            tween={[
                                { start: 62, end: 72, fromTo: [{ x: -80, opacity: 0 }, { x: 0, opacity: 1 }] },
                                { start: 82, end: 90, to: { x: -80, opacity: 0 } }
                            ]}
                        >
                            <div className="absolute top-[120px] left-[20px] flex flex-col gap-[30px] z-10 max-w-[50%]">
                                <p className="font-display text-[#183C04] text-[96px] font-semibold underline decoration-[#C1622D] decoration-wavy">
                                    PASTE
                                </p>
                                <div className="flex flex-col gap-[20px]">
                                    <p className="font-display text-[32px] text-[#183C04]">
                                        Then, drop the link into ReciKeep!
                                    </p>
                                    <p className="font-display text-[26px] text-[#183C04]/80">
                                        We'll pull out the ingredients, instructions, and any additional notes for your convenience.
                                    </p>
                                </div>
                            </div>
                        </Scrollytelling.Animation>

                        <Scrollytelling.Animation
                            tween={[
                                { start: 62, end: 72, fromTo: [{ opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1 }] },
                                { start: 82, end: 90, to: { opacity: 0, scale: 0.8 } }
                            ]}
                        >
                            <div className="absolute right-[40px] top-[100px]">
                                <PhoneFrame picture={phoneLinkScreen} />
                            </div>
                        </Scrollytelling.Animation>

                        {/* Save 4: SAVE */}
                        <Scrollytelling.Animation
                            tween={[
                                { start: 86, end: 95, fromTo: [{opacity: 0 }, {opacity: 1 }] }
                            ]}
                        >
                            <div className="absolute top-[55px] left-0 w-full flex justify-start pl-[20px] gap-1 z-20">
                                <p className="cps">COPY • PASTE • </p>
                                <p id="copy" className="cps">SAVE</p>
                            </div>
                        </Scrollytelling.Animation>

                        <Scrollytelling.Animation
                            tween={[
                                { start: 86, end: 92, fromTo: [{ x: -80, opacity: 0 }, { x: 0, opacity: 1 }] }
                            ]}
                        >
                            <div className="absolute top-[120px] left-[20px] flex flex-col gap-[30px] z-10 max-w-[50%]">
                                <p className="font-display text-[#183C04] text-[96px] font-semibold underline decoration-[#C1622D] decoration-wavy">
                                    SAVE
                                </p>

                                <ul className="font-display text-[24px] text-[#183C04]/80 flex flex-col gap-[12px] list-disc pl-6">
                                    <Scrollytelling.Animation tween={[{ start: 88, end: 93, fromTo: [{ y: 15, opacity: 0 }, { y: 0, opacity: 1 }] }]}>
                                        <li>Save all the recipes you want</li>
                                    </Scrollytelling.Animation>
                                    <Scrollytelling.Animation tween={[{ start: 90, end: 95, fromTo: [{ y: 15, opacity: 0 }, { y: 0, opacity: 1 }] }]}>
                                        <li>Match recipes with your pantry ingredients</li>
                                    </Scrollytelling.Animation>
                                    <Scrollytelling.Animation tween={[{ start: 92, end: 97, fromTo: [{ y: 15, opacity: 0 }, { y: 0, opacity: 1 }] }]}>
                                        <li>Plan your week with the recipes you want to make</li>
                                    </Scrollytelling.Animation>
                                    <Scrollytelling.Animation tween={[{ start: 94, end: 99, fromTo: [{ y: 15, opacity: 0 }, { y: 0, opacity: 1 }] }]}>
                                        <li>Share recipes with friends & family</li>
                                    </Scrollytelling.Animation>
                                </ul>

                                <Scrollytelling.Animation
                                tween={[
                                    { start: 95, end: 99, fromTo: [{ y: 30, opacity: 0, scale: 0.95 }, { y: 0, opacity: 1, scale: 1 }] }
                                    ]}
                                >
                                   <div>
                                        <button 
                                            style={{ padding: '10px 30px' }}
                                            className="flex items-center bg-[#C1622D] hover:bg-[#a54f21] text-white font-display text-[26px] font-semibold rounded-full shadow-lg transition-transform hover:scale-105 active:scale-95 cursor-pointer"
                                            onClick={() => window.location.href = '/signup'}
                                        >
                                            Start saving recipes →
                                        </button>
                                    </div>
                                </Scrollytelling.Animation>
                                
                            </div>
                        </Scrollytelling.Animation>

                        <Scrollytelling.Animation
                            tween={[
                                { start: 86, end: 95, fromTo: [{ opacity: 0, scale: 0.8, y: 40 }, { opacity: 1, scale: 1, y: 0 }] },
                                { start: 95, end: 100, to: { scale: 1.05 } }
                            ]}
                        >
                            <div className="absolute right-[40px] top-[100px]">
                                <PhoneFrame picture={savedRecipeScreen} />
                            </div>
                        </Scrollytelling.Animation>

                    </div>
                </Scrollytelling.Pin>
            </Scrollytelling.Root>
        </div>
    );
}

export default Home;