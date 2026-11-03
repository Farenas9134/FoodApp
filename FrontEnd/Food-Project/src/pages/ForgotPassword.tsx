// @ts-ignore
import "../css/ForgotPassword.css";
import { useState } from "react";
import type { SubmitEvent } from "react";

function ForgotPassword() {
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(e: Parameters<NonNullable<React.ComponentProps<"form">["onSubmit"]>>[0]) {
        e.preventDefault();
        setError("");
        setMessage("");

        setLoading(true);

        // Querying database to determine if user exists and then sending password reset link to user email from the backend
        try {
            const response = await fetch("api/forgot-password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email
                }),

            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.message || "Something went wrong.");
                return;
            }

            setMessage(data.message);
        } catch {
            setError("Unable to connect. Please try again.")
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="forgot-password-container">
            <h1>Forgot Password?</h1>

            <p>
                Enter the email associated with your account.
                We'll send you a link to reset your password.
            </p>

            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                {error && <p role="alert">{error}</p>}
                {message && <p role="status">{message}</p>}

                <button type="submit" disabled={loading}>
                    {loading ? "Sending..." : "Reset Password"}
                </button>
            </form>
        </div>
    );
}

export default ForgotPassword;