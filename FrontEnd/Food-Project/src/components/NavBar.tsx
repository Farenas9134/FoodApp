// @ts-ignore
import "../css/styles.css"
// @ts-ignore
import logo from "../assets/ReciKeep_Icon.png"
// @ts-ignore
import user from "../assets/user.png"

function NavBar(){

    return (
        <nav className="nav">
            <a href="/">
                <img src={logo} alt="Site logo" className="site-logo"></img>
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
                <img src={user} alt="User Icon" className="user-icon"></img>
                    Log In
                </a>
            </ul>
        </nav>
    );
}

export default NavBar