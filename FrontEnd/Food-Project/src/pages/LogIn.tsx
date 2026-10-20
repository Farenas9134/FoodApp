// @ts-ignore
import "../css/LogIn.css";
import { useState } from "react";
import type { SubmitEvent } from "react";

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

            window.location.href = "/home";
        } catch {
            setError("Unable to connect. Please try again.");
        } finally {
            setLoading(false);
        }
    }
    return (
        <form onSubmit={handleSubmit}>
            <h1>LogIn</h1>

            {/* Email Field */}
            <label htmlFor="email">Email</label>
            <input
                id="email"
                type="email"
                autoComplete="username"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />

            {/* Password Field */}
            <label htmlFor="password">Password</label>
            <input
                id="password"
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />

            {error && <p role="alert">{error}</p>}

            <button type="submit" disabled={loading}>
                {loading ? "Logging in..." : "Log in"}
            </button>
            </form>
    );
}

export default LogIn;