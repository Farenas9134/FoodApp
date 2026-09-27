// @ts-ignore
import "../css/styles.css"

function NavBar(){

    return (
        <nav className="nav">
            <a href="/" className="site-title">
                ReciKeep
            </a>
            <ul>
                <li><a href="#" >About Us</a></li>
                <li><a href="#" >Recipes</a></li>
                <li><a href="#" >Community</a></li>
                <li><a href="#" >Pantry</a></li>
                <li><a href="#" >Contact Us</a></li>
            </ul>
            <ul>
                <a>
                    <form action="/search" method="get">
                        <button type="submit">Search</button>
                    </form>
                </a>
                <a href="/login" className="login">
                    Login
                </a>
            </ul>
        </nav>
    );
}

export default NavBar