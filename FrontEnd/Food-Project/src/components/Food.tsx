
function Food(){

    const food = "Orange";
    const food2 = "Banana";

    return(
        <ul>
            <li>Apple</li>
            <li>{food}</li>
            <li>{food2.toUpperCase()}</li>

        </ul>
    );
}

export default Food