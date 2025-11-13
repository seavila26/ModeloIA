import React from 'react';
import { Dna } from 'react-loader-spinner'

const Loader = () => {
    return(
        <div style = {{margin: "auto"}}>
            <Dna visible={true} height="350" width="350" ariaLabel="Loading" wrapperStyle={{}} wrapperClass="dna-wrapper"/>
        </div>
    );
};

export default Loader;