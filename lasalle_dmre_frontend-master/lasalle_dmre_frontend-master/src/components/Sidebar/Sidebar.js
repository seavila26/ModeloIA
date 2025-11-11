import React, { useContext, useRef, useState } from 'react';
import { SDivider, SLink, SLinkContainer, SLinkIcon, SLinkLabel, SLinkNotification, SLogo, SSearch, SSearchIcon, SSidebar, SSidebarButton, STheme, SThemeLabel, SThemeToggler, SToggleThumb } from './styles';

import { logoSVG } from '../../assets';

import { AiOutlineLeft, AiOutlineSearch, AiOutlineSetting } from 'react-icons/ai';
import { GiBrassEye, GiGooeyEyedSun, GiCyberEye, GiAbstract069 } from 'react-icons/gi';
import { FaHome } from 'react-icons/fa';
import { MdLogout } from 'react-icons/md';

import { ThemeContext } from './../../App';
import { useLocation } from 'react-router-dom';

const Sidebar = () => {
    const searchRef = useRef(null);
    const { setTheme, theme } = useContext(ThemeContext);
    const [ sidebarOpen, setSidebarOpen ] = useState(true);
    const { pathname } = useLocation();

    const searchClickHandler = () => {
        if (!sidebarOpen){
            setSidebarOpen(true);
            searchRef.current.focus();
        } else {
            // buscar funcionalidad
        }
    };

    return (
        <SSidebar isOpen={sidebarOpen}>
            <>
                <SSidebarButton isOpen={sidebarOpen} onClick={() => setSidebarOpen(p => !p)}>
                    <AiOutlineLeft />
                </SSidebarButton>
            </>
            <SLogo>
                <img src={logoSVG} alt="logo" />
            </SLogo>
            <SSearch onClick={searchClickHandler} style={!sidebarOpen ? {width: `fit-content` } : {}}>
                <SSearchIcon>
                    <AiOutlineSearch />
                </SSearchIcon>
                <input ref={searchRef} placeholder='Buscar' style={!sidebarOpen ? {width: 0, padding: 0} : {}}/>
            </SSearch>
            <SDivider />
            {linksArray.map(({ icon, label, notification, to }) => (
                <SLinkContainer key={label} isActive={pathname === to}>
                    <SLink to={to} style={!sidebarOpen ? {width: `fit-content`} : {}}>
                        <SLinkIcon>{icon}</SLinkIcon>
                        {sidebarOpen && (
                            <>
                                <SLinkLabel>{label}</SLinkLabel>
                                {!!notification && (
                                    <SLinkNotification>{notification}</SLinkNotification>
                                )}
                            </>
                        )}
                    </SLink>
                </SLinkContainer>
            ))}
            <SDivider />
            {secondaryLinksArray.map(({ icon, label, notification }) => (
                <SLinkContainer key={label}>
                    <SLink to="/" style={!sidebarOpen ? {width: `fit-content`} : {}}>
                        <SLinkIcon>{icon}</SLinkIcon>
                        {sidebarOpen && <SLinkLabel>{label}</SLinkLabel>}
                        {sidebarOpen && !!notification && (
                            <SLinkNotification>{notification}</SLinkNotification>
                        )}
                    </SLink>
                </SLinkContainer>
            ))}
            <SDivider />
            <STheme>
                {sidebarOpen && <SThemeLabel>Dark Mode</SThemeLabel>}
                <SThemeToggler
                    isActive={theme === 'dark'}
                    onClick={() => setTheme((p) => (p === 'light' ? "dark" : "light"))}
                >
                    <SToggleThumb style={theme === 'dark' ? { right: "1px" } : {  }}/>
                </SThemeToggler>
            </STheme>
        </SSidebar>
    );
};

const linksArray = [
    {
        label: "Inicio",
        icon: <FaHome />,
        to: "/lasalle_dmre_frontend",
        notification: 3
    },
    {
        label: "Disco Optico",
        icon: <GiBrassEye />,
        to: "/disco",
        notification: 0
    },
    {
        label: "Vasos",
        icon: <GiAbstract069 />,
        to: "/vasos",
        notification: 0
    },
    {
        label: "Macula",
        icon: <GiCyberEye />,
        to: "/macula",
        notification: 0
    },
    {
        label: "Modelo IA",
        icon: <GiGooeyEyedSun />,
        to: "/modelo",
        notification: 0
    }
];

const secondaryLinksArray = [
    {
        label: "Settings",
        icon: <AiOutlineSetting />,
        notification: 2
    },
    {
        label: "Logout",
        icon: <MdLogout />,
        notification: 0
    }
];

export default Sidebar;