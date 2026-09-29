// @ts-ignore
import "../css/navbar.css"
// @ts-ignore
import logo from "../assets/ReciKeep_Icon2.png"

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
                <a href="/login" className="login">
                    Log In
                </a>
                <a href="/signup" className="signup">
                    Sign Up
                </a>
            </ul>
        </nav>
    );
}

export default NavBar