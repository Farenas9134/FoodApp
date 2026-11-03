import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/UI/NavBar";
import Home from "./pages/Home";
import SignUp from "./pages/SignUp";
import LogIn from "./pages/LogIn";
import Recipes from "./pages/Recipes";
import AboutUs from "./pages/About";
import RecipeDisplay from "./pages/RecipeDisplay";
import NotFoundPage from "./pages/NotFoundPage";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";

function App() {
  return (
      <BrowserRouter>
        {/*Everything outside the routes will load in every page  */}
        <NavBar/>

        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/signup" element={<SignUp/>} />
          <Route path="/login" element={<LogIn/>} />
          <Route path="/recipes" element={<Recipes/>} />
          <Route path='/about' element={<AboutUs/>} />
          <Route path='/recipe/:id' element={<RecipeDisplay/>}/>
          <Route path="*" element={<NotFoundPage />}/>
          <Route path="/forgot-password" element={<ForgotPassword/>} />
          <Route path="/reset-password" element={<ResetPassword/>} />
        </Routes>
      </BrowserRouter>
  );
}

export default App
