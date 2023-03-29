import React, { useState } from 'react'
import {useNavigate} from 'react-router-dom'


const RegisterForm = () => {
    const [name, setName] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const user = {
                name,
                username,
                password
            };
            // send call to backend to create user
            
            setName('');
            setUsername('');
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
                Name: <input value={name} onChange={(e)=>setName(e.target.value)}/>
                Username: <input value={username} onChange={(e)=>setUsername(e.target.value)} />
                Password: <input value={password} type="password" onChange={(e)=>setPassword(e.target.value)} />
                <button type="submit">Register new user</button>
            </div>
        </form>
    </div>
  )
}

export default RegisterForm