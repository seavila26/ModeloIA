import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import Login from './components/Login/Login'
import { BrowserRouter as Router } from 'react-router-dom';

ReactDOM.render(
  <Router>
    <App />
    {/* <Login /> */}
  </Router>,
  document.getElementById('root')
);