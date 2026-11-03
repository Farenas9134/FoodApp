import { useState } from "react"; 
import { useNavigate } from "react-router-dom";

function ResetPassword() {
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
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
        <div className="reset-password-container">
            
        </div>
    );
}

export default ResetPassword;