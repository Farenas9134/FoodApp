// @ts-ignore
import "../css/ForgotPassword.css";
import { useState } from "react";

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
        <main className="forgot-password-page">
            <div className="forgot-password-container">
                <form className="forgot-password-form" onSubmit={handleSubmit}>
                <h1>Forgot Password?</h1>

                <h2>
                    Enter the email associated with your account.
                    We'll send you a link to reset your password.
                </h2>

                    <div className="email-field">
                        <label htmlFor="email">Email</label>
                        <input
                            id="email"
                            type="email"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    {error && <p role="alert">{error}</p>}
                    {message && <p role="status">{message}</p>}

                    {/* If forgot password request is processing, "Sending..." is displayed, otherwise "Send Password Reset Link" is displayed */}
                    <button type="submit" disabled={loading} className="forgot-password-button">
                        {loading ? "Sending..." : "Send Password Reset Link"}
                    </button>
                </form>
            </div>
        </main>
    );
}

export default ForgotPassword;