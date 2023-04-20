import React, {useEffect, useState} from 'react'
import SingularCredential from '../components/SingularCredential'

const CredentialList = ({credentialList}) => {

    return (
        <div>
            {credentialList.map(credential => 
                <SingularCredential credential={credential} key={credential.websiteName}/>)}
        </div>
    )
}

export default CredentialList;