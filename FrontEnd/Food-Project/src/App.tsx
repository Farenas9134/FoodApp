import { BrowserRouter, Routes, Route } from "react-router-dom";
import NavBar from "./components/UI/NavBar";
import Home from "./pages/Home";
import SignUp from "./pages/signup";
import LogIn from "./pages/login";

function App() {
  return (
      <BrowserRouter>
        {/*Everything outside the routes will load in every page  */}
        <NavBar/>

        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/signup" element={<SignUp/>} />
          <Route path="/login" element={<LogIn/>} />
          {/* <Route path="*" element={<NotFoundPage />}/> */}
        </Routes>
      </BrowserRouter>
  );
}

export default App
