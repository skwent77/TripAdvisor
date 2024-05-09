import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import NavBar from "./Components/NavBar.jsx";
import SideBar from "./Components/SideBar.jsx";
import MainPlanContents, {MainFormContents} from "./Components/MainContent.jsx";
import IntroPage from "./Components/IntroPage.jsx";
import EmptyPage from "./Components/EmptyPage.jsx";
import {CreateForm} from "./Components/CreateForm.jsx"

import { BrowserRouter, Route , Routes } from 'react-router-dom';
import FlightPlan from "./Components/FlightPlan.jsx";
import TripForm from "./Components/TripForm.jsx";
import LoadingScreen from "./Components/LoadingScreen.jsx";
import Footer from "./Components/Footer.jsx";
import LoadingForChange from "./Components/LoadingForChange.jsx";
function App() {
  return (
      <BrowserRouter>
          <div style={{position: "relative"}}>
              <div><NavBar/></div>
              <div style={{display: "flex"}}>
                  <SideBar/>
                  <Routes>
                      <Route path="/" element={<IntroPage/>}/>
                      <Route path="/create_form" element={<MainFormContents/>}/>
                      <Route path="/chat/:targetId" element={<MainPlanContents/>}/>
                      <Route path="/create_chat" element={<CreateForm/>}/>
                      <Route path="/flight" element={<FlightPlan/>}/>
                      <Route path="/loading" element={<LoadingForChange/>}/>
                      <Route path="/intro" element={<IntroPage/>}/>
                      <Route path="*" element={<EmptyPage/>}/>
                  </Routes>
              </div>

          </div>
      </BrowserRouter>

  )
}

export default App
