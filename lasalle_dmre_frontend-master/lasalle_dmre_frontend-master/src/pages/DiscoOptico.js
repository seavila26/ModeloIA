import React from 'react';
import Upload from '../components/Upload/Upload';

function DiscoOptico(props) {
    const page_id = 0;
    return (
        <div style={{width: '100%', height: '100%'}}>
            <h1>Segmentación Disco Optico</h1>
            <Upload page_id={page_id} userEmail={props.userEmail}></Upload>
        </div>
    );
};

export default DiscoOptico;