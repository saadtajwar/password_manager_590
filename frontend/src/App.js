import React, {useState, useEffect} from 'react'
import {BrowserRouter as Router, Link, Routes, Route} from 'react-router-dom'
import Header from './components/Header'
import LoginForm from './components/LoginForm'
import RegisterForm from './components/RegisterForm'
import CredentialsInfo from './components/CredentialsInfo'


const App = () => {
  const [user, setUser] = useState(null);
  const [credentialList, setCredentialList] = useState(null);


  /*
    - make a useEffect to get the stored credentials
    - make a useEffect to see if the user is logged in? (check localStorage, honestly might need to find better option than localStorage)
  */


  return (
    <Router>
      <Header user={user} />

      <Routes>
        <Route path='/register' element={<RegisterForm />} />
        <Route path='/login' element={<LoginForm />} />
        <Route path='/' element={<CredentialsInfo credentialList={credentialList} />} />

      </Routes>
    </Router>
  )

}

export default App;
