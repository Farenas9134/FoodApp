// @ts-ignore
import "../css/SignUp.css"
import { useState } from "react";
import type { ComponentProps } from "react";

function SignUp() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const[confirmPassword, setConfirmPassword] = useState("");
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
        <form onSubmit={handleSubmit}>
        <h1>Create an account</h1>

        {/* Username Field */}
        <label htmlFor="name">Username</label>
        <input
            id="name"
            type="name"
            autoComplete="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
        />

        {/* Email Field */}
        <label htmlFor="email">Email</label>
        <input
            id="email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
        />

        {/* Password Field */}
        <label htmlFor="password">Password</label>
        <input
            id="password"
            type="password"
            autoComplete="new-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={8}
            required
        />
        
        {/* Confirm Password Field */}
        <label htmlFor="confirmPassword">
            Confirm password
        </label>
        <input
            id="confirmPassword"
            type="password"
            autoComplete="new-password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            minLength={8}
            required
        />

        {error && <p role="alert">{error}</p>}

        <button type="submit" disabled={loading}>
            {loading ? "Creating account..." : "Sign up"}
        </button>

        <p>
            Already have an account? <a href="/login">Log in</a>
        </p>
        </form>
    );
}

export default SignUp;