import axios from 'axios';
import React, {useState} from 'react'
import {useNavigate} from 'react-router-dom'

const LoginForm = ({user, setUser}) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    if (user) {
        return (
            <div>
                Already logged in!
            </div>
        )
    }

    const handleSubmit = async (e) => {
        try {
            e.preventDefault();
            const loggingInUser = {
                email,
                password
            }
            const apiURL = 'http://localhost:5000/api/users/login';
            const loggedUser = await axios.post(apiURL, loggingInUser);
            const userID = loggedUser.user_id;
            const user = {email, password, userID};
            setUser(user);
            window.localStorage.setItem('loggedUser', JSON.stringify(user));
            // send attempted user credentials to backend API and setUser to that
            // , then log that in local storage (prob gotta change this later to be more secure)
            // setUser(returnedUser)    
            // window.localStorage.setItem('loggedUser', JSON.stringify(returnedUser));
            setEmail('');
            setPassword('');
            navigate('/');
        } catch (error) {
            console.log('Log in did not work');
        }
    }


  return (
    <div>
        <form onSubmit={handleSubmit}>
            <input value={email} onChange={(e) => setEmail(e.target.value)} />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </form>
    </div>
  )
}

export default LoginForm