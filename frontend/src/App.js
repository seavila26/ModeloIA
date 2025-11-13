import React, { useState } from 'react';
import { Helmet } from 'react-helmet';
import { ThemeProvider } from 'styled-components';
import Layout from './components/Layout/Layout';
import Login from './components/Login/Login';
import Routes from './Routes';
import { GlobalStyle } from './styles/globalStyles';
import { lightTheme, darkTheme } from './styles/theme';

export const ThemeContext = React.createContext(null);

const App = () => {
    const [theme, setTheme] = useState("light");
    const [isAuth, setIsAuth] = useState();
    const [userEmail, setUserEmail] = useState('');
    const themeStyle = theme === 'light' ? lightTheme : darkTheme;

    const userAuth = (isUserAuth) => {
        console.log("user auth = " , isUserAuth)
        setIsAuth(isUserAuth)
    }

    const getUserEmail = (email) => {
        console.log("get user email = ", email)
        setUserEmail(email)
    }

    return (
        <ThemeContext.Provider value={{ setTheme, theme }}>
            {!isAuth && <Login userAuth={userAuth} getUserEmail={getUserEmail}></Login>}
            {isAuth && <ThemeProvider theme={themeStyle}>
                <GlobalStyle />
                <Helmet>
                    <title>Universidad de La Salle</title>
                    <link rel="preconnect" href="https://fonts.googleapis.com" />
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
                    <link
                        href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap"
                        rel="stylesheet"
                    />
                </Helmet>
                <Layout>
                    <Routes userEmail={userEmail}/>
                </Layout>
            </ThemeProvider>}
        </ThemeContext.Provider>
    );
};

export default App;