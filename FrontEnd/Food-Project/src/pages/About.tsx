// @ts-ignore
import giratina from "../assets/svgs/Giratina.png";
// @ts-ignore
import drapion from "../assets/svgs/drapion.webp";
// @ts-ignore
import gyarados from "../assets/svgs/gyarados.webp";
// @ts-ignore
import wobbuffet from "../assets/svgs/wobbuffet.png";

function getRandomPokemon(): string {
    const pokemonList: string[] = [drapion, giratina, wobbuffet, gyarados];
    const randomIndex = Math.floor(Math.random() * pokemonList.length);
    const randomPokemon: string = pokemonList[randomIndex]
    return randomPokemon
}
function AboutUs(): React.JSX.Element {
    return (
        <div className="flex flex-col w-full min-h-screen mx-auto px-[3%] pt-[3%] gap-10 font-display text-[#183C04]">

            <section className="text-center">
                <h1 className="text-4xl font-bold">About ReciKeep</h1>
            </section>

            <section className="max-w-4xl mx-auto text-lg text-center flex flex-col gap-6">
                <p>You know the feeling!!!</p>
                <p> 
                    While scrolling on TikTok or Instagram, you see an easy recipe that'll solidify your status as a home chef. 
                    But you're busy! So you save the reel, promising to come back to it later.
                    Days go on, and and by the time you remember, you just found the next new viral 'super gooey melt-in-your-mouth brown butter with heavy cream poured on top cinnamin rolls' forgetting all about the original recipe.
                    And the cycle repeats anew.
                </p>
                <p>
                    We got tired of losing recipes to doomscrolling sessions, so we built ReciKeep!
                </p>
            </section>

            <section className="max-w-2xl mx-auto text-center">
                <h2 className="text-4xl font-bold mb-3 ">Who we are</h2>
                <p className="text-lg">
                    We are Francisco and Shalim. Two computer science graduates who wanted to prove we could build a full-stack app that fixes a small everyday annoyance.
                </p>
            </section>
            <div className="flex flex-col items-center">
                <img src={getRandomPokemon()} width={300}/>
            </div>
        </div>

    )
}

export default AboutUs