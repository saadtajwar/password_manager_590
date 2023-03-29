import React, {useEffect, useState} from 'react'

const SingularCredential = ({credential}) => {
    /*
        Credential is (object, array? probably should go with object) with:
            - Website username
            - Credential username
            - Credential password

    */

    return (
        <div>
            <p>Website name: {credential.websiteName}</p>
            <p>Your Username: {credential.username}</p>
            <p>Your Password: {credential.password}</p>
        </div>
    )
}

export default SingularCredential;