import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./Auth";

function RequireAuth() {
    const { user, loading } = useAuth();
    if (loading) return null;
    return user ? <Outlet /> : <Navigate to="/login" replace />;
}

export default RequireAuth;