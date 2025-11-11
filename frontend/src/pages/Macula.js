import React from 'react';
import Upload from '../components/Upload/Upload';

function Macula(props) {
    const page_id = 2;
    return (
        <div style={{width: '100%', height: '100%'}}>
            <h1>Segmentación Macula</h1>
            <Upload page_id={page_id} userEmail={props.userEmail}></Upload>
        </div>
    );
};

export default Macula;