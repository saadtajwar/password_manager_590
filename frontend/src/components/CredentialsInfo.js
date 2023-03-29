import React, {useEffect, useState} from 'react'
import NewCredentialsForm from '../components/NewCredentialsForm'
import SingularCredential from '../components/SingularCredential'


/*

Whats in a credential:
    - Name of the website
    - Their username
    - Their password
    * need to figure out if credential should include an array of ppls usernames its shared w/ ? *
*/

const CredentialsInfo = ({credentialList}) => {


    return (
        <div>
            <NewCredentialsForm />
            {credentialList.map(credential => 
                <SingularCredential credential={credential} />)}
        </div>
    )
}

export default CredentialsInfo;