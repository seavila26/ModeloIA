import styled from "styled-components";
import { v, btnReset } from "../../styles/variables";

export const SLogin = styled.div`
    height: 94vh;
    width: 100%;
    display: flex;
`;

export const SCard = styled.div`
    height: auto;
    width: auto;
    margin: auto;
`;

export const SForm = styled.div`
    height: 400px;
    width: 370px;
    background-color: rgb(17,50,80);
    border-radius: 30px;
    margin-top: ${v.xxlSpacing};

    h1 {
        text-align: center;
        padding: 25px 0 0 0;
        font-size: 35px;
        font-family: 'Roboto', sans-serif;
    }
`;

export const SInputEmail = styled.input`
    text-align: center;
    height: 50px;
    width: 70%;
    border: 2px solid black;
    border-radius: 12px;
    margin: auto;
    margin-top: 30px;
    font-size: 30px;
`;

export const SInputPassword = styled.input`
    text-align: center;
    height: 50px;
    width: 70%;
    border: 2px solid black;
    border-radius: 12px;
    margin: auto;
    margin-top: 30px;
    margin-bottom: 30px;
    font-size: 30px;
`;

export const SButton = styled.button`
    ${btnReset};
    width: 200px;
    height: 60px;
    border-radius: 10px;
    background: rgb(251,184,0);
    text-align: center;
    font-family: 'Roboto', sans-serif;
    margin: auto;
    margin-top: 10px;
    font-size: 20px;
    font-weight: bold;
    color: white;
`;