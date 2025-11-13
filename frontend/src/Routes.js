import React from 'react';
import { Route, Switch } from 'react-router-dom';
import DiscoOptico from './pages/DiscoOptico';
import Vasos from './pages/Vasos';
import HomePage from './pages/HomePage';
import Macula from './pages/Macula';

const Routes = (props) => {
    return (
        <Switch>
            <Route exact path="/lasalle_dmre_frontend">
                <HomePage userEmail={props.userEmail}/>
            </Route>
            <Route exact path="/disco">
                <DiscoOptico userEmail={props.userEmail}/>
            </Route>
            <Route exact path="/vasos">
                <Vasos userEmail={props.userEmail}/>
            </Route>
            <Route exact path="/macula">
                <Macula userEmail={props.userEmail}/>
            </Route>
            <Route exact path="/modelo">
                <h1>Modelo Inteligencia Artificial</h1>
            </Route>
        </Switch>
    );
}

export default Routes;