// @ts-ignore
import "../css/LogIn.css";
import { useState } from "react";
import type { SubmitEvent } from "react";
// @ts-ignore
import pasta from "../assets/foodPics/pasta.jpg";

function LogIn() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e: SubmitEvent<HTMLFormElement>) {
        e.preventDefault();
        setError("")
        setLoading(true)
        
        // Making request to our backend where it will check if the user exists in our database
        try {
            const response = await fetch("/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify({ email, password}),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.message || "Invalid email or password");
                return;
            }
            
            // Will change when we make a profile page or something similar
            window.location.href = "/home";
        } catch {
            setError("Unable to connect. Please try again.");
        } finally {
            setLoading(false);
        }
    }
    return (
        <main className="login-page">
                <div className="login-container">
                    {/* Left side of the login container, will contain an image */}
                    <div className="recipe-image">
                        <img src={pasta} alt="Image of a pasta dish"/>
                    </div>

                    {/* Right side of the login container, where the user will actually input info to login */}
                    <div className="login-form-container">
                        <form className="login-form" onSubmit={handleSubmit}>

                            <h1>Login</h1>

                            {/* Email Field */}
                            <div className="input-field">
                                <label htmlFor="email">Email</label>
                                <input
                                    id="email"
                                    type="email"
                                    autoComplete="username"
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
                                        type="password"
                                        autoComplete="current-password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        required
                                    />
                                </div>
                            </div>

                            {error && <p role="alert">{error}</p>}

                            {/* If login request is processing, "Logging in" will show on the button, otherwise "Log in" will show */}
                            <button type="submit" disabled={loading} className="login-button">
                                {loading ? "Logging in..." : "Log in"}
                            </button>
                        </form>
                    </div>
                </div>
        </main>
    );
}

export default LogIn;