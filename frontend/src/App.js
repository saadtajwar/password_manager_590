import React, {useState, useEffect} from 'react'
import {BrowserRouter as Router, Link, Routes, Route} from 'react-router-dom'
import Header from './components/Header'
import LoginForm from './components/LoginForm'
import RegisterForm from './components/RegisterForm'


const App = () => {
  const [user, setUser] = useState(null);


  return (
    <Router>
      <Header user={user} />

      <Routes>
        <Route path='/register' element={<RegisterForm />} />
        <Route path='/login' element={<LoginForm />} />
      </Routes>
    </Router>
  )

}

export default App;
