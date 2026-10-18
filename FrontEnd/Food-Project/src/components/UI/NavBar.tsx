// @ts-ignore
import "../../css/navbar.css"
// @ts-ignore
import logo from "../../assets/icons/ReciKeep-logo.svg"
import { Link } from 'react-router-dom'

function NavBar(){

    return (
        <nav className="nav">
            <Link to="/">
                <img src={logo} 
                alt="Site logo" 
                className="site-logo w-auto h-auto min-w-[150px] min-h-[40px] object-contain"/>
            </Link>
            <ul>
                <li><Link to="/about">About Us</Link></li>
                <li><Link to="/recipes">Recipes</Link></li>
                <li><Link to="/community">Community</Link></li>
                <li><Link to="/pantry">Pantry</Link></li>
                <li><Link to="/contact">Contact</Link></li>
            </ul>
            <ul>
                <Link to="/login" className="login">Log In</Link>
                <Link to="/signup" className="signup">Sign Up</Link>
            </ul>
        </nav>
    );
}

export default NavBar