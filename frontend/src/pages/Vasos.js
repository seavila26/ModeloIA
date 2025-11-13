import React from 'react';
import Upload from '../components/Upload/Upload';

function Vasos(props) {
    const page_id = 1;
    return (
        <div style={{width: '100%', height: '100%'}}>
            <h1>Segmentación Vasos</h1>
            <Upload page_id={page_id} userEmail={props.userEmail}></Upload>
        </div>
    );
};

export default Vasos;