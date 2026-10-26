// @ts-ignore
import poke from "../assets/svgs/Giratina.png";
// @ts-ignore
import drapion from "../assets/svgs/drapion.webp";
function AboutUs() {
    return (
        <div className="flex flex-col w-full min-h-screen mx-auto px-[3%] pt-[3%] gap-10 font-display text-[#183C04]">

            <section className="text-center">
                <h1 className="text-[56px] font-bold">About ReciKeep</h1>
            </section>

            <section className="max-w-4xl mx-auto text-[24px] text-center flex flex-col gap-6">
                <p>You know the feeling</p>
                <p> 
                    While scrolling on TikTok or Instagram, you see an easy recipe that'll solidify your status as a home chef. 
                    But you're busy! So you save the reel, promising to come back to it.
                    Days go on, and and by the time you're hungry, you just found the new viral 'super gooey melt-in-your-mouth cinnamin rolls' forgetting all about the original recipe.
                    And the cycle repeats anew.
                </p>
                <p>
                    We got tired of losing recipes to the endless feed, so we built ReciKeep!
                </p>
            </section>

            <section className="max-w-2xl mx-auto text-center">
                <h2 className="text-[36px] font-bold mb-3">Who we are</h2>
                <p className="text-[24px]">
                    We are Francisco and Shalim. We wanted to prove we could build a full-stack app that fixes a small everyday annoyance
                </p>
            </section>
            <div className="flex flex-col items-center">
                <img src={drapion} width={400}/>
                <p>I like drapion</p>
            </div>
        </div>

    )
}

export default AboutUs