import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import NavBar from "./NavBar.jsx";

function App() {
  const [count, setCount] = useState(0)

  return (
      <div>
          <div>
              <NavBar />
          </div>
      </div>
  )
}

export default App
