// @ts-ignore
import "../css/ResetPassword.css";
import { useState } from "react"; 
import { useNavigate } from "react-router-dom";

import { Eye } from 'lucide-react';
import { EyeClosed } from "lucide-react";

function ResetPassword() {
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [showConfPassword, setShowConfPassword] = useState(false);
    const [error, setError] = useState("");
    const [message, setMesssage] = useState("");
    const [loading, setLoading] = useState(false);

    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    const navigate = useNavigate();

    // User is taken to a page to reset their password after clicking link sent to email
    async function handleSubmit(e: Parameters<NonNullable<React.ComponentProps<"form">["onSubmit"]>>[0]) {
        e.preventDefault();
        setError("");
        setMesssage("");

        if (!token) {
            setError("Invalid or missing reset token.");
            return;
        }

        if (password !== confirmPassword) {
            setError("Passwords do not match.");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch('api/reset-password', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    token,
                    password
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                setError(data.message || "Invalid email or invalid token. Please try again.");
                return;
            }

            setMesssage(data.message);
            setPassword("");
            setConfirmPassword("");

            navigate("/login");
        } catch {
            setError("Unable to connect. Please try again.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <main className="reset-password-page">
            <div className="reset-password-container">
                {/* Where users will input information */}
                <div className="reset-password-form-container">
                    <form onSubmit={handleSubmit}>
                        <h1>Reset Password</h1>

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
                                    placeholder="New Password"
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
                                    placeholder="Confirm New Password"
                                    autoComplete="new-password"
                                    value={confirmPassword}
                                    onChange={(e) => setConfirmPassword(e.target.value)}
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
                        {message && <p role="status">{message}</p>}

                        {/* If reset password request is processing, "Resetting Password..." is displayed, otherwise "Reset Password" is displayed */}
                        <button type="submit" disabled={loading} className="reset-password-button">
                            {loading ? "Resetting Password..." : "Reset Password"}
                        </button>
                    </form>
                </div>
            </div>
        </main>
    );
}

export default ResetPassword;