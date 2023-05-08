import React, {useState, useEffect} from 'react'
import {BrowserRouter as Router, Link, Routes, Route} from 'react-router-dom'
import Header from './components/Header'
import LoginForm from './components/LoginForm'
import RegisterForm from './components/RegisterForm'
import CredentialsInfo from './components/CredentialsInfo'


const App = () => {
  const [user, setUser] = useState(null);
  const [credentialList, setCredentialList] = useState(null);


  useEffect(()=> {
    const loggedUser = window.localStorage.getItem('loggedUser');
    if (loggedUser) {
      const existingUser = JSON.parse(loggedUser);
      setUser(existingUser);
    }
  }, [])



  return (
    <Router>
      <Header user={user} />

      <Routes>
        <Route path='/register' element={<RegisterForm />} />
        <Route path='/login' element={<LoginForm user={user} setUser={setUser} />} />
        <Route path='/' element={<CredentialsInfo credentialList={credentialList} userID={user.userID}/>} />

      </Routes>
    </Router>
  )

}

export default App;
