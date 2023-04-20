import React, { useState } from 'react'
import {useNavigate} from 'react-router-dom'
import axios from 'axios'


const RegisterForm = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const user = {
                username,
                email,
                password
            };
            // send call to backend to create user
            const apiURL = 'http://localhost:5000/api/users';
            const newUser = await axios.post(apiURL, user);
            const userID = newUser.id;
            setUsername('');
            setEmail('');
            setPassword('');
            navigate('/login');
        } catch (error) {
            alert("Registration did not work, please try again");
        }

    }

  return (
    <div>
        <form onSubmit={handleRegister}>
            <div>
                Username: <input value={username} onChange={(e)=>setUsername(e.target.value)}/>
                Email: <input value={email} onChange={(e)=>setEmail(e.target.value)} />
                Password: <input value={password} type="password" onChange={(e)=>setPassword(e.target.value)} />
                <button type="submit">Register new user</button>
            </div>
        </form>
    </div>
  )
}

export default RegisterForm