import React, {useEffect, useState} from 'react'
import NewCredentialsForm from '../components/NewCredentialsForm'
import SingularCredential from '../components/SingularCredential'
import CredentialList from '../components/CredentialList'


/*

Whats in a credential:
    - Name of the website
    - Their username
    - Their password
    * need to figure out if credential should include an array of ppls usernames its shared w/ ? *
*/

const CredentialsInfo = ({credentialList}) => {

    console.log('the list', credentialList);
    return (
        <div>
            <NewCredentialsForm />
            <CredentialList credentialList={credentialList} />
        </div>
    )
}

export default CredentialsInfo;