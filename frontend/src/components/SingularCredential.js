import React, {useEffect, useState} from 'react'

const SingularCredential = ({credential}) => {
    const [sharedUsername, setSharedUsername] = useState('');


    const handleSubmit = async (e) => {
        try {
            e.preventDefault();
            const sharedCredential = credential;
            const apiURL = `http://localhost:5000/api/users/${userID}/share`;
            const returnedMessage = await axios.post(apiURL, sharedCredential);
            setSharedUsername('');
        } catch (error) {
            console.log('Sharing did not work');
        }        
    }
    
    return (
        <div>
            <p>Website name: {credential.websiteName}</p>
            <p>Your Username: {credential.username}</p>
            <p>Your Password: {credential.password}</p>
            <form onSubmit={handleSubmit}>
                Share Wtih: <input value={sharedUsername} onChange={(e)=>sharedUsername(e.target.value)}/>
            </form>
        </div>
    )
}

export default SingularCredential;