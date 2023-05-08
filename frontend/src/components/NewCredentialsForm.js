import React, {useEffect, useState} from 'react'
import axios from 'axios'


const NewCredentialsForm = ({userID}) => {
    const [websiteUsername, setWebsiteUsername] = useState('');
    const [credentialUsername, setCredentialUsername] = useState('');
    const [credentialPassword, setCredentialPassword] = useState('');


    const handleSubmit = (e) => {
        e.preventDefualt();
        const newCredential = {
            website: websiteUsername,
            alias: credentialUsername,
            password: credentialPassword
        }
        const apiURL = `http://localhost:5000/api/users/${userID}/add`;
        const returnedMessage = await axios.post(apiURL, newCredential);
        setWebsiteUsername('');
        setCredentialUsername('');
        setCredentialPassword('');
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                Credential Website:<input value={websiteUsername} onChange={(e) => setWebsiteUsername(e.target.value)} />
                Credential Username:<input value={credentialUsername} onChange={(e) => setCredentialUsername(e.target.value)} />
                Credential Password:<input type="password" value={credentialPassword} onChange={(e) => setCredentialPassword(e.target.value)} />
                <button type="submit">Add New Credential</button>
            </form>

        </div>
    )
}

export default NewCredentialsForm;