import React, {useState} from 'react'
import {useNavigate} from 'react-router-dom'

const LoginForm = ({user, setUser}) => {
    const [username, setUsername] = useState('');
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
                username,
                password
            }
            // send attempted user credentials to backend API and setUser to that
            // , then log that in local storage (prob gotta change this later to be more secure)
            // setUser(returnedUser)    
            // window.localStorage.setItem('loggedUser', JSON.stringify(returnedUser));
            setUsername('');
            setPassword('');
            navigate('/');
        } catch (error) {
            alert('Log in did not work')
        }
    }


  return (
    <div>
        <form onSubmit={handleSubmit}>
            <input value={username} onChange={(e) => setUsername(e.target.value)} />
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </form>
    </div>
  )
}

export default LoginForm