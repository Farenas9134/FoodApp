import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { api, ApiError } from "../components/api";

type User = { id: string; name: string; email: string };

type AuthContextType = {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string, remember: boolean) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // On first load, ask the server whether the cookie is still valid
  useEffect(() => {
    api<{ user: User }>("/me")
      .then((d) => setUser(d.user))
      .catch((e) => {
        if (!(e instanceof ApiError && e.status === 401)) console.error(e);
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, []);

  async function login(username: string, password: string, remember: boolean) {
    const d = await api<{ user: User }>("/login", {
      method: "POST",
      body: JSON.stringify({ username, password, remember }),
    });
    setUser(d.user);
  }

  async function logout() {
    await api("/logout", { method: "POST" });
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}