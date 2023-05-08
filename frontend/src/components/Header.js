import React, {useEffect, useState} from 'react'
import {Link, useLocation} from 'react-router-dom'

const Header = ({user}) => {
    const location = useLocation().pathname;
    const [registerVisibility, setRegisterVisibility] = useState(true);
    const [loginVisibility, setLoginVisibility] = useState(true);

    const registerVisible = { display: registerVisibility ? "" : "none"};
    const loginVisible = { display: loginVisibility ? "" : "none"};

    useEffect(() => {
        const setDisplayRegister = () => {
            if (location === '/register' || user) {
                setRegisterVisibility(false);
            } else {
                setRegisterVisibility(true);
            }
        }

        const setDisplayLogin = () => {
            if (location === '/login' || user) {
                setLoginVisibility(false);
            } else {
                setLoginVisibility(true);
            }
        }
        
        setDisplayRegister();
        setDisplayLogin();
    }, [location, user])



  return (
    <div>
        <div>
            <Link to='/'>Secure Password Manager</Link>
        </div>
        <div>
            <h1>Welcome back, {user.email}</h1>
        </div>
        <div style={registerVisible}>
            <Link to='/register'>Register</Link>
        </div>
        <div style={loginVisible}>
            <Link to='/login'>Log In</Link>
        </div>
    </div>
  )
}

export default Header;