import React, { useState } from "react";
import { SLogin, SForm, SCard, SInputEmail, SInputPassword, SButton } from "./styles";
import logo from "./../../assets/universidadLogo.png"
import { Divider } from "@mui/material";
import { auth } from "../../firebase/config";
import { signInWithEmailAndPassword } from "firebase/auth"

const Login = (props) => {
    const [ email , setEmail ] = useState('');
    const [ password , setPassword ] = useState('');

    const submit = async () => {
        try {
            const res = await signInWithEmailAndPassword(auth, email, password)
            console.log(res);
            props.userAuth(true);
            props.getUserEmail(email);
        } catch (err) {
            console.error(err);
            alert(err.message);
        }
    }

    return(
        <SLogin>
            <SCard>
                <img src={logo} width={370} height={100} alt="" ></img>
                <SForm>
                    <h1 style={{color: "white"}}>Bienvenid@</h1>
                    <Divider style={{ background: 'white' }}></Divider>
                    <div style={{display: "flex", flexDirection: "column"}}>
                        <SInputEmail type="email" placeholder="Correo" onChange={(ev) => setEmail(ev.target.value)}></SInputEmail>
                        <SInputPassword type="password" placeholder="Contraseña" onChange={(ev) => setPassword(ev.target.value)}></SInputPassword>
                        <SButton onClick={submit}>INICIAR SESION</SButton>
                    </div>
                </SForm>
            </SCard>
        </SLogin>
    );
};

export default Login;