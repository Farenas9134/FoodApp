import { useEffect } from "react"

function Home(){
    useEffect(() => {
        console.log("Fetching recipes");

        fetch('/api/recipes')
         .then((response) => {
            if (!response.ok) {
                throw new Error('HTTP error!');
            }
            return response.json()
         })
          .then((data) => {
            console.log("Recipes returned from Flask:", data);
          });
    }, []);

    return (
        <div>
            <h1>Major Food App</h1>
            <p>Hello!</p>
        </div>
    )
}

export default Home