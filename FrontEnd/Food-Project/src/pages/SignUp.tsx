// @ts-ignore
import "../css/SignUp.css"
import { useState } from "react";
// @ts-ignore
import pasta from "../assets/foodPics/pasta.jpg";
import { Eye } from 'lucide-react';
import { EyeClosed } from "lucide-react";

import { Link } from 'react-router-dom';


function SignUp() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [showConfPassword, setShowConfPassword] = useState(false);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    // Avoids deprecated FormEvent
    // ComponentProps<"form"> gives all props a React form accepts
    // -> a prop (property) is read-only data passed from a parent component to a child component which
    // allows components to communicate and stay reusable
    async function handleSubmit(e: Parameters<NonNullable<React.ComponentProps<"form">["onSubmit"]>>[0]) {
        e.preventDefault();
        setError("");

        // Ensuring passwords match
        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        setLoading(true);

        // Adding user to database by making a request to the signup route on the backend
        try {
            const response = await fetch("/api/signup", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name,
                    email, 
                    password
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.message || "Unable to create an account, please try again later.");
                return;
            }
            
            // Redirecting to login page following a successful signup
            window.location.href = "/login";
        
        } catch {
            setError("Unable to connect. Please try again");
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="signup-page">
            <div className="signup-container">
                {/* Left side of the login container, will contain an image */}
                <div className="recipe-image">
                    <img src={pasta} alt="Image of a pasta dish"/>
                </div>

                {/* Right side of the login container, where the user will actually input info to login */}
                <div className="signup-form-container">
                    <form className="signup-form" onSubmit={handleSubmit}>

                        <h1>Welcome!</h1>

                        <h2>Create an account to begin exploring recipes!</h2>

                        {/* Username Field */}
                        <div className="input-field">
                            <label htmlFor="name">Username</label>
                            <input
                                id="name"
                                type="name"
                                autoComplete="name"
                                placeholder="Enter your username"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required
                            />
                        </div>

                        {/* Email Field */}
                        <div className="input-field">
                            <label htmlFor="email">Email</label>
                            <input
                                id="email"
                                type="email"
                                autoComplete="email"
                                placeholder="Enter your email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                        </div>

                        {/* Password Field */}
                        <div className="input-field">
                            <label htmlFor="password">Password</label>
                            <div className="password-input-container">
                                <input
                                    id="password"
                                    type={
                                        showPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Enter your password"
                                    autoComplete="current-password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    minLength={8}
                                    required
                                />

                                <button 
                                    type="button" 
                                    className="password-toggle"
                                    onClick={() => 
                                        setShowPassword(
                                            !showPassword
                                        )
                                    }
                                    aria-label={
                                        showPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                >
                                    {showPassword ? <EyeClosed size={20}/> : <Eye size={20}/>}
                                </button>
                            </div>
                        </div>

                        {/* Confirm Password Field */}
                        <div className="input-field">
                            <label htmlFor="confirmPassword">Confirm Password</label>
                            <div className="password-input-container">
                                <input
                                    id="confirmPassword"
                                    type={
                                        showConfPassword
                                            ? "text"
                                            : "password"
                                    }
                                    autoComplete="new-password"
                                    placeholder="Confirm your password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
                                    minLength={8}
                                    required
                                />

                                <button 
                                    type="button" 
                                    className="password-toggle"
                                    onClick={() => 
                                        setShowConfPassword(
                                            !showConfPassword
                                        )
                                    }
                                    aria-label={
                                        showConfPassword
                                            ? "Hide password"
                                            : "Show password"
                                    }
                                >
                                    {showConfPassword ? <EyeClosed size={20}/> : <Eye size={20}/>}
                                </button>
                            </div>
                        </div>

                        {error && <p role="alert">{error}</p>}

                        {/* If signup request is processing, "Signing up.." will show on the button, otherwise "Sign Up" will show */}
                        <button type="submit" disabled={loading} className="signup-button">
                            {loading ? "Signing up..." : "Sign Up"}
                        </button>

                        <div className="extra-text">
                            <div className="create-account">
                                <Link to="/login">Already have an account?</Link>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </main>

        // <form onSubmit={handleSubmit}>
        // <h1>Create an account</h1>

        // <label htmlFor="email">Email</label>
        // <input
        //     id="email"
        //     type="email"
        //     autoComplete="email"
        //     value={email}
        //     onChange={(e) => setEmail(e.target.value)}
        //     required
        // />

        // <label htmlFor="password">Password</label>
        // <input
        //     id="password"
        //     type="password"
        //     autoComplete="new-password"
        //     value={password}
        //     onChange={(e) => setPassword(e.target.value)}
        //     minLength={8}
        //     required
        // />
        
        // <label htmlFor="confirmPassword">
        //     Confirm password
        // </label>
        // <input
        //     id="confirmPassword"
        //     type="password"
        //     autoComplete="new-password"
        //     value={confirmPassword}
        //     onChange={(e) => setConfirmPassword(e.target.value)}
        //     minLength={8}
        //     required
        // />

        // {error && <p role="alert">{error}</p>}

        // <button type="submit" disabled={loading}>
        //     {loading ? "Creating account..." : "Sign up"}
        // </button>

        // <p>
        //     Already have an account? <a href="/login">Log in</a>
        // </p>
        // </form>
    );
}

export default SignUp;