import React, {useEffect, useState} from 'react'
import NewCredentialsForm from '../components/NewCredentialsForm'
import SingularCredential from '../components/SingularCredential'
import CredentialList from '../components/CredentialList'


const CredentialsInfo = ({credentialList, userID}) => {

    console.log('the list', credentialList);
    return (
        <div>
            <NewCredentialsForm userID={userID} />
            <CredentialList credentialList={credentialList} />
        </div>
    )
}

export default CredentialsInfo;