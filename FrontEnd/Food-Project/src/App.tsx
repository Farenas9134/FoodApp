import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/UI/NavBar";
import Home from "./pages/Home";
import SignUp from "./pages/SignUp";
import LogIn from "./pages/LogIn";
import Recipes from "./pages/Recipes";
import AboutUs from "./pages/About";

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
          {/* <Route path="*" element={<NotFoundPage />}/> */}
        </Routes>
      </BrowserRouter>
  );
}

export default App
