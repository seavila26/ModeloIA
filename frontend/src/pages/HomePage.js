import React from 'react';
import image  from "./../assets/intro.png"

function HomePage(props) {
    return (
        <div style={{width: '100%', height: '100%'}}>
            <h1>Universidad de La Salle</h1>
            {/* <h2>{props.userEmail}</h2> */}
            <div style={{width: '100%', height: '100%', display: "flex", alignItems: "center", justifyContent: "center"}}>
                <div style={{width: "50%"}}>
                    <h3 style={{padding: "0px 50px 0px 0px", textAlign: "justify"}}>Bienvenidos al software clinico para la detección de caracteristicas morfolicas en fotografias de fondo de ojo, en el menú de la izquierda podra seleccionar la caracteristica a segmentar individualmente ó utilizar el modelo entrenado para una segmentación completa.</h3>
                </div>
                <div style={{width: "50%", display: "flex", justifyContent: "center"}}>
                    <img src={image} width={500} alt="" ></img>
                </div>
            </div>
        </div>
    );
};

export default HomePage;