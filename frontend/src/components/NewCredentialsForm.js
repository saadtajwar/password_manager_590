import React, {useEffect, useState} from 'react'

const NewCredentialsForm = () => {
    const [websiteUsername, setWebsiteUsername] = useState('');
    const [credentialUsername, setCredentialUsername] = useState('');
    const [credentialPassword, setCredentialPassword] = useState('');
    const [randomPassword, setRandomPassword] = useState('');


    const handleSubmit = (e) => {
        e.preventDefualt();
        /*
            send POST request to our REST API to add this credential stuff into the user's credential storage
        */
    }

    const handleRandomPasswordSubmit = async (e) => {
        e.preventDefualt();
        setCredentialPassword("abc");
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                Credential Website:<input value={websiteUsername} onChange={(e) => setWebsiteUsername(e.target.value)} />
                Credential Username:<input value={credentialUsername} onChange={(e) => setCredentialUsername(e.target.value)} />
                Credential Password:<input type="password" value={credentialPassword} onChange={(e) => setCredentialPassword(e.target.value)} />
                <button type="submit">Add New Credential</button>
            </form>

            <form onSubmit={handleRandomPasswordSubmit}>

                <button type="submit">Generate Random Secure Password</button>
            </form>
        </div>
    )
}

export default NewCredentialsForm;