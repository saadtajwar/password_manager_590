import React, {useEffect, useState} from 'react'

const NewCredentialsForm = () => {
    const [websiteUsername, setWebsiteUsername] = useState('');
    const [credentialUsername, setCredentialUsername] = useState('');
    const [credentialPassword, setCredentialPassword] = useState('');


    const handleSubmit = (e) => {
        e.preventDefualt();
        /*
            send POST request to our REST API to add this credential stuff into the user's credential storage
        */
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input value={websiteUsername} onChange={(e) => setWebsiteUsername(e.target.value)} />
                <input value={credentialUsername} onChange={(e) => setCredentialUsername(e.target.value)} />
                <input type="password" value={credentialPassword} onChange={(e) => setCredentialPassword(e.target.value)} />
            </form>
        </div>
    )
}

export default NewCredentialsForm;